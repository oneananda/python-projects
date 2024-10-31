"""
This program contains functions which identifies 
and redacts Personally Identifiable Information (PII).
"""

import re
import sys, argparse, os, uuid

# INP_PATH = sys.argv[1]
PARSER = argparse.ArgumentParser(description="PII Redacting parameters!")
PARSER.add_argument("INP_PATH",type=str,help="Path of the text file")

ARGS = PARSER.parse_args()

def redact_pii(given_path):    
	PATH, FILE_NAME = os.path.split(given_path)

	# print("Path:", PATH)       
	# print("Filename:", FILE_NAME)
	
	EMAIL_PATTERN = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
	
	with open(given_path,'r') as file:
	    CONTENT = file.read()
	CONTENT = re.sub(EMAIL_PATTERN, '[REDACTED EMAIL]', CONTENT)
	RANDOM_FILE_NAME = FILE_NAME.replace(".txt",'') +'_'+ str(uuid.uuid4())[0:7]+'.txt'

	with open(PATH +'\\' + RANDOM_FILE_NAME, 'w') as file :
	    file.write(CONTENT)
	# print(RANDOM_FILE_NAME)

    return CONTENT

redact_pii(ARGS.INP_PATH)
