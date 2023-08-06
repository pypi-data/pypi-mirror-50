#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Simple, extendable nlp engine that can extract data based on provided conditions.
"""

__version__ = "0.0.6"
import os
import os.path
import sys
import re
import collections
from .model import *
from .normalizer import *


# -------------
# Stemmer
# -------------
class SuffixStemmer:
    """
    Base class for stemming words
    Return tuple of stemmed outputs
    """
    def __init__(self, language, path=None):
        self.language = language
        self.stemwords = ()
        if path is None:
            subpath = os.sep.join(os.path.dirname(__file__).split(os.sep)[:-1])
            path = subpath+"/data/{}/suffix.txt".format(language)
        with open(path) as f:
            # read file strip \n sort by length and save as tuple
            w = [w.strip() for w in f.readlines()]
            w.sort(key=len)
            self.stemwords = tuple(w)

    def stem(self, word):
        stem_list = []
        for s in self.stemwords:
            if word.endswith(s):
                stem_list.append(word[:-len(s)])
        return tuple(stem_list)


# -------------
# Tokenzier
# -------------
class LanguageTokenizer:
    """Tokenize string of data to array of tokens"""
    def __init__(self, charset):
        self.charset = charset
        self.charset_counter = collections.Counter()
        self.char_counter = collections.Counter()
        self.tokens = []

    def tokenize(self, text):
        partial = ""
        for i, character in enumerate(text):
            # pick
            if character.lower() in self.charset:
                partial += character
            else:
                if len(partial) > 0:
                    self.append(partial, i)
                    partial = ""
                self.append(character, i, False)
        if len(partial) > 0:
            self.append(partial, i)
        return self.tokens

    def append(self, data, index, charset=True):
        if charset:
            self.charset_counter[data.lower()] += 1
        else:
            self.char_counter[data.lower()] += 1
        self.tokens.append(Token(token=data, end=index-1))

    def most_common(self, n, charset=True):
        if charset:
            return self.charset_counter.most_common(n)
        return self.char_counter.most_common(n)

# -------------
# Lexer / Visitor
# -------------
class Visitor:
    """
    Utility class for Lexer that use Condition class to check wheather
    we add Lemma to Lexer output or process list of tokens further
    """
    def __init__(self, conditions, empty=True, auto_space=False, num_words=10):
        self.conditions = conditions
        # empty lexer token list
        self.empty = empty
        self.auto_space = auto_space
        self.lemma = None
        self.prev = None
        self.num_words = num_words

    def __contains__(self, item):
        # get items of size num_words
        token_list, next_token = item
        item_copy = token_list[-self.num_words:]
        while len(item_copy) > 0:
            # make sentence from list of item
            if self.auto_space:
                data = Lemma.filter_space(item_copy)
                sentence = Lemma.build_sentence(data, separator=" ")
            else:
                sentence = Lemma.build_sentence(item_copy)
            # check sentence against conditions
            for condition in self.conditions:
                if (sentence, next_token) in condition:
                    self.lemma = Lemma(type=condition.lemma_type,
                                       data=item_copy[:],
                                       condition=condition.found,
                                       sentence=sentence,
                                       prev=self.prev)
                    if self.prev is not None:
                        self.prev.next = self.lemma
                    self.prev = self.lemma
                    return True
            item_copy.pop(0)
        return False


class Lexer:
    """
    Converts list of tokens based on conditions in LexVisitor
    """
    def __init__(self, tokens, visitor):
        self.tokens = tokens
        self.visitor = visitor

    def lex(self, progress=False):
        lemma_list = []
        token_list = []
        last_index = len(self.tokens) - 1
        for i, token in enumerate(self.tokens):
            token_list.append(token)
            if i != last_index:
                next_token = self.tokens[i+1]
            else:
                next_token = None
            if (token_list, next_token) in self.visitor:
                lemma_list.append(self.visitor.lemma)
                if self.visitor.empty:
                    token_list = []
            if progress:
                sys.stdout.write("\r{}%".format(int(i/len(self.tokens)*100)))
        return lemma_list


# -------------
# Prosecco
# -------------
class Prosecco:
    """Let's drink"""
    def __init__(self, charset=Charset.EN, conditions=None, num_words=10):
        conditions = conditions or [Condition(compare=r".*")]
        # custom
        self.lemmas = None
        self.tokenizer = LanguageTokenizer(charset)
        self.visitor = Visitor(conditions=conditions, num_words=num_words)

    def drink(self, text, progress=False):
        self.tokenizer.tokenize(text)
        self.lexer = Lexer(tokens=self.tokenizer.tokens, visitor=self.visitor)
        self.lemmas = self.lexer.lex(progress=progress)
        return self.lemmas[:]

    def get_lemmas(self, type):
        return [l for l in self.lemmas if re.match(type, l.type)]
