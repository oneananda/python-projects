"""
This program contains functions which identifies 
and redacts Personally Identifiable Information (PII).
"""

import re
import argparse
import os
import uuid

# INP_PATH = sys.argv[1]
PARSER = argparse.ArgumentParser(description="PII Redacting parameters!")
PARSER.add_argument("INP_PATH",type=str,help="Path of the text file")

ARGS = PARSER.parse_args()

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
      with open(given_path, "r", encoding="utf-8") as file:
        content = file.read()
    # Process the content as needed
    except FileNotFoundError:
        print(f"The file at {given_path} was not found.")
    except PermissionError:
        print(f"Permission denied for accessing the file at {given_path}.")
    except UnicodeDecodeError:
        print(f"Could not decode the file at {given_path}. Check the file encoding.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    content = process_content(content)

    random_file_name = file_name.replace(".txt",'') +'_'+ str(uuid.uuid4())[0:7]+'.txt'
    new_file_path = os.path.join(path, random_file_name)
    with open(new_file_path, "w", encoding="utf-8") as file:
        file.write(content)
    print(f"Redacted file saved at {new_file_path}")
    return content

def process_content(content):
    """
    This function processes the content 
    and redacts Personally Identifiable Information (PII).
    """
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    content = re.sub(email_pattern, '[REDACTED EMAIL]', content) 
    return content

redact_pii(ARGS.INP_PATH)
