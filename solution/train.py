import argparse
import sys
import re

parser = argparse.ArgumentParser()
parser.add_argument("--input-dir", help="directory of text files")
parser.add_argument("--model", help="directory for model to be saved in")
args = parser.parse_args()

if not args.model:
    print('Please, enter the path for model to save')
    exit()

text = ''
if args.input_dir:
    text = open(args.input_dir).read()
else:
    print('You dont add path to text files, so type it in stdin.\nWhen you done just print \"eNd_type.\" in a new line')
    for line in sys.stdin:
        if line.rstrip() == 'eNd_type.':
            break
        text += line

# -------------------------- data preprocessing and tokenizing

text = text.lower()
tokens = re.split("[^a-zа-я]+", text)

