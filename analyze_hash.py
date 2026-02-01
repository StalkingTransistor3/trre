#!/usr/bin/env python3
"""
Analyze the hash format to ensure we're doing comparison correctly
"""

import bcrypt
import base64

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

# Analyze the given salt
SALT_STD_B64 = "fT2JQQzNMJl2NRoMbo9RjA=="
print(f"Given salt (std b64): {SALT_STD_B64}")
print(f"Salt length: {len(SALT_STD_B64)}")

# Decode the salt
try:
    salt_bytes = base64.b64decode(SALT_STD_B64)
    print(f"Salt bytes: {salt_bytes.hex()}")
    print(f"Salt bytes length: {len(salt_bytes)}")
except Exception as e:
    print(f"Error decoding salt: {e}")

# Convert to BCrypt format
SALT_BCRYPT_B64 = std_b64_to_bcrypt_b64(SALT_STD_B64.rstrip("="))
print(f"Salt (bcrypt b64): {SALT_BCRYPT_B64}")
print(f"Salt bcrypt length: {len(SALT_BCRYPT_B64)}")

# Full BCrypt salt
BCRYPT_SALT = f"$2a$04${SALT_BCRYPT_B64}"
print(f"Full BCrypt salt: {BCRYPT_SALT}")

# Analyze the target hashes
print("\n=== Target Hash Analysis ===")
for effect, hash_val in TARGETS.items():
    print(f"\n{effect}:")
    print(f"  Hash (given): {hash_val}")
    print(f"  Length: {len(hash_val)}")

    # Check if it's valid base64
    try:
        # Add padding if needed
        padded = hash_val + "=" * (4 - len(hash_val) % 4) if len(hash_val) % 4 else hash_val
        decoded = base64.b64decode(padded)
        print(f"  Decoded bytes: {len(decoded)} bytes")
        print(f"  Hex: {decoded.hex()}")
    except Exception as e:
        print(f"  Base64 decode error: {e}")

    # Convert to BCrypt alphabet
    bcrypt_hash = std_b64_to_bcrypt_b64(hash_val)
    print(f"  BCrypt format: {bcrypt_hash}")

# Test with a known seed
print("\n=== Test with known seed ===")
test_seed = "test"
hashed = bcrypt.hashpw(test_seed.encode('utf-8'), BCRYPT_SALT.encode('utf-8'))
print(f"Seed: '{test_seed}'")
print(f"Full hash: {hashed.decode()}")
print(f"Hash portion (bcrypt b64): {hashed.decode()[29:]}")
hash_std = bcrypt_b64_to_std_b64(hashed.decode()[29:])
print(f"Hash portion (std b64): {hash_std}")

# What BCrypt hash length should be
print("\n=== BCrypt Format ===")
print("BCrypt format: $2a$04$<22-char salt><31-char hash>")
print(f"Expected salt length: 22 chars")
print(f"Expected hash length: 31 chars")
print(f"Our salt length: {len(SALT_BCRYPT_B64)}")
print(f"Our hash portions: {[len(h) for h in TARGETS.values()]}")
