#!/usr/bin/env python3
"""
Intensive Terraria Seed Cracker

Tries many word combinations and patterns.
"""

import bcrypt
import re
import itertools
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing

# Target hashes
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
    """Check if a seed matches any of the target hashes."""
    normalized = normalize_seed(seed)
    if not normalized:
        return None, seed

    hashed = bcrypt.hashpw(normalized.encode('utf-8'), BCRYPT_SALT.encode('utf-8'))
    hash_str = hashed.decode('utf-8')
    hash_portion = hash_str[29:]
    hash_std = bcrypt_b64_to_std_b64(hash_portion)

    for effect, target in TARGETS.items():
        if hash_std == target or hash_std.startswith(target) or target.startswith(hash_std):
            return effect, seed

    return None, seed

# Extensive word list for Terraria-related and general gaming seeds
WORDS = [
    # Terraria-specific
    "hallow", "surface", "portal", "gun", "chest", "chests", "dual", "dungeon", "dungeons",
    "corruption", "crimson", "jungle", "desert", "snow", "ice", "hell", "underworld",
    "sky", "cloud", "island", "floating", "ocean", "beach", "cave", "cavern",
    "boss", "king", "queen", "slime", "eye", "brain", "eater", "wall", "flesh",
    "plantera", "golem", "cultist", "lunar", "moon", "lord", "terraria",

    # Numbers and dates
    "1", "2", "3", "4", "5", "42", "69", "420", "666", "777", "1337", "9001",

    # Common seed words
    "secret", "hidden", "special", "bonus", "easter", "egg", "debug", "test",
    "developer", "dev", "admin", "god", "mode", "cheat", "unlock", "all",

    # Gaming references
    "portal", "valve", "aperture", "science", "cake", "lie", "companion", "cube",
    "zelda", "link", "mario", "luigi", "sonic", "sega", "nintendo",

    # Pop culture
    "rick", "roll", "never", "gonna", "give", "you", "up", "let", "down",
    "starwars", "star", "wars", "trek", "force", "jedi", "sith",
    "matrix", "neo", "morpheus", "red", "blue", "pill",
    "lotr", "ring", "frodo", "gandalf", "mordor",

    # Internet culture
    "meme", "doge", "pepe", "kek", "lol", "lmao", "rofl", "yolo", "swag",
    "based", "cringe", "poggers", "pog", "sus", "among", "us", "amogus",

    # Common phrases
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could", "should",
    "can", "may", "might", "must", "shall", "for", "on", "in", "at", "by",
    "with", "from", "to", "of", "and", "or", "but", "not", "no", "yes",

    # Directions/positions
    "top", "bottom", "left", "right", "up", "down", "above", "below",
    "inside", "outside", "front", "back", "north", "south", "east", "west",

    # Colors
    "black", "white", "red", "green", "blue", "yellow", "purple", "orange",
    "pink", "cyan", "magenta", "brown", "gray", "grey", "gold", "silver",

    # Time
    "day", "night", "morning", "evening", "noon", "midnight", "dawn", "dusk",
    "today", "tomorrow", "yesterday", "now", "then", "always", "never", "forever",

    # Nature
    "sun", "moon", "star", "earth", "water", "fire", "air", "wind",
    "rain", "snow", "ice", "lightning", "thunder", "storm", "cloud",
    "tree", "forest", "mountain", "valley", "river", "lake", "sea",

    # More gaming
    "game", "play", "player", "level", "world", "map", "spawn", "respawn",
    "health", "mana", "power", "magic", "spell", "weapon", "armor", "item",
    "loot", "drop", "rare", "epic", "legendary", "mythic", "unique",

    # Animals
    "bee", "bees", "bunny", "slime", "zombie", "skeleton", "demon", "angel",
    "dragon", "worm", "fish", "bird", "bat", "spider", "snake",

    # Adjectives
    "big", "small", "large", "tiny", "huge", "giant", "mini", "mega", "ultra",
    "super", "hyper", "extra", "more", "less", "many", "few", "all", "none",
    "good", "bad", "evil", "holy", "dark", "light", "bright", "dim",
    "fast", "slow", "quick", "rapid", "hard", "soft", "easy", "difficult",
    "new", "old", "ancient", "modern", "classic", "retro", "vintage",
    "cool", "hot", "warm", "cold", "frozen", "burning", "blazing",

    # Verbs
    "run", "walk", "jump", "fly", "swim", "dig", "mine", "build", "craft",
    "fight", "attack", "defend", "block", "dodge", "roll", "dash",
    "open", "close", "lock", "unlock", "break", "fix", "make", "create",
    "find", "search", "look", "see", "watch", "hear", "listen", "feel",
    "get", "give", "take", "bring", "send", "receive", "keep", "lose",

    # Terraria items/features
    "npc", "merchant", "nurse", "guide", "goblin", "mechanic", "wizard",
    "truffle", "pirate", "cyborg", "steampunk", "witch", "doctor",
    "biome", "hardmode", "prehardmode", "expert", "master", "journey",
    "copper", "tin", "iron", "lead", "silver", "tungsten", "platinum",
    "demonite", "crimtane", "hellstone", "cobalt", "palladium", "mythril",
    "orichalcum", "adamantite", "titanium", "chlorophyte", "shroomite", "spectre",
    "luminite", "solar", "vortex", "nebula", "stardust",
]

def generate_candidates():
    """Generate candidate seeds."""
    # Single words
    for word in WORDS:
        yield word

    # Two word combinations
    for w1, w2 in itertools.product(WORDS[:100], repeat=2):
        yield f"{w1} {w2}"
        yield f"{w1}{w2}"

    # Three word combinations (limited)
    key_words = ["hallow", "surface", "portal", "gun", "chest", "dual", "dungeon", "on", "the", "in", "with", "two", "double"]
    for w1, w2, w3 in itertools.product(key_words, repeat=3):
        yield f"{w1} {w2} {w3}"
        yield f"{w1}{w2}{w3}"

    # Numeric seeds up to 10 million
    for i in range(10000000):
        yield str(i)

def main():
    found = {}
    count = 0

    print(f"Starting intensive search...")
    print(f"BCrypt salt: {BCRYPT_SALT}")
    print()

    for candidate in generate_candidates():
        result, seed = check_seed(candidate)
        count += 1

        if count % 100000 == 0:
            print(f"Checked {count} candidates... (current: {seed[:30] if len(seed) > 30 else seed})")

        if result:
            print(f"\n*** FOUND: {result} = '{seed}' ***\n")
            found[result] = seed

            if len(found) == 3:
                break

    print(f"\n=== RESULTS (checked {count} candidates) ===")
    for effect, seed in found.items():
        print(f"{effect}: {seed}")

    remaining = set(TARGETS.keys()) - set(found.keys())
    if remaining:
        print(f"\nNot found: {remaining}")

if __name__ == "__main__":
    main()
