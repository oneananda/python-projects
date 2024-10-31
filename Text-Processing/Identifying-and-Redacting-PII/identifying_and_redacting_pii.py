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
    This program contains functions which identifies 
    and redacts Personally Identifiable Information (PII).
    """
    path, file_name = os.path.split(given_path)
    # print("Path:", PATH)       
    # print("Filename:", FILE_NAME)
    content = ""	
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'	
    with open(given_path,"r", encoding="utf-8") as file:
        content = file.read()
    content = re.sub(email_pattern, '[REDACTED EMAIL]', content)
    random_file_name = file_name.replace(".txt",'') +'_'+ str(uuid.uuid4())[0:7]+'.txt'
    with open(path +'\\' + random_file_name, 'w', encoding="utf-8") as file:
        file.write(content)
    return content
redact_pii(ARGS.INP_PATH)
