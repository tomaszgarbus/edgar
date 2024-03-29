import argparse
import logging
import os

from tqdm import tqdm

from ner.highlighter import Highlighter
from utils import list_all_files


def build_prompts(input_path, output_dir, config_path, limit=None):
    highlighter = Highlighter(config_path)
    logging.info('Building prompts...')
    os.makedirs(output_dir, exist_ok=True)
    if os.path.isdir(input_path):
        files = list_all_files(input_path)
        if limit is not None:
            files = files[:limit]
        for f in tqdm(files):
            with open(os.path.join(input_path, f), 'r') as fp:
                article = fp.read()
            with open(os.path.join(output_dir, f), 'w') as fp:
                fp.write(highlighter.append_prompt_to_article(article))
    elif os.path.isfile(input_path):
        with open(input_path, 'r') as fp:
            lines = list(fp.readlines())
        if limit is not None:
            lines = lines[:limit]
        for article in tqdm(lines):
            outfile = os.path.join(output_dir,
                                   str(len(os.listdir(output_dir))))
            with open(outfile, 'w+') as fp:
                fp.write(highlighter.append_prompt_to_article(article))
    else:
        raise FileNotFoundError()
    logging.info('OK')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', action='store', type=str, required=True,
                        help='Dataset input file directory.')
    parser.add_argument('-o', action='store', type=str, required=True,
                        help='Prompted dataset output directory.')
    parser.add_argument('-c', action='store', type=str, required=True,
                        help='Highlighter config file path.')
    parser.add_argument('--limit', action='store', type=int, required=False,
                        help='Limit of output files. Use this parameter if '
                             'you want the script to run for a shorter time.')
    args = parser.parse_args()
    build_prompts(args.i, args.o, args.c, args.limit)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    main()
