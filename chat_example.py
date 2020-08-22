import spacy
import os
import json
from simpleChat import SimpleChat
from time import time_ns as ns

nlp = spacy.load("zh_core_web_md")
sp = SimpleChat(nlp, 0.90)


def main():
    path = os.path.abspath('dialog.json')
    if path is False:
        return

    with open(path) as f:
        json_data = json.load(f)

    i = 1
    for row in json_data:
        if len(row) == 2:
            sp.learn(row[0], row[1])
        i += 1
        if i % 1000 == 0:
            print("load %d lines", i)
        if i > 8000:
            break

    while True:
        say = input('input:')
        start = ns()
        r = sp.reply(say, 0.5)
        end = ns()
        print(r, end - start)


if __name__ == '__main__':
    main()
