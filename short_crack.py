#!/usr/bin/env python3
"""
Exhaustive short string cracker - tries ALL short alphanumeric combinations
"""

import bcrypt
import re
import string
import itertools
import sys

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

def check_seed(normalized):
    if not normalized:
        return None

    hashed = bcrypt.hashpw(normalized.encode('utf-8'), BCRYPT_SALT)
    hash_portion = hashed.decode('utf-8')[29:]
    hash_std = bcrypt_b64_to_std_b64(hash_portion)

    for effect, target in TARGETS.items():
        min_len = min(len(hash_std), len(target))
        if hash_std[:min_len] == target[:min_len]:
            return effect

    return None

found = {}
count = 0
chars = string.ascii_lowercase + string.digits

print(f"BCrypt salt: {BCRYPT_SALT.decode()}")
print(f"Trying all short alphanumeric strings...")
sys.stdout.flush()

# Try all lengths 1-5
for length in range(1, 6):
    print(f"\nLength {length} ({36**length} combinations)...")
    sys.stdout.flush()

    for combo in itertools.product(chars, repeat=length):
        normalized = ''.join(combo)
        count += 1

        if count % 100000 == 0:
            print(f"  Progress: {count} (current: {normalized})")
            sys.stdout.flush()

        result = check_seed(normalized)
        if result:
            print(f"\n*** FOUND: {result} = '{normalized}' ***\n")
            found[result] = normalized
            sys.stdout.flush()

            if len(found) == 3:
                print("All found!")
                break

    if len(found) == 3:
        break

# Also try numbers up to 10 million
if len(found) < 3:
    print("\nTrying numeric seeds 0-10000000...")
    sys.stdout.flush()

    for i in range(10000000):
        normalized = str(i)
        count += 1

        if count % 500000 == 0:
            print(f"  Progress: {count} (current: {normalized})")
            sys.stdout.flush()

        result = check_seed(normalized)
        if result:
            print(f"\n*** FOUND: {result} = '{normalized}' ***\n")
            found[result] = normalized
            sys.stdout.flush()

            if len(found) == 3:
                break

print(f"\n=== RESULTS (checked {count} candidates) ===")
for effect, seed in found.items():
    print(f"{effect}: {seed}")

remaining = set(TARGETS.keys()) - set(found.keys())
if remaining:
    print(f"\nNot found: {remaining}")
