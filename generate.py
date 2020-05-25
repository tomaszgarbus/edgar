import logging
from typing import Set, Tuple

import tensorflow as tf

import gpt_2_simple.gpt_2 as gpt2
from ner.highlighter import Highlighter
from utils import fscore
import os


def generate(prompt: str, hl: Highlighter,
             entity_set: Set[Tuple[str, str]], input_dir: str,
             model_name='355M',
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
        print('f1: ', variants[0][0])

    tf.reset_default_graph()
    sess.close()

    return text