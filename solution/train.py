import argparse
import os
import random

import dill
import sys
import re


def get_text():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", help="directory of text files")
    parser.add_argument("--model", help="directory for model to be saved in")
    parser.add_argument("--n_grams", help="amount of n in n-grams model")
    args = parser.parse_args()

    if not args.model:
        print('Please, enter the path for model to save')
        exit()

    text = ''
    if args.input_dir:
        for file in os.listdir(args.input_dir):
            text += open(os.path.join(args.input_dir, file), encoding="utf8").read()
    else:
        print('You dont add path to text files, so type it in stdin.\nWhen you done just print \"eNd_type.\" in a new '
              'line')
        # text = sys.stdin.read()
        for line in sys.stdin:
            if line.rstrip() == 'eNd_type.':
                break
            text += line

    n = 2
    if args.n_grams:
        n = int(args.n_grams)

    return text, args.model, n


class Model:
    n_grams = {}

    def __init__(self, n=2):
        self.n = n

    def text_to_tokens(self, text: str):
        text = text.lower()
        return re.split("[^a-zа-я'ё-]+", text)

    def fit(self, data):
        n_grams = self.n_grams

        for i in range(self.n, len(data)):
            key_grams = tuple(data[i - self.n: i])
            if n_grams.get(key_grams) is None:
                n_grams[key_grams] = {data[i]: 1}
            else:
                if n_grams[key_grams].get(data[i]) is None:
                    n_grams[key_grams][data[i]] = 1
                else:
                    n_grams[key_grams][data[i]] += 1

        for grammar in n_grams.items():
            cnt_sum = sum(grammar[1].values())

            for it in grammar[1].items():
                n_grams[grammar[0]][it[0]] = it[1] / cnt_sum

    def generate(self, start, length):
        #n_grams = self.n_grams
        ans = start
        tokens = self.text_to_tokens(start)
        prefix = tuple(tokens[-self.n:])

        for i in range(length):
            if self.n_grams.get(prefix) is None:
                prefix = random.choice(list(self.n_grams.keys()))
            variants = self.n_grams.get(prefix)

            add_word = random.choices(list(variants.keys()), weights=variants.values(), k=1)[0]

            ans = ans + ' ' + add_word
            prefix = (*prefix[-self.n + 1:], add_word)
        return ans

    def save(self, model_dir):
        with open(model_dir, 'wb') as model_file:
            dill.dump(self, model_file)


if __name__ == "__main__":
    rawText, model_dir, n = get_text()

    model = Model(n)

    tokens = model.text_to_tokens(rawText)
    model.fit(tokens)

    #text = model.generate(' '.join(random.choice(list(model.n_grams.keys()))), 1400)
    text = model.generate("твоим бывшим", 500)
    print(text)

    model.save(model_dir)
