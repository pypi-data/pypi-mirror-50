#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


class Charset:
    """
    Provides information about character set for LanguageTokenizer
    All other characters will be treet as single tokens
    """
    EN = "qwertyuiopasdfghjklzxcvbnm1234567890"
    PL = EN+"ęóąśłżźćń"
    PL_EN = { "ę": "e", "ó": "o", "ą": "a", "ś": "s", "ł": "l", "ż": "z", "ź": "z", "ć": "c", "ń": "n", }


class Token:
    """Tokenise result"""
    def __init__(self, token, end):
        self.token = token
        self.end = end

    def __eq__(self, other):
        return self.token == other

    def __len__(self):
        return len(self.token)

    def __repr__(self):
        return self.token

    def lower(self):
        return self.token.lower()


class Lemma:
    """Base lemma class output for lexer"""
    def __init__(self, type, data, condition, sentence):
        self.type = type
        self.data = data
        self.condition = condition
        self.sentence = sentence
        self.start = self.data[0].end - len(self.data[0])

    @classmethod
    def filter_space(cls, data):
        return list(filter(lambda x: x != " ", data))

    @classmethod
    def build_sentence(self, data, separator=""):
        return separator.join(map(str, data))

    def __repr__(self):
        return "{}[{}][start:{}]".format(self.sentence, self.type, self.start)

    def __eq__(self, other):
        return self.data == other

    def __ne__(self, other):
        return self.data != other

    def __hash__(self):
        # hack for set comparasion - probably need some smarter way to do it
        return 1


class Condition:
    """Base condition class contain compare statement"""
    def __init__(self, lemma_type="skip",
                 compare=None,
                 normalizer=None,
                 stemmer=None,
                 lower=False,
                 regex=False):
        self.lemma_type = lemma_type
        self.lower = lower
        if isinstance(compare, str):
            compare = (compare,)
        self.compare = compare
        self.normalizer = normalizer
        self.stemmer = stemmer
        self.regex = regex
        self.found = None

    def __contains__(self, item):
        if self.lower:
            item = item.lower()
        if self.normalizer:
            item = self.normalizer.normalize(item)
        if self.stemmer:
            words = self.stemmer.stem(item)
            # we got list of words so compare if we found one
            for word in words:
                if self._compare(word):
                    return True
        # comparasion
        return self._compare(item)

    def _compare(self, data):
        for c in self.compare:
            if self.regex and re.match(c, data):
                self.found = c
                return True
            elif c == data:
                self.found = c
                return True
        return False

    def __repr__(self):
        return "|".join(self.compare)
