"""A demo script highlighting articles and displaying them to console."""
import os
import random
import argparse


from tqdm import tqdm
from trans import trans

from ner.highlighter import Highlighter

DATA_DIR = '../data/bbcsport'
LANGUAGE = 'en'


def run(hl: Highlighter):
    dirs = os.listdir(DATA_DIR)
    random.shuffle(dirs)
    for dir in tqdm(dirs):
        if not os.path.isdir(os.path.join(DATA_DIR, dir)):
            continue
        for fname in os.listdir(os.path.join(DATA_DIR, dir))[:1]:
            fpath = os.path.join(DATA_DIR, dir, fname)
            with open(fpath, 'r') as file:
                content = file.read()
            content = trans(content)
            content = hl.highlight(content)
            # content = hl.placehold_with_id(content)
            print(content)
            input()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Highlighter demo')
    parser.add_argument('--pl', action='store_true', required=False,
                        help='input directory')
    args = parser.parse_args()
    if args.pl:
        DATA_DIR = '../data/sportpl'
        LANGUAGE = 'pl'
    h = Highlighter(language=LANGUAGE)
    run(h)
