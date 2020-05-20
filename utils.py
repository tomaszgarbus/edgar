import json
import logging
import os
from typing import Optional

from jsonschema import validate

from ner.schema import schema as config_schema


def precision(y, p) -> Optional[float]:
    if len(p) != 0:
        return len(p.intersection(y)) / len(p)
    else:
        return None


def recall(y, p) -> Optional[float]:
    if len(y) != 0:
        return len(p.intersection(y)) / len(y)
    else:
        return None


def f1(y, p) -> Optional[float]:
    prec = precision(y, p)
    rec = recall(y, p)
    if prec is not None and rec is not None:
        if prec + rec == 0.:
            return 0.
        else:
            return 2 * prec * rec / (prec + rec)
    else:
        return None


def list_all_files(dir):
    ret = []
    for e in os.listdir(dir):
        if os.path.isfile(os.path.join(dir, e)):
            ret.append(e)
        elif os.path.isdir(os.path.join(dir, e)):
            ret += list(map(lambda f: os.path.join(e, f),
                            list_all_files(os.path.join(dir, e))))
    return ret


def validate_and_load_config(config_path: str):
    with open(config_path, 'r') as fp:
        config = json.load(fp)
    logging.info('Validating JSON schema...')
    validate(instance=config, schema=config_schema)
    if 'case_sensitive' not in config:
        config['case_sensitive'] = True
    return config
