import os
from typing import Optional

from ner.highlighter import Highlighter


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


def fscore(y, p) -> Optional[float]:
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


def load_prompt_from_file(fname: str, highlighter: Highlighter) -> (str, set):
    entities = set()
    with open(fname, 'r') as file:
        content = file.read()
    for line in content.split('\n'):
        if line == '':
            continue
        cat = line.split(':')[0]
        if len(line.split(':')) > 1:
            vals = line.split(':')[1].split(',')
        else:
            vals = []
        assert cat in highlighter.categories
        for val in vals:
            if val in highlighter.trie:
                for e in highlighter.trie[val]:
                    if e[1] == cat:
                        val = e[0]
                        break
            entities.add((val, cat))
    return content, entities
