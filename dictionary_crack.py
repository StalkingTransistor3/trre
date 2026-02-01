#!/usr/bin/env python3
"""
Dictionary-based Terraria Seed Cracker
"""

import bcrypt
import re
import itertools

TARGETS = {
    "hallowOnTheSurface": "KYvKIk2LK0oyNY86m+uPhKQ7QbzFmDsRpo",
    "portalGunInChests": "ALdQZ+bxQA4VdfjVfdhO/sm9q3sZD9dJ",
    "dualDungeons": "ypBuvKpqKay//OvhG2COriSpGT7f4YY3",
}

STD_BASE64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
BCRYPT_BASE64 = "./ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"

def bcrypt_b64_to_std_b64(s):
    trans = str.maketrans(BCRYPT_BASE64, STD_BASE64)
    return s.translate(trans)

def std_b64_to_bcrypt_b64(s):
    trans = str.maketrans(STD_BASE64, BCRYPT_BASE64)
    return s.translate(trans)

SALT_STD_B64 = "fT2JQQzNMJl2NRoMbo9RjA=="
SALT_BCRYPT_B64 = std_b64_to_bcrypt_b64(SALT_STD_B64.rstrip("="))
BCRYPT_SALT = f"$2a$04${SALT_BCRYPT_B64}"

def normalize_seed(seed):
    return re.sub(r'[^a-z0-9]', '', seed.lower())

def check_seed(seed):
    normalized = normalize_seed(seed)
    if not normalized:
        return None

    hashed = bcrypt.hashpw(normalized.encode('utf-8'), BCRYPT_SALT.encode('utf-8'))
    hash_str = hashed.decode('utf-8')
    hash_portion = hash_str[29:]
    hash_std = bcrypt_b64_to_std_b64(hash_portion)

    for effect, target in TARGETS.items():
        min_len = min(len(hash_std), len(target))
        if hash_std[:min_len] == target[:min_len]:
            return effect

    return None

# Load words
with open('/home/user/trre/words.txt', 'r') as f:
    words = [line.strip() for line in f if line.strip()]

print(f"Loaded {len(words)} words")
print(f"BCrypt salt: {BCRYPT_SALT}")

found = {}
count = 0

# Single words
print("\n=== Single words ===")
for word in words:
    result = check_seed(word)
    count += 1
    if result:
        print(f"*** FOUND: {result} = '{word}' ***")
        found[result] = word

# Two word combinations (space separated)
print("\n=== Two-word phrases ===")
top_words = words[:500]  # Use top 500 words for combinations
for w1, w2 in itertools.product(top_words, repeat=2):
    seed = f"{w1} {w2}"
    result = check_seed(seed)
    count += 1
    if count % 50000 == 0:
        print(f"Progress: {count}")
    if result:
        print(f"*** FOUND: {result} = '{seed}' ***")
        found[result] = seed

# Three word combinations with important words
print("\n=== Three-word phrases with key words ===")
key_words = ["the", "a", "on", "in", "at", "for", "to", "of", "with", "is", "are", "and", "or"]
game_words = ["hallow", "surface", "portal", "gun", "chest", "dual", "dungeon", "holy", "sacred", "double", "twin"]
for w1 in game_words:
    for w2 in key_words:
        for w3 in words[:200]:
            seed = f"{w1} {w2} {w3}"
            result = check_seed(seed)
            count += 1
            if result:
                print(f"*** FOUND: {result} = '{seed}' ***")
                found[result] = seed

print(f"\n=== RESULTS (checked {count} candidates) ===")
for effect, seed in found.items():
    print(f"{effect}: {seed}")

remaining = set(TARGETS.keys()) - set(found.keys())
if remaining:
    print(f"\nNot found: {remaining}")
