#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
