import argparse
import logging
import os

import gpt_2_simple.gpt_2 as gpt2


def finetune(model_name, input_dir,
             num_steps=4000,
             multi_gpu=False,
             model_dir='gpt_2_simple/models',
             checkpoint_dir='gpt_2_simple/checkpoints'):
    sess = gpt2.start_tf_sess()

    os.makedirs(model_dir, exist_ok=True)
    if not os.path.isdir(os.path.join(model_dir, model_name)):
        logging.info('Downloading model...')
        gpt2.download_gpt2(model_dir=model_dir,
                           model_name=model_name)
        logging.info('OK')
    else:
        gpt2.load_gpt2(sess, model_name=model_name, model_dir=model_dir)

    logging.info('Finetuning model...')
    gpt2.finetune(sess,
                  dataset=input_dir,
                  model_name=model_name,
                  model_dir=model_dir,
                  steps=num_steps,
                  multi_gpu=multi_gpu,
                  checkpoint_dir=checkpoint_dir,
                  run_name=os.path.dirname(input_dir)
                  )
    logging.info('Finetuning finished')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', action='store', type=str, required=True,
                        help='Input corpus directory.')
    parser.add_argument('--num_steps', action='store', type=int,
                        default=4000)
    parser.add_argument('--model_name', action='store', type=str,
                        default='355M',
                        choices=['124M', '355M', '774M', '1558M'],
                        help='Name of the finetuned model to use. '
                             'Note that most likely you don\'t have enough '
                             'computing power to use 1558M or 774M.')
    parser.add_argument('--multi-gpu', action='store_true',
                        help='Whether or not to  use multiple GPU cores. '
                             'This may be useful if you have an Tesla K80.')
    args = parser.parse_args()
    finetune(model_name=args.model_name,
             input_dir=args.i,
             num_steps=args.num_steps,
             multi_gpu=args.multi_gpu)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    main()
