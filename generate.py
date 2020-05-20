from typing import Set, Tuple

import tensorflow as tf

import gpt_2_simple.gpt_2 as gpt2
from ner.highlighter import Highlighter
from utils import f1


def generate(prompt: str, hl: Highlighter,
             entity_set: Set[Tuple[str, str]], model_name='355M',
             multi_gpu=False,
             model_dir='gpt_2_simple/models',
             checkpoint_dir='gpt_2_simple/checkpoints',
             steps: int = 5, step_length: int = 20,
             samples_per_step: int = 20):
    sess = gpt2.start_tf_sess()

    gpt2.load_gpt2(sess, checkpoint_dir=checkpoint_dir,
                   model_name=model_name, multi_gpu=multi_gpu,
                   model_dir=model_dir)

    text = prompt
    for _ in range(steps):
        variants = gpt2.generate(sess,
                                 checkpoint_dir=checkpoint_dir,
                                 model_name=model_name,
                                 model_dir=model_dir,
                                 return_as_list=True,
                                 nsamples=samples_per_step,
                                 length=step_length,
                                 prefix=text)
        variants = list(map(
            lambda v: (f1(entity_set, hl.extract_entities_from_article(v)), v),
            variants))
        variants = list(map(lambda v: (0. if v[0] is None else v[0], v[1]),
                            variants))
        variants.sort(reverse=True)
        text = variants[0][1]

    tf.reset_default_graph()
    sess.close()

    return text
