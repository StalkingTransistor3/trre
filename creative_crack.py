#!/usr/bin/env python3
"""
Creative patterns cracker - tries dates, versions, and unique patterns
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
BCRYPT_SALT = f"$2a$04${SALT_BCRYPT_B64}".encode('utf-8')

def normalize_seed(seed):
    return re.sub(r'[^a-z0-9]', '', seed.lower())

def check_seed(seed, verbose=False):
    normalized = normalize_seed(seed)
    if not normalized:
        return None

    hashed = bcrypt.hashpw(normalized.encode('utf-8'), BCRYPT_SALT)
    hash_portion = hashed.decode('utf-8')[29:]
    hash_std = bcrypt_b64_to_std_b64(hash_portion)

    if verbose:
        print(f"'{seed}' -> '{normalized}' -> {hash_std[:25]}...")

    for effect, target in TARGETS.items():
        min_len = min(len(hash_std), len(target))
        if hash_std[:min_len] == target[:min_len]:
            return effect

    return None

found = {}

# Date formats (Terraria uses dates like 05162011)
print("=== Dates in various formats ===")
for year in range(2000, 2026):
    for month in range(1, 13):
        for day in range(1, 32):
            for fmt in [
                f"{month:02d}{day:02d}{year}",
                f"{month}{day}{year}",
                f"{year}{month:02d}{day:02d}",
                f"{day:02d}{month:02d}{year}",
            ]:
                result = check_seed(fmt)
                if result:
                    print(f"*** FOUND: {result} = '{fmt}' ***")
                    found[result] = fmt

# Version numbers
print("\n=== Version patterns ===")
for major in range(1, 3):
    for minor in range(0, 10):
        for patch in range(0, 10):
            for build in range(0, 100):
                for fmt in [
                    f"{major}.{minor}.{patch}.{build}",
                    f"{major}.{minor}.{patch}",
                    f"{major}{minor}{patch}{build}",
                    f"v{major}.{minor}.{patch}",
                ]:
                    result = check_seed(fmt)
                    if result:
                        print(f"*** FOUND: {result} = '{fmt}' ***")
                        found[result] = fmt

# Leet speak patterns
print("\n=== Leet speak and internet culture ===")
leet_words = [
    "l33t", "h4x0r", "n00b", "pr0", "1337", "w00t", "r0x0r",
    "h4ll0w", "p0rt4l", "dung30n", "ch35t", "surf4c3",
    "h4110w", "d00m", "3p1c", "l3g3nd4ry", "g0d", "m0d3",
    "s3cr3t", "h1dd3n", "sp3c14l", "b0nus", "34st3r",
    "h0ly", "s4cr3d", "d1v1n3", "c3l3st14l",
    "d0ubl3", "tw1n", "du4l", "p41r",
    "p0rt4l gun", "gun p0rt4l", "ch3st gun",
]
for word in leet_words:
    result = check_seed(word, verbose=True)
    if result:
        print(f"*** FOUND: {result} = '{word}' ***")
        found[result] = word

# Reverse words
print("\n=== Reversed words ===")
words_to_reverse = [
    "hallow", "surface", "portal", "gun", "chest", "chests",
    "dual", "dungeon", "dungeons", "secret", "hidden", "double",
    "terraria", "relogic", "cenx", "redigit", "andrew", "red",
]
for word in words_to_reverse:
    result = check_seed(word[::-1], verbose=True)
    if result:
        print(f"*** FOUND: {result} = '{word[::-1]}' ***")
        found[result] = word[::-1]

# Binary/hex patterns
print("\n=== Binary/hex patterns ===")
hex_patterns = [
    "deadbeef", "cafebabe", "baadf00d", "feedface",
    "c0ffee", "c0de", "face", "beef", "dead", "bad",
    "0xdead", "0xbeef", "0xcafe", "0xbabe",
    "01234567", "76543210", "f00d", "d00d",
]
for p in hex_patterns:
    result = check_seed(p, verbose=True)
    if result:
        print(f"*** FOUND: {result} = '{p}' ***")
        found[result] = p

# Mathematical constants
print("\n=== Math constants ===")
math_constants = [
    "pi", "e", "phi", "tau",
    "3.14159", "2.71828", "1.61803", "6.28318",
    "314159", "271828", "161803", "628318",
    "3141592653", "2718281828", "1414213562",
]
for c in math_constants:
    result = check_seed(c, verbose=True)
    if result:
        print(f"*** FOUND: {result} = '{c}' ***")
        found[result] = c

# Famous phrases (normalized)
print("\n=== Famous phrases ===")
phrases = [
    "hello world", "goodbye world", "it works", "test123", "password",
    "admin", "root", "user", "guest", "default", "master", "slave",
    "abc123", "qwerty", "asdfgh", "zxcvbn", "12345678", "87654321",
    "iloveyou", "letmein", "welcome", "monkey", "dragon", "shadow",
    "sunshine", "princess", "qwertyuiop", "asdfghjkl", "zxcvbnm",
    "trustno1", "access", "soccer", "thunder", "whatever", "killer",
]
for p in phrases:
    result = check_seed(p, verbose=True)
    if result:
        print(f"*** FOUND: {result} = '{p}' ***")
        found[result] = p

# Keyboard patterns
print("\n=== Keyboard patterns ===")
patterns = [
    "qwerty", "asdf", "zxcv", "qazwsx", "edcrfv", "tgbyhn",
    "1qaz", "2wsx", "3edc", "4rfv", "5tgb", "6yhn", "7ujm", "8ik",
    "qwertyuiop", "asdfghjkl", "zxcvbnm", "1234567890",
    "0987654321", "zyxwvutsrqponmlkjihgfedcba",
]
for p in patterns:
    result = check_seed(p, verbose=True)
    if result:
        print(f"*** FOUND: {result} = '{p}' ***")
        found[result] = p

print(f"\n=== RESULTS ===")
for effect, seed in found.items():
    print(f"{effect}: {seed}")

remaining = set(TARGETS.keys()) - set(found.keys())
if remaining:
    print(f"\nNot found: {remaining}")
