from __future__ import annotations

from functools import lru_cache
from typing import Optional, Tuple

import pronouncing

@lru_cache(None)
def phones_for_word_cached(word: str) -> Tuple[str, ...]:
    return tuple(pronouncing.phones_for_word(word))

@lru_cache(None)
def rhyming_part_cached(phones: str) -> Optional[str]:
    try:
        return pronouncing.rhyming_part(phones)
    except Exception:
        return None

@lru_cache(None)
def stresses_for_word_cached(word: str) -> Tuple[str, ...]:
    return tuple(pronouncing.stresses(word))

@lru_cache(None)
def rhymes_cached(word: str) -> Tuple[str, ...]:
    return tuple(pronouncing.rhymes(word))

def basic_stem(word: str) -> str:
    if word.endswith("'s"):
        return word[:-2]
    if word.endswith("’s"):
        return word[:-2]
    if word.endswith("es") and len(word) > 3:
        return word[:-2]
    if word.endswith("s") and len(word) > 2:
        return word[:-1]
    return word

def crude_orthographic_rhyme_key(word: str) -> str:
    w = word.lower()
    vowels = "aeiouy"
    last_vowel_idx = -1
    for i in range(len(w) - 1, -1, -1):
        if w[i] in vowels:
            last_vowel_idx = i
            break
    if last_vowel_idx == -1:
        return w[-3:] if len(w) >= 3 else w
    return w[last_vowel_idx:]

@lru_cache(None)
def rhyme_key(word: str) -> Tuple[Optional[str], float]:
    phones = phones_for_word_cached(word)
    if phones:
        key = rhyming_part_cached(phones[0])
        if key:
            return key, 1.0

    w2 = basic_stem(word)
    if w2 != word:
        phones2 = phones_for_word_cached(w2)
        if phones2:
            key2 = rhyming_part_cached(phones2[0])
            if key2:
                return key2, 0.8

    return crude_orthographic_rhyme_key(w2), 0.3
