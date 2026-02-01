#!/usr/bin/env python3
"""
Terraria Seed Cracker

Cracks BCrypt hashes to find Terraria seeds.
Verification: lowercase, keep only a-z 0-9, BCrypt with salt `fT2JQQzNMJl2NRoMbo9RjA==` cost 4.
"""

import bcrypt
import base64
import re
import itertools
import string

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
    """Convert standard base64 to BCrypt's base64 alphabet."""
    trans = str.maketrans(STD_BASE64, BCRYPT_BASE64)
    return s.translate(trans)

def bcrypt_b64_to_std_b64(s):
    """Convert BCrypt's base64 to standard base64 alphabet."""
    trans = str.maketrans(BCRYPT_BASE64, STD_BASE64)
    return s.translate(trans)

# Convert the salt from standard base64 to BCrypt base64
SALT_STD_B64 = "fT2JQQzNMJl2NRoMbo9RjA=="
SALT_BCRYPT_B64 = std_b64_to_bcrypt_b64(SALT_STD_B64.rstrip("="))
# Full BCrypt salt prefix with cost 4
BCRYPT_SALT = f"$2a$04${SALT_BCRYPT_B64}"

print(f"BCrypt salt: {BCRYPT_SALT}")

# Convert targets from standard base64 to bcrypt base64 for comparison
TARGETS_BCRYPT = {}
for effect, hash_std in TARGETS.items():
    # Pad if needed for valid base64
    padded = hash_std + "=" * (4 - len(hash_std) % 4) if len(hash_std) % 4 else hash_std
    hash_bcrypt = std_b64_to_bcrypt_b64(hash_std)
    TARGETS_BCRYPT[effect] = hash_bcrypt
    print(f"{effect}: std={hash_std} -> bcrypt={hash_bcrypt}")

def normalize_seed(seed):
    """Lowercase and keep only a-z 0-9."""
    return re.sub(r'[^a-z0-9]', '', seed.lower())

def check_seed(seed, verbose=False):
    """Check if a seed matches any of the target hashes."""
    normalized = normalize_seed(seed)
    if not normalized:
        return None

    # Generate BCrypt hash
    hashed = bcrypt.hashpw(normalized.encode('utf-8'), BCRYPT_SALT.encode('utf-8'))
    hash_str = hashed.decode('utf-8')

    # Extract just the hash portion (after the 29-char prefix: $2a$04$ + 22 char salt)
    hash_portion = hash_str[29:]

    # Also convert to standard base64 for comparison
    hash_std = bcrypt_b64_to_std_b64(hash_portion)

    if verbose:
        print(f"Seed: {seed} -> normalized: {normalized}")
        print(f"  BCrypt hash: {hash_portion}")
        print(f"  Std base64:  {hash_std}")

    # Check against both formats
    for effect, target in TARGETS.items():
        if hash_std == target or hash_std.rstrip("=") == target.rstrip("="):
            return effect
        # Also check first N chars in case of padding differences
        if hash_std[:len(target)] == target or target[:len(hash_std)] == hash_std:
            return effect

    for effect, target in TARGETS_BCRYPT.items():
        if hash_portion == target or hash_portion[:len(target)] == target:
            return effect

    return None

# Known Terraria special seeds to try
SPECIAL_SEEDS = [
    # Official special seeds
    "for the worthy",
    "not the bees",
    "drunk world",
    "celebrationmk10",
    "the constant",
    "don't starve",
    "no traps",
    "remix",
    "zenith",
    "get fixed boi",
    "getfixedboi",

    # Variations and combinations
    "05162020",
    "5162020",
    "05162011",
    "5162011",

    # Maybe related to the effects themselves
    "hallow on the surface",
    "hallowonthesurface",
    "hallow on surface",
    "hallowonsurface",
    "surface hallow",
    "surfacehallow",

    "portal gun in chests",
    "portalguninchests",
    "portal gun chests",
    "portalgunchests",
    "portal chests",
    "portalchests",

    "dual dungeons",
    "dualdungeons",
    "two dungeons",
    "twodungeons",
    "double dungeon",
    "doubledungeon",
    "double dungeons",
    "doubledungeons",
    "2dungeons",
    "2dungeon",

    # Legacy and secret seeds
    "notthebees",
    "fortheworthy",
    "theconstant",
    "dontstarve",
    "notraps",

    # Common combinations
    "secret",
    "easter egg",
    "easteregg",
    "special",
    "hidden",
]

def try_special_seeds():
    """Try known special Terraria seeds."""
    print("\n=== Trying special seeds ===")
    found = {}

    for seed in SPECIAL_SEEDS:
        result = check_seed(seed, verbose=False)
        if result:
            print(f"\n*** FOUND: {result} = '{seed}' ***\n")
            found[result] = seed

    return found

def try_numeric_range(start=0, end=1000000):
    """Try numeric seeds in a range."""
    print(f"\n=== Trying numeric seeds {start} to {end} ===")
    found = {}

    for i in range(start, end):
        if i % 100000 == 0:
            print(f"Progress: {i}")

        seed = str(i)
        result = check_seed(seed)
        if result:
            print(f"\n*** FOUND: {result} = '{seed}' ***\n")
            found[result] = seed
            if len(found) == 3:
                break

    return found

def try_word_combinations():
    """Try common word combinations."""
    words = [
        "hallow", "surface", "portal", "gun", "chest", "chests",
        "dual", "dungeon", "dungeons", "world", "seed", "secret",
        "fixed", "boi", "worthy", "bees", "drunk", "constant",
        "starve", "traps", "remix", "zenith", "celebration",
        "double", "two", "both", "twin", "multi",
        "on", "the", "in", "at", "with",
    ]

    print("\n=== Trying word combinations ===")
    found = {}

    # Single words
    for word in words:
        result = check_seed(word)
        if result:
            print(f"\n*** FOUND: {result} = '{word}' ***\n")
            found[result] = word

    # Two word combinations
    print("Trying 2-word combinations...")
    for w1, w2 in itertools.product(words, repeat=2):
        for sep in ["", " "]:
            seed = f"{w1}{sep}{w2}"
            result = check_seed(seed)
            if result:
                print(f"\n*** FOUND: {result} = '{seed}' ***\n")
                found[result] = seed

    # Three word combinations (limited)
    print("Trying 3-word combinations...")
    key_words = ["hallow", "surface", "portal", "gun", "chest", "chests", "dual", "dungeon", "dungeons", "on", "the", "in"]
    for w1, w2, w3 in itertools.product(key_words, repeat=3):
        for sep in ["", " "]:
            seed = f"{w1}{sep}{w2}{sep}{w3}"
            result = check_seed(seed)
            if result:
                print(f"\n*** FOUND: {result} = '{seed}' ***\n")
                found[result] = seed

    return found

def try_alphanumeric(length=6):
    """Try short alphanumeric strings."""
    print(f"\n=== Trying alphanumeric length {length} ===")
    chars = string.ascii_lowercase + string.digits
    found = {}
    count = 0

    for combo in itertools.product(chars, repeat=length):
        seed = ''.join(combo)
        count += 1
        if count % 1000000 == 0:
            print(f"Progress: {count} ({seed})")

        result = check_seed(seed)
        if result:
            print(f"\n*** FOUND: {result} = '{seed}' ***\n")
            found[result] = seed
            if len(found) == 3:
                return found

    return found

if __name__ == "__main__":
    all_found = {}

    # Try special seeds first (fast)
    found = try_special_seeds()
    all_found.update(found)

    # Check remaining
    remaining = set(TARGETS.keys()) - set(all_found.keys())
    if remaining:
        print(f"\nStill need to find: {remaining}")

        # Try word combinations
        found = try_word_combinations()
        all_found.update(found)

    remaining = set(TARGETS.keys()) - set(all_found.keys())
    if remaining:
        print(f"\nStill need to find: {remaining}")

        # Try numeric range
        found = try_numeric_range(0, 1000000)
        all_found.update(found)

    print("\n=== RESULTS ===")
    for effect, seed in all_found.items():
        print(f"{effect}: {seed}")

    remaining = set(TARGETS.keys()) - set(all_found.keys())
    if remaining:
        print(f"\nNot found: {remaining}")
