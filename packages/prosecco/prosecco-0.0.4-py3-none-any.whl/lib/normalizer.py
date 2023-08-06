#!/usr/bin/env python
# -*- coding: utf-8 -*-


class CharsetNormalizer:
    def __init__(self, charset):
        self.charset = charset

    def normalize(self, word):
        out = ""
        for character in word:
            if character in self.charset:
                if character.istitle():
                    character = self.charset[character].upper()
                else:
                    character = self.charset[character]
            out += character
        return out


class EnglishWordNormalizer:
    def normalize(self, word):
        return word.replace("-", "").replace("'", "")
