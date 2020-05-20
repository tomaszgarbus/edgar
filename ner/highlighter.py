import logging
from collections import defaultdict
from typing import Tuple, Callable

import pygtrie
from tqdm import tqdm

from utils import validate_and_load_config


class Highlighter:
    DEFAULT_CODE = '\033[0;37;40m'

    def __init__(self,
                 config_path: str):
        logging.info('Initializing Highlighter...')
        config = validate_and_load_config(config_path)
        self.categories = [c['name'] for c in config['categories']]
        self.case_sensitive = config['case_sensitive']
        logging.info('Building trie...')
        self.trie = pygtrie.Trie()
        for category in config['categories']:
            logging.info('Adding category %s...' % category['name'])
            for entity in tqdm(category['entities']):
                variants = entity['variants']
                variants = set(variants + [entity['name']])
                for variant in variants:
                    key = variant if self.case_sensitive else variant.lower()
                    if key not in self.trie:
                        self.trie[key] = []
                    self.trie[key].append((entity['name'], category['name']))
        logging.info('Highlighter initialization finished.')

        self._init_colors()

    def _init_colors(self):

        def random_colors(num=1):
            assert num >= 1
            colors = [
                31,  # red
                32,  # green
                33,  # yellow
                34,  # blue
                35,  # purple
                36,  # cyan
            ]
            modifiers = [
                4,  # underlined
                0,  # normal
                1,  # bold or light
                5,  # blinking
            ]
            res = []
            for mod in modifiers:
                for col in colors:
                    res.append('\033[%d;%d;40m' % (mod, col))
                    if len(res) == num:
                        break
            return res

        self.color_codes = dict(zip(self.categories,
                                    random_colors(len(self.categories))))

    @staticmethod
    def run(article,
            handle_entity: Callable[[Tuple[int, int], str, Tuple[str, str]], str],
            trie: pygtrie.Trie,
            match_case=True):
        """
        handle_entity  is a function that takes as arguments:
        * matched pattern range in text
        * matched pattern as string
        * resolved entity (base name, category name)
        and returns a single string, to replace the pattern. Example string
        values to return:
        * the same string, if you only want to process the detected entity but
          not alter the article
        * a placeholder
        * same string, but highlighted
        """
        ret = ""
        i = 0
        mentioned_entities = set()
        resolutions = dict()

        def subtrie(s):
            return trie.has_subtrie(s if match_case else s.lower())

        def in_trie(s):
            return (s if match_case else s.lower()) in trie

        while i < len(article):
            max_found = -1
            j = i
            while j < len(article) and (
                    subtrie(article[i:j + 1]) or in_trie(article[i:j + 1])):
                if in_trie(article[i:j + 1]) and (
                        j + 1 == len(article) or not article[j + 1].isalpha()):
                    max_found = j + 1
                j += 1
            if max_found != -1:
                entity_val = None
                if article[i:max_found] in resolutions:
                    entity_val = resolutions[article[i:max_found]]
                else:
                    for v in trie[article[i:max_found]]:
                        entity_val = v
                        if v in mentioned_entities:
                            break
                ret += handle_entity((i, max_found), article[i:max_found],
                                     entity_val)
                mentioned_entities.add(entity_val)
                resolutions[article[i:max_found]] = entity_val
                i = max_found
            else:
                ret += article[i]
                i += 1
        return ret

    def extract_entities_from_article(self, article: str):
        entities = set()

        def _get_code_default(ignored_where, pattern, entity):
            entities.add(entity)
            return pattern

        self.run(article, _get_code_default, self.trie)
        return entities

    def build_prompt(self, article: str):
        entities_list = self.extract_entities_from_article(article)
        entities = defaultdict(list)
        for entity in entities_list:
            entities[entity[1]].append(entity[0])

        prompt = ''
        for cat in self.categories:
            prompt += cat + ':' + ','.join(entities[cat]) + '\n'
        return prompt

    def append_prompt_to_article(self, article: str):
        return self.build_prompt(article) + article

    def highlight(self, article: str) -> str:
        """
        Highlights player and team in the article using linux prompt
        colors.
        """
        def code_fun(_, s, v):
            return (self.color_codes[v[1]] + s + (' (' + v[0] + ')' if s != v[0]
                                                  else '')
                    + self.DEFAULT_CODE)

        return self.run(article, code_fun, self.trie)
