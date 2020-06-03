import logging
from typing import List, Tuple, Optional, Set, Union

import numpy as np
from tqdm import tqdm

from ner.highlighter import Highlighter


def _evaluate_category(predictions: Union[
                           List[Set[Tuple[str, str]]],
                           List[Set[Tuple[int, int, str]]],
                       ],
                       ground_truths: Union[
                           List[Set[Tuple[str, str]]],
                           List[Set[Tuple[int, int, str]]],
                       ],
                       category_name: Optional[str]) -> None:
    """
    :param predictions: Predictions, expressed as sets of pairs
                        (base entity name, category name).
    :param ground_truths: Ground truths in the same format.
    :param category_name: If None, all categories are evaluated jointly.
    :return: Nothing, outputs evaluation metrics to std.
    """
    precs = []
    recs = []
    f1s = []
    for y, p in list(zip(ground_truths, predictions)):
        if category_name is not None:
            y = set(filter(lambda a: a[-1] == category_name, y))
            p = set(filter(lambda a: a[-1] == category_name, p))
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
             entity_sets: Union[
                 List[Set[Tuple[str, str]]],
                 List[Set[Tuple[int, int, str]]],
             ], mode='default') -> None:
    """
    :param hl: Highlighter object put under test.
    :param texts: Evaluation dataset.
    :param entity_sets: Ground truths for each text, expressed as sets
                        of pairs (base entity name, category name).
    :param mode: Entity representation mode. 'default' or 'spacy'
    :return: Nothing, outputs evaluation metrics to std.
    """
    assert len(entity_sets) == len(texts)
    categories = set()
    for es in entity_sets:
        for e in es:
            categories.add(e[-1])
    logging.info('Computing predictions...')
    preds = []
    for text in tqdm(texts):
        preds.append(hl.extract_entities_from_article(text, mode=mode))
    logging.info('OK')
    for category in list(categories) + [None]:
        _evaluate_category(preds, entity_sets, category)
