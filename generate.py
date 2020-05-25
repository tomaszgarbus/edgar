import argparse
import logging
from random import shuffle
from typing import Set, Tuple

import tensorflow as tf
from tqdm import tqdm

import gpt_2_simple.gpt_2 as gpt2
from ner.highlighter import Highlighter
from utils import fscore, list_all_files, load_prompt_from_file
import os


def generate(prompt: str, hl: Highlighter,
             entity_set: Set[Tuple[str, str]], input_dir: str,
             multi_gpu=False,
             checkpoint_dir='gpt_2_simple/checkpoints',
             steps: int = 5, step_length: int = 20,
             samples_per_step: int = 5):
    sess = gpt2.start_tf_sess()

    gpt2.load_gpt2(sess, checkpoint_dir=checkpoint_dir, multi_gpu=multi_gpu,
                   run_name=(os.path.dirname(input_dir) or input_dir))

    text = prompt
    for _ in range(steps):
        variants = gpt2.generate(sess,
                                 checkpoint_dir=checkpoint_dir,
                                 return_as_list=True,
                                 nsamples=samples_per_step,
                                 length=step_length,
                                 include_prefix=True,
                                 prefix=text,
                                 truncate='<|endoftext|>',
                                 run_name=(os.path.dirname(input_dir) or input_dir))
        variants = list(map(
            lambda v: (fscore(entity_set, hl.extract_entities_from_article(v[len(prompt):])), v),
            variants))
        variants = list(map(lambda v: (0. if v[0] is None else v[0], v[1]),
                            variants))
        variants.sort(reverse=True)
        text = variants[0][1]
        logging.debug(variants[0][0])

    tf.reset_default_graph()
    sess.close()

    return text


def main():
    parser = argparse.ArgumentParser(
        prog='Generate samples from finetuned model.')
    parser.add_argument('-i', action='store', type=str, required=True,
                        help='Input directory you have used to train the model.')
    parser.add_argument('-c', action='store', type=str, required=True,
                        help='Highlighter config. Refer to ner/schema.py for the JSON schema definition.')
    parser.add_argument('-p', action='store', type=str, required=True,
                        help='Prompts source directory.')
    parser.add_argument('-o', action='store', type=str, required=True,
                        help='Output directory for samples.')
    parser.add_argument('--steps', action='store', type=int, default=5,
                        help='Number of generation steps.')
    parser.add_argument('--step_length', action='store', type=int, default=20,
                        help='Number of tokens generated at each step.')
    parser.add_argument('--samples_per_step', action='store', type=int,
                        default=5, help='Number of samples to select from at each step.')
    parser.add_argument('--multi-gpu', action='store_true',
                        help='Whether or not to  use multiple GPU cores. '
                             'This may be useful if you have an Tesla K80.')
    parser.add_argument('--limit', action='store', type=int,
                        help='Maximum number of samples to generate.')
    args = parser.parse_args()
    files = list_all_files(args.i)
    shuffle(files)
    if args.limit:
        files = files[:args.limit]
    # Initialize Highlighter.
    hl = Highlighter(args.c)
    # Run generation loop.
    for f in tqdm(files):
        prompt, entity_set = load_prompt_from_file(os.path.join(args.i, f),
                                                   hl)
        out = generate(prompt, hl, entity_set, args.i, multi_gpu=args.multi_gpu,
                       steps=args.steps, step_length=args.step_length,
                       samples_per_step=args.samples_per_step)
        out_path = os.path.join(args.o, f)
        os.makedirs(out_path, exist_ok=True)

        f_score = fscore(entity_set,
                         hl.extract_entities_from_article(out[len(prompt):]))
        logging.info('F-Score: %f' % f_score)
        
        with open(out_path, 'w') as fp:
            fp.write(out)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    main()
