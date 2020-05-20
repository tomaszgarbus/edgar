import argparse
import logging
import os

from tqdm import tqdm

from ner.highlighter import Highlighter
from utils import list_all_files


def build_prompts(input_dir, output_dir, config_path):
    files = list_all_files(input_dir)
    highlighter = Highlighter(config_path)
    logging.info('Building prompts...')
    for f in tqdm(files):
        with open(os.path.join(input_dir, f), 'r') as fp:
            article = fp.read()
        with open(os.path.join(output_dir, f), 'w') as fp:
            fp.write(highlighter.append_prompt_to_article(article))
    logging.info('OK')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', action='store', type=str, required=True,
                        help='Dataset input directory.')
    parser.add_argument('-o', action='store', type=str, required=True,
                        help='Prompted dataset output directory.')
    parser.add_argument('-c', action='store', type=str, required=True,
                        help='Highlighter config file path.')
    args = parser.parse_args()
    build_prompts(args.i, args.o, args.c)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    main()
