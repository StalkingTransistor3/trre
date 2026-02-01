#!/usr/bin/env python3
"""
Focused Terraria Seed Cracker - tries short strings and specific patterns
"""

import bcrypt
import re
import string
import itertools

TARGETS = {
    "hallowOnTheSurface": "KYvKIk2LK0oyNY86m+uPhKQ7QbzFmDsRpo",
    "portalGunInChests": "ALdQZ+bxQA4VdfjVfdhO/sm9q3sZD9dJ",
    "dualDungeons": "ypBuvKpqKay//OvhG2COriSpGT7f4YY3",
}

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

def check_seed(seed):
    normalized = normalize_seed(seed)
    if not normalized:
        return None

    hashed = bcrypt.hashpw(normalized.encode('utf-8'), BCRYPT_SALT.encode('utf-8'))
    hash_str = hashed.decode('utf-8')
    hash_portion = hash_str[29:]
    hash_std = bcrypt_b64_to_std_b64(hash_portion)

    for effect, target in TARGETS.items():
        # Try various comparison methods
        if hash_std == target:
            return effect
        if hash_std.rstrip('=') == target.rstrip('='):
            return effect
        # Prefix match (in case of length issues)
        min_len = min(len(hash_std), len(target))
        if hash_std[:min_len] == target[:min_len]:
            return effect

    return None

found = {}

# Try all lowercase strings of length 1-5
print("Trying short lowercase strings...")
for length in range(1, 6):
    print(f"  Length {length}...")
    for combo in itertools.product(string.ascii_lowercase, repeat=length):
        seed = ''.join(combo)
        result = check_seed(seed)
        if result:
            print(f"\n*** FOUND: {result} = '{seed}' ***\n")
            found[result] = seed

# Try all alphanumeric strings of length 1-4
print("Trying short alphanumeric strings...")
chars = string.ascii_lowercase + string.digits
for length in range(1, 5):
    print(f"  Length {length}...")
    for combo in itertools.product(chars, repeat=length):
        seed = ''.join(combo)
        result = check_seed(seed)
        if result:
            print(f"\n*** FOUND: {result} = '{seed}' ***\n")
            found[result] = seed

# Try common short phrases
print("Trying common phrases...")
phrases = [
    # Short memes and references
    "gg", "ez", "op", "rip", "lol", "wtf", "omg", "bruh", "yeet", "noob",
    "pro", "pog", "sus", "amogus", "sigma", "alpha", "beta", "omega",

    # Dates (MMDDYYYY format like Terraria uses)
    "01012024", "12252023", "10312023", "07042024", "04012024",

    # Simple phrases
    "hello world", "test123", "password", "admin", "debug", "secret",
    "developer", "cheat", "unlock", "god mode", "creative",

    # Terraria dates/versions
    "1449", "1450", "1451", "145", "144", "143", "05162011", "05162020",

    # Random ideas
    "yes", "no", "maybe", "ok", "okay", "sure", "why not", "because",
    "trust me", "believe", "faith", "hope", "love", "hate", "fear",

    # More gaming references
    "iddqd", "idkfa", "konami", "up up down down",
    "sv_cheats 1", "noclip", "god", "fly", "spawn",

    # Movie/book references
    "rosebud", "xanadu", "kansas", "oz", "wonderland", "narnia",
    "hogwarts", "tatooine", "endor", "hoth", "dagobah",
]

for phrase in phrases:
    result = check_seed(phrase)
    if result:
        print(f"\n*** FOUND: {result} = '{phrase}' ***\n")
        found[result] = phrase

print("\n=== RESULTS ===")
for effect, seed in found.items():
    print(f"{effect}: {seed}")

remaining = set(TARGETS.keys()) - set(found.keys())
if remaining:
    print(f"\nNot found: {remaining}")
