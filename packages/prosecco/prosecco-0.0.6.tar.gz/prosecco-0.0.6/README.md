prosecco
====

[![GitHub](https://img.shields.io/github/license/vane/prosecco)](https://github.com/vane/prosecco/blob/master/LICENSE)
[![pypi](https://img.shields.io/pypi/v/prosecco)](https://pypi.org/project/prosecco/)
[![GitHub commits since tagged version](https://img.shields.io/github/commits-since/vane/prosecco/0.0.6)](https://github.com/vane/prosecco/compare/0.0.6...master)
[![GitHub last commit](https://img.shields.io/github/last-commit/vane/prosecco)](https://github.com/vane/prosecco)

  
## Description

NLP engine with text extraction capabilities that can be easily extended to desired needs.

Can be used to build chat bots, question answer machines (see [example/qa.py](https://github.com/vane/prosecco/blob/master/example/qa.py)), text converters.

Extract words or even whole sentences in ordered manner.  
Get position of found text.  
Use ```Condition``` class and mark data using regex or string comparasion.  
Extend each part of it in easy manner. ( see [example/custom_condition_class.py](https://github.com/vane/prosecco/blob/master/example/custom_condition_class.py)).

## Install
```bash
pip install prosecco
```
## Usage

### Basic
[example/basic.py](https://github.com/vane/prosecco/blob/master/example/basic.py)
```python
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
```

### Output
```Batman[hero|dc][start:1089] Wonder Woman[hero|dc][start:2100] Iron Man[hero|marvel][start:2184] Superman[hero|dc][start:2070] Spider-Man[hero|marvel][start:2080] Black Panther[hero|marvel][start:17690]```

### Advanced
[example/advanced.py](https://github.com/vane/prosecco/blob/master/example/advanced.py)
```python
from prosecco import *

text = """Chrząszcz brzmi w trzcinie w Szczebrzeszynie.
Ząb zupa zębowa, dąb zupa dębowa.
Gdzie Rzym, gdzie Krym. W Pacanowie kozy kują.
Tak, jeśli mam szczęśliwy być, to w Gdańsku muszę żyć! 
"""

# 1. Create condition with city names
cities = ["szczebrzeszyn", "pacanow", "gdansk", "rzym", "krym"]
animals = ["koz", "chrzaszcz"]
# 2. Normalizer to remove polish specific charset
n = CharsetNormalizer(Charset.PL_EN)
# 3. Stemmer to remove suffix
s = SuffixStemmer(language="pl")
# 4. Conditions for city and animal
city_condition = Condition(lemma_type="city", compare=cities, normalizer=n, stemmer=s, lower=True)
animal_condition = Condition(lemma_type="animal", compare=animals, normalizer=n, stemmer=s, lower=True)
conditions = [city_condition, animal_condition]
# 5. Create tokenizer for polish charset
tokenizer = LanguageTokenizer(Charset.PL)
# 6. Get list of tokens
tokens = tokenizer.tokenize(text)
# 7. Create visitor with conditions provided in step 1
visitor = Visitor(conditions=conditions)
# 8. Parse tokens based on visitor conditions
lexer = Lexer(tokens=tokens, visitor=visitor)
# 9. Get list of lemmas
lemmas = lexer.lex()
# 10. filter found cities and print output
found = filter(lambda l: l.type == "city", lemmas)
print(" ".join(map(str, found)))
# 11. filter found anumals and print output
found = list(filter(lambda l: l.type == "animal", lemmas))
print(" ".join(map(str, found)))
# 12. print exact words from text
for l in list(found):
    print(text[l.start:l.start+len(l.sentence)])
```   

### Output
```bash
Szczebrzeszynie[city][start:29] Rzym[city][start:86] Krym[city][start:98] Pacanowie[city][start:106] Gdańsku[city][start:163]
Chrząszcz[animal][start:0] kozy[animal][start:116]
Chrząszcz
kozy
```

### QA ( question answer machine )
[example/qa.py](https://github.com/vane/prosecco/blob/master/example/qa.py)
```python
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
```

### Output

```bash
Question :  Whats the time ?
Robot :  2019-08-13 20:38:06.948720
Question :  How long boil egg?
Robot :  
Hard for 9-15 minutes.
Soft for 6-8 minutes.
Question :  100 miles to km
Robot :  160.93440057946685
Question :  30,3 celsius to farenheit
86.53999999999999
```
