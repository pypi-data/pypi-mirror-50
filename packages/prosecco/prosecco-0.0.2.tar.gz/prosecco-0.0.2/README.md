prosecco
====

## Description

Slim, flexible and extendable NLP engine that can produce list of features 
from text based on provided condtions.  

## Features
- word categorisation
- feature extraction 

## Download
```bash
pip install prosecco
```
## Usage

```bash
python example.py
```

### or

```python
text = """Chrząszcz brzmi w trzcinie w Szczebrzeszynie.
Ząb zupa zębowa, dąb zupa dębowa.
Gdzie Rzym, gdzie Krym. W Pacanowie kozy kują.
Tak, jeśli mam szczęśliwy być, to w Gdańsku muszę żyć! 
"""

# 1. Create conditions based on city names
cities = ["szczebrzeszyn", "pacanow", "gdansk", "rzym", "krym"]
conditions = []
for city in cities:
    conditions.append(Condition(lemma_type="city",
                                compare=city,
                                normalizer=CharsetNormalizer(Charset.PL_EN),
                                stemmer=WordStemmer(language="pl"),
                                lower=True))
# accept all words
conditions.append(Condition(compare=r".*"))

# 2. Create tokenizer for polish charset
tokenizer = LanguageTokenizer(Charset.PL)
# 3. Get list of tokens
tokens = tokenizer.tokenize(text)
# 4. Create visitor with conditions provided in step 1
visitor = Visitor(conditions=conditions)
# 5. Parse tokens based on visitor conditions
lexer = Lexer(tokens=tokens, visitor=visitor)
# 6. Get list of lemmas
lemmas = lexer.lex()
# 7. filter found cities
found_cities = filter(lambda l: l.type == 'city', lemmas)
# 8. print output
print(" ".join(map(str, found_cities)))
```   

## Output
`Szczebrzeszynie[city] Rzym[city] Krym[city] Pacanowie[city] Gdańsku[city]`
