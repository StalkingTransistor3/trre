#!/usr/bin/env python3
"""
Verify specific seeds against target hashes
"""

import bcrypt
import re

# Target hashes (in standard base64 format)
TARGETS = {
    "hallowOnTheSurface": "KYvKIk2LK0oyNY86m+uPhKQ7QbzFmDsRpo",
    "portalGunInChests": "ALdQZ+bxQA4VdfjVfdhO/sm9q3sZD9dJ",
    "dualDungeons": "ypBuvKpqKay//OvhG2COriSpGT7f4YY3",
}

# BCrypt uses a modified base64 alphabet
STD_BASE64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
BCRYPT_BASE64 = "./ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"

def std_b64_to_bcrypt_b64(s):
    trans = str.maketrans(STD_BASE64, BCRYPT_BASE64)
    return s.translate(trans)

def bcrypt_b64_to_std_b64(s):
    trans = str.maketrans(BCRYPT_BASE64, STD_BASE64)
    return s.translate(trans)

SALT_STD_B64 = "fT2JQQzNMJl2NRoMbo9RjA=="
SALT_BCRYPT_B64 = std_b64_to_bcrypt_b64(SALT_STD_B64.rstrip("="))
BCRYPT_SALT = f"$2a$04${SALT_BCRYPT_B64}"

def normalize_seed(seed):
    return re.sub(r'[^a-z0-9]', '', seed.lower())

def check_seed_verbose(seed):
    """Check a seed and show detailed output."""
    normalized = normalize_seed(seed)
    print(f"Seed: '{seed}'")
    print(f"Normalized: '{normalized}'")

    hashed = bcrypt.hashpw(normalized.encode('utf-8'), BCRYPT_SALT.encode('utf-8'))
    hash_str = hashed.decode('utf-8')
    hash_portion = hash_str[29:]
    hash_std = bcrypt_b64_to_std_b64(hash_portion)

    print(f"BCrypt hash portion: {hash_portion}")
    print(f"Converted to std b64: {hash_std}")
    print()

    for effect, target in TARGETS.items():
        if hash_std == target or hash_std.startswith(target) or target.startswith(hash_std):
            print(f"*** MATCH: {effect} ***")
            return effect

    print("No match found")
    return None

# Test seeds from the wiki
seeds_to_test = [
    # From wiki - dualDungeons
    "dual dungeons",
    "dualdungeons",

    # All 35 secret seeds from wiki
    "monochrome",
    "negative infinity",
    "invisible plane",
    "xray vision",
    "mole people",
    "save the rainforest",
    "the care bears movie",
    "i am error",
    "night of the living dead",
    "such great heights",
    "bring a towel",
    "abandoned manors",
    "how did i get here",
    "beam me up",
    "too easy",
    "fish mox",
    "purify this",
    "toadstool",
    "sandy britches",
    "truck stop",
    "arachnophobia",
    "more traps please",
    "rainbow road",
    "jagged rocks",
    "planetoids",
    "waterpark",
    "winter is coming",
    "pumpkin season",
    "hocus pocus",
    "jingle all the way",
    "what a horrible night to have a curse",
    "royale with cheese",
]

print("=== Testing known seeds ===\n")
for seed in seeds_to_test:
    check_seed_verbose(seed)
    print("-" * 50)
