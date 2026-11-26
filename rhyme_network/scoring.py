from __future__ import annotations

from functools import lru_cache
from typing import List

from .phonetics import rhyme_key, stresses_for_word_cached

MAX_STRESS_BONUS = 0.1

def levenshtein_tokens(a: List[str], b: List[str]) -> int:
    la, lb = len(a), len(b)
    dp = [[0]*(lb+1) for _ in range(la+1)]
    for i in range(la+1):
        dp[i][0] = i
    for j in range(lb+1):
        dp[0][j] = j
    for i in range(1, la+1):
        for j in range(1, lb+1):
            cost = 0 if a[i-1] == b[j-1] else 1
            dp[i][j] = min(dp[i-1][j] + 1,
                           dp[i][j-1] + 1,
                           dp[i-1][j-1] + cost)
    return dp[la][lb]

@lru_cache(None)
def base_from_keys(key_a: str, key_b: str) -> float:
    if key_a == key_b:
        return 1.0
    toks_a = key_a.split()
    toks_b = key_b.split()
    if not toks_a or not toks_b:
        toks_a = list(key_a)
        toks_b = list(key_b)
    denom = max(len(toks_a), len(toks_b))
    if denom == 0:
        return 0.0
    d = levenshtein_tokens(toks_a, toks_b)
    return max(0.0, 1.0 - (d / denom))

def stress_bonus(a: str, b: str) -> float:
    sa = stresses_for_word_cached(a)
    sb = stresses_for_word_cached(b)
    if not sa or not sb:
        return 0.0

    spa, spb = sa[0], sb[0]

    def last_primary_idx(s: str) -> int:
        for i in range(len(s)-1, -1, -1):
            if s[i] == '1':
                return i
        return -1

    ia, ib = last_primary_idx(spa), last_primary_idx(spb)
    if ia == -1 or ib == -1:
        return 0.0

    tail_a, tail_b = spa[ia:], spb[ib:]
    return MAX_STRESS_BONUS if tail_a == tail_b else 0.0

def rhyme_strength(a: str, b: str) -> float:
    key_a, conf_a = rhyme_key(a)
    key_b, conf_b = rhyme_key(b)
    if not key_a or not key_b:
        return 0.0

    base = base_from_keys(key_a, key_b)
    bonus = stress_bonus(a, b)
    conf = (conf_a + conf_b) / 2.0
    return max(0.0, min(1.0, (base + bonus) * conf))
