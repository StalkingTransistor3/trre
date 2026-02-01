#!/usr/bin/env python3
"""
Aggressive short string brute force
"""

import bcrypt
import string
import itertools
import sys
from multiprocessing import Pool, cpu_count

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
    results = []
    for normalized in batch:
        hashed = bcrypt.hashpw(normalized.encode('utf-8'), BCRYPT_SALT)
        hash_portion = hashed.decode('utf-8')[29:]
        hash_std = bcrypt_b64_to_std_b64(hash_portion)

        for effect, target in TARGETS.items():
            min_len = min(len(hash_std), len(target))
            if hash_std[:min_len] == target[:min_len]:
                results.append((effect, normalized))
                break
    return results

def gen_strings(length):
    chars = string.ascii_lowercase + string.digits
    for combo in itertools.product(chars, repeat=length):
        yield ''.join(combo)

def batch_gen(gen, size=1000):
    batch = []
    for item in gen:
        batch.append(item)
        if len(batch) >= size:
            yield batch
            batch = []
    if batch:
        yield batch

def search_length(length):
    print(f"\n=== Searching length {length} ({36**length:,} combinations) ===")
    sys.stdout.flush()

    found = {}
    count = 0

    with Pool(cpu_count()) as pool:
        for results in pool.imap_unordered(check_batch, batch_gen(gen_strings(length))):
            count += 1000
            if count % 500000 == 0:
                print(f"  Progress: {count:,}")
                sys.stdout.flush()

            for effect, seed in results:
                print(f"\n*** FOUND: {effect} = '{seed}' ***\n")
                found[effect] = seed
                sys.stdout.flush()

    return found

if __name__ == '__main__':
    print(f"BCrypt salt: {BCRYPT_SALT.decode()}")
    print(f"Using {cpu_count()} CPU cores")
    sys.stdout.flush()

    all_found = {}

    # Search lengths 1-6
    for length in range(1, 7):
        if len(all_found) == 3:
            break

        found = search_length(length)
        all_found.update(found)

        if found:
            print(f"Found so far: {found}")

    print(f"\n=== FINAL RESULTS ===")
    for effect, seed in all_found.items():
        print(f"{effect}: {seed}")

    remaining = set(TARGETS.keys()) - set(all_found.keys())
    if remaining:
        print(f"\nNot found: {remaining}")
