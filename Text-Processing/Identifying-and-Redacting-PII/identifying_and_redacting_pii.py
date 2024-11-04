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
from masking_functions import mask_function_mapping  # Import the mapping and functions

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
    # Define patterns for redacting
    redacting_patterns = config['patterns']['redacting_patterns']
    # Define patterns and corresponding masking functions
    # masking_patterns = config['patterns']['masking_patterns']

    masking_patterns = {}
    for pii_type, details in config['patterns']['masking_patterns'].items():
        # Compile the pattern and convert the mask function from string to lambda
        pattern = re.compile(details['pattern'])
        mask_func = eval(details['mask_function'])  # Caution: Only use `eval` with trusted sources
        # Safely map function name to actual function
        # print(details['mask_function'])
        # mask_func = details['mask_function']
        # mask_func = mask_function_mapping[details['mask_function']]
        masking_patterns[pii_type] = (pattern, mask_func)

    # Dictionary to store the count of redactions for each PII type
    redaction_count = {pii_type: 0 for pii_type in redacting_patterns}
    masking_count = {pii_type: 0 for pii_type in masking_patterns}

    if ARGS.REDACT_OR_MASK == "Redact":
        # Replace identified PII with a placeholder indicating the type of PII
        for pii_type, pattern in redacting_patterns.items():
            content = re.sub(pattern,
            redact_and_log(pii_type, file_stamp,
            redaction_count), content)
    else:
        # Mask it
        for pii_type, (pattern, mask_func) in masking_patterns.items():
            content = re.sub(pattern,
            mask_and_log(pii_type, file_stamp,
            masking_count, mask_func), content)

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
    def replace(_):
        # Log the PII type being redacted with the session ID
        logging.info("Session Id: %s, redacting PII type: %s.", file_stamp, pii_type)
        # Increment the count for the current PII type
        redaction_count[pii_type] += 1
        return f'[REDACTED {pii_type}]'
    return replace

def mask_and_log(pii_type, file_stamp, masking_count, mask_func):
    """
    Returns a function that logs the masking the match with a placeholder.
    """
    def wrapper(match):
        # Log the PII type being redacted with the session ID
        logging.info("Session Id: %s, masking PII type: %s.", file_stamp, pii_type)
        # Increment the count for the current PII type
        masking_count[pii_type] += 1
        return mask_func(match)
    return wrapper

def main():
    """
    Main function to execute PII redaction based on input path.
    """
    redact_pii(ARGS.INP_PATH)

if __name__ == "__main__":
    main()
