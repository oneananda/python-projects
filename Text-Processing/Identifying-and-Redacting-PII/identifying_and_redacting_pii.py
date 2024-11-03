"""
This program contains functions which identifies 
and redacts Personally Identifiable Information (PII).
"""

import re
import argparse
import os
import uuid
import logging
from datetime import datetime
import yaml

TEXT_EXT = '.txt'

PARSER = argparse.ArgumentParser(description="PII Redacting parameters!")
PARSER.add_argument("INP_PATH",type=str,help="Path of the text file")
PARSER.add_argument("REDACT_OR_MASK",type=str,help="Option to redacting or masking")

ARGS = PARSER.parse_args()

REDACT_OR_MASK = ARGS.REDACT_OR_MASK if ARGS.REDACT_OR_MASK in ["Redact", "Mask"] else "Redact"

with open('config.yaml', 'r', encoding="utf-8") as logfile:
    config = yaml.safe_load(logfile)

LOG_DIR = config['logging']['log_dir']

os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, f"pii_process_{datetime.now().strftime('%Y-%m-%d')}.log")

logging.basicConfig(
filename = LOG_FILE,
level= logging.INFO,
format= '%(asctime)s - %(levelname)s- %(message)s'
)

# Dictionary to store the count of redactions for each PII type

def redact_pii(given_path):
    """
    This function identifies 
    and redacts Personally Identifiable Information (PII).
    """
    path, file_name = os.path.split(given_path)
    # print("Path:", PATH)
    # print("Filename:", FILE_NAME)
    content = ""
    file_stamp = str(uuid.uuid4())[0:7].upper()

    try:
        with open(given_path, "r", encoding="utf-8") as orginal_file:
            logging.info("Session Id: %s, opened file %s for reading.",file_stamp, given_path)
            logging.info("Process option : %s .", ARGS.REDACT_OR_MASK)
            content = orginal_file.read()
    # Process the content as needed
    except FileNotFoundError:
        print(f"The file at {given_path} was not found.")
        logging.error("The file at %s was not found.", given_path)
    except PermissionError:
        print(f"Permission denied for accessing the file at {given_path}.")
        logging.error("Permission denied for accessing the file at %s.", given_path)
    except UnicodeDecodeError:
        print(f"Could not decode the file at {given_path}. Check the file encoding.")
        logging.error("Could not decode the file at %s. Check the file encoding.", given_path)

    content = process_content(content, file_stamp)

    random_file_name = file_name.replace(TEXT_EXT,'') +'_'+ file_stamp + TEXT_EXT
    new_file_path = os.path.join(path, random_file_name)
    with open(new_file_path, "w", encoding="utf-8") as processed_file:
        processed_file.write(content)
    print(f"Process complete, file saved at {new_file_path}")
    logging.info("Session Id: %s, process complete, file saved at %s.", file_stamp, new_file_path)
    return content

def process_content(content, file_stamp):
    """
    This function processes the content 
    and redacts Personally Identifiable Information (PII).
    """
    redacting_patterns = {
        'EMAIL': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
        'PHONE': r'\b(\+?\d{1,2})?\s?(\(?\d{3}\)?)?\s?-?\d{3}-?\d{4}\b',
        'SSN': r'\b\d{3}-\d{2}-\d{4}\b',
        'CREDIT_CARD': r'\b(?:\d{4}-?){3}\d{4}\b',
        'DATE_OF_BIRTH': r'\b\d{2}[/-]\d{2}[/-]\d{4}\b',
        'PASSPORT': r'\b[0-9]{9}\b',  # Example for U.S. passport numbers
        'DRIVER_LICENSE': r'\b[A-Z]{1,2}-\d{3,6}-\d{3,6}\b',
        'BANK_ACCOUNT': r'\b\d{9,18}\b',
        'IP_ADDRESS': r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
        'MAC_ADDRESS': r'\b([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})\b',
        'PHYSICAL_ADDRESS': r'\b\d+\s[A-Za-z]+(?:\s[A-Za-z]+)*\b'  # Basic pattern
    }
    # Define patterns and corresponding masking functions
    masking_patterns = {
        'EMAIL': (
            r'([a-zA-Z0-9._%+-])([a-zA-Z0-9._%+-]*)(@[\w.-]+\.[a-zA-Z]{2,})', 
            lambda m: m.group(1) + "****" + m.group(3)
        ),
        'PHONE': (
            r'\b(\+?\d{1,2})?[-.\s]?(\(?\d{3}\)?)?[-.\s]?(\d{3})[-.\s]?(\d{4})\b', 
            lambda m: "***-***-" + m.group(4)
        ),
        'SSN': (
            r'\b(\d{3})-(\d{2})-(\d{4})\b', 
            lambda m: "***-**-" + m.group(3)
        ),
        'CREDIT_CARD': (
            r'\b(\d{4})-?(\d{4})-?(\d{4})-?(\d{4})\b', 
            lambda m: "****-****-****-" + m.group(4)
        ),
        'DATE_OF_BIRTH': (
            r'\b(\d{2})[/-](\d{2})[/-](\d{4})\b', 
            lambda m: "****/**/" + m.group(3)
        ),
        'PASSPORT': (
            r'\b(\d{3})(\d{3})(\d{3})\b', 
            lambda m: "***-***-" + m.group(3)
        ),
        'DRIVER_LICENSE': (
            r'\b([A-Z]{1,2})-\d{3,6}-\d{3,6}\b', 
            lambda m: m.group(1) + "-***-***"
        ),
        'BANK_ACCOUNT': (
            r'\b\d{9,18}\b', 
            lambda m: "****" + m.group(0)[-4:]
        ),
        'IP_ADDRESS': (
            r'\b(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})\b', 
            lambda m: "***.***.***." + m.group(4)
        ),
        'MAC_ADDRESS': (
            r'\b([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})\b', 
            lambda m: "**:**:**:**:**:" + m.group(2)
        ),
        'PHYSICAL_ADDRESS': (
            r'\b(\d+)\s([A-Za-z]+(?:\s[A-Za-z]+)*)\b', 
            lambda m: "*** " + m.group(2)
        )
    }
    
    # Dictionary to store the count of redactions for each PII type
    redaction_count = {pii_type: 0 for pii_type in redacting_patterns.keys()}
    masking_count = {pii_type: 0 for pii_type in masking_patterns.keys()}

    if ARGS.REDACT_OR_MASK == "Redact":
        # Replace identified PII with a placeholder indicating the type of PII
        for pii_type, pattern in redacting_patterns.items():
            content = re.sub(pattern, redact_and_log(pii_type, file_stamp, redaction_count), content)
    else:
        # Mask it
        for pii_type, (pattern, mask_func) in masking_patterns.items():
            content = re.sub(pattern, mask_func, content)

    if ARGS.REDACT_OR_MASK == "Redact":
        # Print or log the counts of each PII type redacted
        for pii_type, count in redaction_count.items():
            logging.info("Total redactions for PII type %s: %d", pii_type, count)
            print(f"Total redactions for PII type {pii_type}: {count}")  
    else:        
        for pii_type, count in masking_count.items():
            logging.info("Total maskings for PII type %s: %d", pii_type, count)
            print(f"Total maskings for PII type {pii_type}: {count}")  

    return content

def redact_and_log(pii_type, file_stamp, redaction_count):
    """
    Returns a function that logs the redaction and replaces the match with a placeholder.
    """
    def replace(match):
        # Log the PII type being redacted with the session ID
        logging.info("Session Id: %s, redacting PII type: %s.", file_stamp, pii_type)
        # Increment the count for the current PII type
        redaction_count[pii_type] += 1
        return f'[REDACTED {pii_type}]'
    return replace


def main():
    """
    Main function to execute PII redaction based on input path.
    """
    redact_pii(ARGS.INP_PATH)

if __name__ == "__main__":
    main()
