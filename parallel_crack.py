#!/usr/bin/env python3
"""
Parallel Terraria Seed Cracker using multiprocessing
"""

import bcrypt
import re
import string
import itertools
import sys
from multiprocessing import Pool, cpu_count
from functools import partial

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

def check_batch(batch):
    """Check a batch of seeds."""
    results = []
    for normalized in batch:
        if not normalized:
            continue

        hashed = bcrypt.hashpw(normalized.encode('utf-8'), BCRYPT_SALT)
        hash_portion = hashed.decode('utf-8')[29:]
        hash_std = bcrypt_b64_to_std_b64(hash_portion)

        for effect, target in TARGETS.items():
            min_len = min(len(hash_std), len(target))
            if hash_std[:min_len] == target[:min_len]:
                results.append((effect, normalized))
                break

    return results

def generate_candidates():
    """Generate candidate seeds."""
    chars = string.ascii_lowercase + string.digits

    # Short alphanumeric (1-5 chars)
    for length in range(1, 6):
        for combo in itertools.product(chars, repeat=length):
            yield ''.join(combo)

    # Numbers up to 10 million
    for i in range(10000000):
        yield str(i)

def batch_generator(candidates, batch_size=1000):
    """Group candidates into batches."""
    batch = []
    for c in candidates:
        batch.append(c)
        if len(batch) >= batch_size:
            yield batch
            batch = []
    if batch:
        yield batch

if __name__ == '__main__':
    print(f"BCrypt salt: {BCRYPT_SALT.decode()}")
    print(f"Using {cpu_count()} CPU cores")
    sys.stdout.flush()

    found = {}
    count = 0

    with Pool(cpu_count()) as pool:
        for results in pool.imap_unordered(check_batch, batch_generator(generate_candidates())):
            count += 1000
            if count % 100000 == 0:
                print(f"Progress: {count} batches")
                sys.stdout.flush()

            for effect, seed in results:
                print(f"\n*** FOUND: {effect} = '{seed}' ***\n")
                found[effect] = seed
                sys.stdout.flush()

    print(f"\n=== RESULTS ===")
    for effect, seed in found.items():
        print(f"{effect}: {seed}")

    remaining = set(TARGETS.keys()) - set(found.keys())
    if remaining:
        print(f"\nNot found: {remaining}")
