"""Busca lexical simples no corpus; não usa embeddings nem consulta DB de produtos."""
from pathlib import Path
from functools import lru_cache
from collections import Counter
import json
import re
import unicodedata

KNOWLEDGE = Path(__file__).resolve().parent.parent / "knowledge"
STOP = set("a o as os um uma para por que qual quais de da do das dos em no na nos nas e com como sem quando onde se ao aos esse essa isso sobre mais meu minha fazer posso esta estar como tem ter qual".split())


def words(text: str) -> list[str]:
    text = unicodedata.normalize('NFKD', text.lower())
    text = ''.join(c for c in text if not unicodedata.combining(c))
    return [t for t in re.findall(r'[a-z0-9]+', text) if len(t) >= 3 and t not in STOP]


@lru_cache(maxsize=1)
def policies() -> list[dict]:
    result = []
    for item in json.loads((KNOWLEDGE / "manifest.json").read_text(encoding="utf-8")):
        text = (KNOWLEDGE / item["file"]).read_text(encoding="utf-8")
        result.append({**item, "content": text, "terms": Counter(words(text)), "tag_terms": set(words(' '.join(item['keywords'])))})
    return result


def search_policies(question: str, limit: int = 3) -> list[dict]:
    query = set(words(question))
    ranked = []
    for item in policies():
        body_hits = sum(min(2, item['terms'][word]) for word in query)
        tag_hits = len(query & item['tag_terms'])
        explicit_id = 100 if item['id'].lower() in question.lower() else 0
        score = body_hits + 4*tag_hits + explicit_id
        if score > 0:
            ranked.append((score, item))
    ranked.sort(key=lambda pair: (-pair[0], pair[1]['id']))
    return [record for _, record in ranked[:limit]]
