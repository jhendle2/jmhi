import json

KEYWORDS = json.load(open('keywords.json'))['keywords']
MISC = json.load(open('keywords.json'))['misc']

BULLETS = MISC['bullets']


def resolve_keyword(keyword):
    if keyword in KEYWORDS.keys():
        return KEYWORDS[keyword]
    else:
        return ''
