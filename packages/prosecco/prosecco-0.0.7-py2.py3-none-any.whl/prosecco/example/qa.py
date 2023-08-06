#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
from prosecco import Prosecco, Condition, EnglishWordNormalizer, SuffixStemmer


messages = """Whats the time ?
How long boil egg?
100 miles to km
30,3 celsius to farenheit"""

# create conditions
question = ("what", "whats", "how")
measure = ("celsius", "farenheit", "mile", "km", "kilometer", "time", "long")
cooking = ("boil","cook", "fry")
food = ("egg",)
conditions = [
    Condition(lemma_type="question", compare=question, normalizer=EnglishWordNormalizer(), lower=True),
    Condition(lemma_type="measure", compare=measure,
              normalizer=EnglishWordNormalizer(),
              stemmer=SuffixStemmer(language="en"),
              lower=True),
    Condition(lemma_type="cooking", compare=cooking, normalizer=EnglishWordNormalizer(), lower=True),
    Condition(lemma_type="food", compare=food,
              normalizer=EnglishWordNormalizer(),
              stemmer=SuffixStemmer(language="en"),
              lower=True),
    Condition(lemma_type="number", compare=r"\d+([\.\,]\d+)?", regex=True, until_character=" "),
]

def printer(data):
    print("Robot : ", data)

# time condition
def resolve_time(p):
    printer(datetime.now())

# cooking condition
def resolve_cooking(p):
    if check_condition(p.get_lemmas("cooking|food"), ["boil", "egg"]):
        printer("""
Hard for 9-15 minutes.
Soft for 6-8 minutes.""")
        return True

def resolve_measure(p):
    measures = p.get_lemmas("measure")
    fr = measures[0]
    to = measures[1]
    numbers = p.get_lemmas("number")
    if len(numbers) == 0:
        printer("No number for conversion provided")
        return True
    value = float(numbers[0].sentence.replace(",", "."))
    if fr.condition == "mile" and to.condition == "km":
        printer(value / 0.62137119)
        return True
    elif fr.condition == "km" and to.condition == "mile":
        printer(value * 0.62137119)
        return True
    elif fr.condition == "celsius" and to.condition == "farenheit":
        print(9/5 * value + 32)
        return True
    elif fr.condition == "farenheit" and to.condition == "celsius":
        print((value - 32) * 5/9)
        return True
    return False

def check_condition(lemmas, conditions):
    for l in lemmas:
        for c in conditions:
            if l.condition == c:
                conditions.remove(c)
    return len(conditions) == 0

def resolve(p, m):
    if len(p.get_lemmas("question")) > 0:
        if check_condition(p.get_lemmas("measure"), ["time"]):
            resolve_time(p)
            return True
        elif len(p.get_lemmas("cooking")) > 0:
            return resolve_cooking(p)
    elif len(p.get_lemmas("measure")) > 0:
        return resolve_measure(p)
    return False

for m in messages.split('\n'):
    print("Question : ", m)
    p = Prosecco(conditions=conditions)
    p.drink(m)
    if not resolve(p, m):
        print("Unsupported resolver : ", p.lemmas)
