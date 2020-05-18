import argparse
import logging
import os
from random import shuffle

from ner.highlighter import Highlighter
from utils import list_all_files


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', type=str, action='store',
                        help='input file or directory', required=True)
    parser.add_argument('-c', type=str, action='store',
                        help='config json path', required=True)
    args = parser.parse_args()
    in_path = args.i
    config_path = args.c
    assert os.path.exists(in_path)
    highlighter = Highlighter(config_path)

    if os.path.isfile(in_path):
        files = [in_path]
    else:
        assert os.path.isdir(in_path)
        files = list(map(lambda f: os.path.join(in_path, f),
                         list_all_files(in_path)))
    shuffle(files)
    for f in files:
        with open(f, 'r') as fp:
            article = fp.read()
        print(highlighter.highlight(article))
        print('Press enter to continue...')
        input()


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    main()
