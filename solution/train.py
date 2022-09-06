import argparse
import pickle
import dill
import sys
import re


def get_text():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", help="directory of text files")
    parser.add_argument("--model", help="directory for model to be saved in")
    args = parser.parse_args()

    if not args.model:
        print('Please, enter the path for model to save')
        exit()

    text = ''
    if args.input_dir:
        text = open(args.input_dir, encoding="utf8").read()
    else:
        print('You dont add path to text files, so type it in stdin.\nWhen you done just print \"eNd_type.\" in a new '
              'line')
        # text = sys.stdin.read()
        for line in sys.stdin:
            if line.rstrip() == 'eNd_type.':
                break
            text += line
    return text, args.model




class Model:
    n_grams = {}

    def __init__(self, n=2):
        self.n = n

    def text_to_tokens(self, text):
        text = text.lower()
        return re.split("[^a-zа-я]+", text)

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

            n_grams[grammar[0]] = [(k, v) for k, v in
                                   sorted(grammar[1].items(), key=lambda item: item[1], reverse=True)]

    def generate(self, start, length):
        ans = start
        tokens = self.text_to_tokens(start)
        prefix = tuple(tokens[-self.n:])

        for i in range(length):
            ans = ans + ' ' + self.n_grams[prefix][0][0]
            prefix = (prefix[-1], self.n_grams[prefix][0][0])
        return ans

    def save(self, model_dir):
        with open(model_dir, 'wb') as model_file:
            dill.dump(self, model_file)



if __name__ == "__main__":
    model = Model()

    rawText, model_dir = get_text()
    tokens = model.text_to_tokens(rawText)

    model.fit(tokens)

    text = model.generate('общее всех', 14)
    print(text)

    model.save(model_dir)
