#!/usr/bin/env python3
"""
Alternative cracker with different hash comparison methods
"""

import bcrypt
import base64
import re
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

def normalize_seed(seed):
    return re.sub(r'[^a-z0-9]', '', seed.lower())

# Pre-compute target bytes for comparison
TARGET_BYTES = {}
for effect, hash_val in TARGETS.items():
    # Add padding if needed for base64 decoding
    padded = hash_val + "=" * (4 - len(hash_val) % 4) if len(hash_val) % 4 else hash_val
    try:
        decoded = base64.b64decode(padded)
        TARGET_BYTES[effect] = decoded[:24]  # Only first 24 bytes
    except:
        TARGET_BYTES[effect] = None

def check_seed_alt(seed):
    """Check seed using byte comparison instead of string comparison."""
    normalized = normalize_seed(seed)
    if not normalized:
        return None

    hashed = bcrypt.hashpw(normalized.encode('utf-8'), BCRYPT_SALT)
    hash_portion = hashed.decode('utf-8')[29:]

    # Convert BCrypt hash to standard base64
    hash_std = bcrypt_b64_to_std_b64(hash_portion)

    # Decode to bytes
    try:
        padded = hash_std + "=" * (4 - len(hash_std) % 4) if len(hash_std) % 4 else hash_std
        hash_bytes = base64.b64decode(padded)
    except:
        return None

    # Compare bytes
    for effect, target_bytes in TARGET_BYTES.items():
        if target_bytes and hash_bytes[:len(target_bytes)] == target_bytes:
            return effect

    return None

def check_seed_str(seed):
    """Check seed using string prefix comparison."""
    normalized = normalize_seed(seed)
    if not normalized:
        return None

    hashed = bcrypt.hashpw(normalized.encode('utf-8'), BCRYPT_SALT)
    hash_portion = hashed.decode('utf-8')[29:]
    hash_std = bcrypt_b64_to_std_b64(hash_portion)

    for effect, target in TARGETS.items():
        # Try different prefix lengths
        for prefix_len in [31, 32, 30, 28, 24, 20]:
            if hash_std[:prefix_len] == target[:prefix_len]:
                return effect

    return None

# Test candidates
candidates = [
    # Short common words
    "a", "i", "no", "go", "up", "hi", "ok", "me", "we", "us",
    "the", "and", "for", "are", "but", "not", "you", "all",
    "can", "her", "was", "one", "our", "out",

    # Numbers
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
    "10", "11", "12", "13", "42", "69", "99", "100",

    # Two-letter combos
    "aa", "ab", "ac", "ad", "ba", "bb", "bc", "bd",
    "ha", "he", "hi", "ho", "hu", "hy",
    "sa", "se", "si", "so", "su",
    "po", "pa", "pe", "pi", "pu",
    "du", "da", "de", "di", "do",

    # Effect-related short
    "hs", "hos", "hots",
    "pg", "pgc", "pgic",
    "dd", "2d", "d2",

    # Common Terraria
    "npc", "hp", "mp", "dmg", "def", "crit",
    "dig", "fly", "run", "jump",

    # Leetspeak variations
    "h4110w", "h411ow", "p0rt4l", "dung30n",

    # More obscure
    "owo", "uwu", "nya", "meow", "woof",
    "yay", "yee", "wee", "whee",
    "lol", "lmao", "rofl", "xd",
]

# Also add all single characters and two-character combinations
import string
for c in string.ascii_lowercase + string.digits:
    candidates.append(c)
for c1 in string.ascii_lowercase:
    for c2 in string.ascii_lowercase + string.digits:
        candidates.append(c1 + c2)

candidates = list(set(candidates))  # Remove duplicates

print(f"Testing {len(candidates)} candidates with alternative methods...")
print(f"BCrypt salt: {BCRYPT_SALT.decode()}")
sys.stdout.flush()

found_alt = {}
found_str = {}

for seed in candidates:
    result = check_seed_alt(seed)
    if result:
        print(f"[ALT] FOUND: {result} = '{seed}'")
        found_alt[result] = seed

    result = check_seed_str(seed)
    if result:
        print(f"[STR] FOUND: {result} = '{seed}'")
        found_str[result] = seed

print(f"\n=== RESULTS (alt method) ===")
for effect, seed in found_alt.items():
    print(f"{effect}: {seed}")

print(f"\n=== RESULTS (str method) ===")
for effect, seed in found_str.items():
    print(f"{effect}: {seed}")

remaining = set(TARGETS.keys()) - set(found_alt.keys()) - set(found_str.keys())
if remaining:
    print(f"\nNot found: {remaining}")
