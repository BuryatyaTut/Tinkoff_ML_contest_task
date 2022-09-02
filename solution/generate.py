import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--model", help="enter the path where model located")
parser.add_argument("--prefix", help="start of sentence: one or more words")
parser.add_argument("--length", help="length of generating model")
args = parser.parse_args()

if not args.model:
    print("Please, enter path where model located")
    exit()

length = 10
if args.length:
    length = args.length

