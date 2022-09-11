import argparse
import random
import dill
import re


def get_args():
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

    prefix = ''
    if args.prefix:
        prefix = args.prefix

    return args.model, int(length), prefix


def load(model_dir):
    with open(model_dir, 'rb') as model_file:
        model = dill.load(model_file)
        return model


if __name__ == "__main__":
    model_dir, length, prefix = get_args()
    model = load(model_dir)

    if prefix == '':
        prefix = ' '.join(random.choice(list(model.n_grams.keys())))

    text = model.generate(prefix, length)
    print(text)
