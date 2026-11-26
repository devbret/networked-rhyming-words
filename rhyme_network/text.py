from __future__ import annotations

import re
from typing import List, Optional

WORD_RE = re.compile(r"[^\W\d_](?:[^\W\d_]|['’\-])*")

SMART_QUOTES = {
    "‘": "'", "’": "'", "‛": "'",
    "“": '"', "”": '"', "‟": '"',
}

def normalize_smart_quotes(text: str) -> str:
    for k, v in SMART_QUOTES.items():
        text = text.replace(k, v)
    return text

def split_stanzas(text: str) -> List[List[str]]:
    text = text.replace("\r\n", "\n")
    raw = text.split("\n")
    stanzas: List[List[str]] = []
    cur: List[str] = []
    for line in raw:
        if line.strip() == "":
            if cur:
                stanzas.append(cur)
                cur = []
        else:
            cur.append(line)
    if cur:
        stanzas.append(cur)
    return stanzas

def find_last_word(line: str) -> Optional[str]:
    words = WORD_RE.findall(line)
    if not words:
        return None
    return words[-1].lower()
