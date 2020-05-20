from typing import List, Tuple, Optional, Set

import numpy as np

from ner.highlighter import Highlighter


def _evaluate_category(hl: Highlighter, texts: List[str],
                       entity_sets: List[Set[Tuple[str, str]]],
                       category_name: Optional[str]) -> None:
    precs = []
    recs = []
    f1s = []
    for ground_truth, text in zip(entity_sets, texts):
        pred = hl.extract_entities_from_article(text)
        y = ground_truth
        p = pred
        if category_name is not None:
            y = set(filter(lambda a: a[1] == category_name, y))
            p = set(filter(lambda a: a[1] == category_name, p))
            if len(y) != 0:
                rec = len(p.intersection(y)) / len(y)
                recs.append(rec)
            if len(p) != 0:
                prec = len(p.intersection(y)) / len(p)
                precs.append(prec)
            if len(y) != 0 and len(p) != 0:
                if prec + rec == 0.:
                    f1 = 0.
                else:
                    f1 = 2 * prec * rec / (prec + rec)
                f1s.append(f1)
    if category_name is not None:
        print('Category \"%s\":' % category_name)
    else:
        print('All categories:')
    print('avg F1: %f, avg precision: %f, avg recall: %f' % (
        float(np.mean(f1s)), float(np.mean(precs)), float(np.mean(recs))
    ))


def evaluate(hl: Highlighter, texts: List[str],
             entity_sets: List[Set[Tuple[str, str]]]) -> None:
    """
    :param hl: Highlighter object put under test.
    :param texts: Evaluation dataset.
    :param entity_sets: Ground truths for each text, expressed as sets
                        of pairs (base entity name, category name).
    :return: Nothing, outputs evaluation metrics to std.
    """
    assert len(entity_sets) == len(texts)
    categories = set()
    for es in entity_sets:
        for e in es:
            categories.add(e[1])
    for category in list(categories) + [None]:
        _evaluate_category(hl, texts, entity_sets, category)
