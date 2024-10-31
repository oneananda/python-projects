"""
This program contains functions which identifies and redacts Personally Identifiable Information (PII).
"""

import re
import sys, argparse

#INP_PATH = sys.argv[1]
PARSER = argparse.ArgumentParser(description="PII Redacting parameters!")
PARSER.add_argument("INP_PATH",type=str,help="Path of the text file")

ARGS = PARSER.parse_args() 

def redact_pii(given_path):
EMAIL_PATTERN = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
  with open(given_path,'r') as file:
    CONTENT = file.read()
    CONTENT = re.sub(EMAIL_PATTERN, '[REDACTED EMAIL]', CONTENT)
    print(CONTENT)
  return CONTENT

redact_pii(ARGS.INP_PATH)