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

def redact_pii(given_path):
    """
    This function identifies 
    and redacts Personally Identifiable Information (PII).
    """
    path, file_name = os.path.split(given_path)
    # print("Path:", PATH)
    # print("Filename:", FILE_NAME)
    content = ""

    try:
        with open(given_path, "r", encoding="utf-8") as orginal_file:
            logging.info("Opened file %s for reading.", given_path)
            content = orginal_file.read()
    # Process the content as needed
    except FileNotFoundError:
        print(f"The file at {given_path} was not found.")
    except PermissionError:
        print(f"Permission denied for accessing the file at {given_path}.")
    except UnicodeDecodeError:
        print(f"Could not decode the file at {given_path}. Check the file encoding.")

    content = process_content(content)

    random_file_name = file_name.replace(TEXT_EXT,'') +'_'+ str(uuid.uuid4())[0:7] + TEXT_EXT
    new_file_path = os.path.join(path, random_file_name)
    with open(new_file_path, "w", encoding="utf-8") as processed_file:
        processed_file.write(content)
    print(f"Redacted file saved at {new_file_path}")
    return content

def process_content(content):
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

    if ARGS.REDACT_OR_MASK == "Redact":
        # Replace identified PII with a placeholder indicating the type of PII
        for pii_type, pattern in redacting_patterns.items():
            content = re.sub(pattern, f'[REDACTED {pii_type}]', content)
    else:
        # Mask it
        for pii_type, (pattern, mask_func) in masking_patterns.items():
            content = re.sub(pattern, mask_func, content)

    return content

def main():
    """Main function to execute PII redaction based on input path."""
    redact_pii(ARGS.INP_PATH)

if __name__ == "__main__":
    main()
