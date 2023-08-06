#!/usr/bin/env python
# -*- coding: utf-8 -*-
from prosecco import Prosecco, Condition, EnglishWordNormalizer

# Read wikipedia https://en.wikipedia.org/wiki/Superhero
with open("superhero.txt") as f:
    text = f.read()

# 1. Create conditions with hero names
conditions = [
    Condition(lemma_type="hero|dc", compare=["batman", "superman", "wonder woman"], lower=True),
    Condition(lemma_type="hero|marvel", normalizer=EnglishWordNormalizer(),
              compare=["spiderman", "iron man", "black panther"], lower=True)
]
# 2. Create prosecco
p = Prosecco(conditions=conditions)
# 3. Let's drink and print output
p.drink(text, progress=True)
lemmas  = set(p.get_lemmas(type="hero"))
print(" ".join(map(str, lemmas)))
print(p.tokenizer.most_common(10))
