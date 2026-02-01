#!/usr/bin/env python3
"""
Extended cracker with more patterns and variations
"""

import bcrypt
import re
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

def normalize_seed(seed):
    return re.sub(r'[^a-z0-9]', '', seed.lower())

def check_seed(seed):
    normalized = normalize_seed(seed)
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

# Extended word list with more variations
base_words = [
    # Effect-related
    "hallow", "holy", "sacred", "blessed", "divine", "celestial", "heaven", "paradise",
    "surface", "ground", "land", "earth", "terrain", "above", "top", "upper",
    "portal", "gate", "door", "warp", "teleport", "rift", "vortex", "gateway",
    "gun", "weapon", "blaster", "shooter", "cannon", "pistol", "rifle",
    "chest", "box", "crate", "container", "loot", "treasure", "storage",
    "dual", "double", "twin", "two", "pair", "duo", "both", "second", "twice",
    "dungeon", "maze", "labyrinth", "crypt", "tomb", "catacomb", "vault",

    # Common short words
    "a", "i", "an", "as", "at", "be", "by", "do", "go", "he", "if", "in", "is",
    "it", "me", "my", "no", "of", "on", "or", "so", "to", "up", "us", "we",
    "the", "and", "for", "are", "but", "not", "you", "all", "can", "had", "her",
    "was", "one", "our", "out", "day", "get", "has", "him", "his", "how", "its",
    "let", "may", "new", "now", "old", "see", "two", "way", "who", "boy", "did",

    # Gaming terms
    "spawn", "loot", "drop", "rare", "epic", "legendary", "mythic", "godly",
    "bonus", "secret", "hidden", "locked", "unlock", "key", "code", "cheat",
    "mode", "level", "world", "map", "zone", "area", "region", "biome",

    # Numbers as words
    "zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
    "first", "second", "third", "fourth", "fifth",

    # Common passwords/patterns
    "password", "letmein", "welcome", "admin", "user", "test", "guest", "master",
    "dragon", "monkey", "shadow", "sunshine", "princess", "football", "baseball",
    "qwerty", "abc123", "trustno1", "iloveyou", "whatever", "secret",
]

# Generate candidates
def generate_candidates():
    # Single words
    for word in base_words:
        yield word

    # Words with numbers appended
    for word in base_words[:50]:
        for num in range(0, 1000):
            yield f"{word}{num}"

    # Two-word combinations (no space - normalized)
    for w1 in base_words[:40]:
        for w2 in base_words[:40]:
            yield f"{w1}{w2}"

    # Three-word key combinations
    key1 = ["hallow", "holy", "sacred", "portal", "gun", "dual", "double", "twin", "two"]
    key2 = ["on", "in", "at", "the", "a", "with", "for", "and"]
    key3 = ["surface", "ground", "chest", "chests", "dungeon", "dungeons", "world", "top"]
    for w1 in key1:
        for w2 in key2:
            for w3 in key3:
                yield f"{w1}{w2}{w3}"
                yield f"{w1} {w2} {w3}"

    # Variations with "the"
    for word in ["hallow", "surface", "portal gun", "dungeon", "chest"]:
        yield f"the {word}"
        yield f"{word} the"

    # Common phrases
    phrases = [
        "its a secret", "you found it", "secret world", "hidden world",
        "bonus world", "special world", "dev mode", "debug mode", "test mode",
        "easy mode", "hard mode", "god mode", "creative mode",
        "all items", "free loot", "unlimited", "infinite",
        "open sesame", "abracadabra", "alakazam", "hocus pocus",
        "please", "thank you", "sorry", "help", "hello", "goodbye",
        "yes", "no", "maybe", "ok", "okay", "sure", "fine", "good", "bad",
        "start", "begin", "end", "finish", "stop", "go", "run", "walk",
        "up", "down", "left", "right", "forward", "back", "north", "south",
    ]
    for phrase in phrases:
        yield phrase

    # Movie/game references not tried before
    refs = [
        "konami code", "up up down down", "left right left right", "b a start",
        "iddqd", "idkfa", "impulse 101", "sv cheats 1", "noclip", "god",
        "rosebud", "motherlode", "kaching", "testingcheats", "freerealestate",
        "hesoyam", "baguvix", "fullclip", "infiniteammo",
        "xyzzy", "plugh", "plover", "fee fie foe foo",
        "open source", "free software", "gnu linux", "hello world",
        "foo", "bar", "baz", "qux", "quux", "corge", "grault", "garply",
        "lorem ipsum", "dolor sit amet", "the quick brown fox",
    ]
    for ref in refs:
        yield ref

    # All numbers 0 to 99999
    for i in range(100000):
        yield str(i)

print("Starting extended cracking...")
print(f"BCrypt salt: {BCRYPT_SALT.decode()}")
sys.stdout.flush()

for candidate in generate_candidates():
    result = check_seed(candidate)
    count += 1

    if count % 50000 == 0:
        print(f"Progress: {count} (current: {candidate[:30]}...)")
        sys.stdout.flush()

    if result:
        print(f"\n*** FOUND: {result} = '{candidate}' ***\n")
        found[result] = candidate
        sys.stdout.flush()

        if len(found) == 3:
            break

print(f"\n=== RESULTS (checked {count}) ===")
for effect, seed in found.items():
    print(f"{effect}: {seed}")

remaining = set(TARGETS.keys()) - set(found.keys())
if remaining:
    print(f"\nNot found: {remaining}")
