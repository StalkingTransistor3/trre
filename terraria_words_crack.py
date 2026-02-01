#!/usr/bin/env python3
"""
Cracker focusing on Terraria-specific terminology and patterns
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

# Terraria NPCs and characters
npcs = [
    "guide", "merchant", "nurse", "arms dealer", "dryad", "demolitionist",
    "clothier", "goblin tinkerer", "wizard", "mechanic", "truffle",
    "steampunker", "dye trader", "party girl", "cyborg", "painter",
    "witch doctor", "pirate", "stylist", "angler", "tax collector",
    "skeleton merchant", "golfer", "zoologist", "princess", "santa claus",
    "old man", "travelling merchant", "andrew", "cenx", "redigit", "red",
    "yorai", "leinfors", "grox", "crowno", "skiphs", "lazure", "ghostar",
    "arkhalis", "darthkitten", "d-town", "food barbarian", "acacia", "will",
]

# Terraria bosses
bosses = [
    "king slime", "eye of cthulhu", "eater of worlds", "brain of cthulhu",
    "queen bee", "skeletron", "wall of flesh", "queen slime",
    "the twins", "the destroyer", "skeletron prime", "plantera",
    "golem", "duke fishron", "empress of light", "lunatic cultist",
    "moon lord", "deerclops", "ocram", "lepus", "turkor",
]

# Terraria biomes and locations
biomes = [
    "forest", "desert", "snow", "jungle", "corruption", "crimson",
    "hallow", "ocean", "space", "underground", "cavern", "underworld",
    "hell", "dungeon", "temple", "abyss", "mushroom", "spider cave",
    "granite", "marble", "floating island", "sky", "beach",
]

# Terraria items
items = [
    "zenith", "meowmere", "star wrath", "terra blade", "last prism",
    "lunar flare", "s.d.m.g.", "celebration", "copper shortsword",
    "nights edge", "true excalibur", "portal gun", "rod of discord",
    "slime staff", "lucky coin", "coin gun", "binoculars", "companion cube",
]

# Terraria events
events = [
    "blood moon", "solar eclipse", "goblin army", "frost legion",
    "pirate invasion", "pumpkin moon", "frost moon", "martian madness",
    "lunar events", "old ones army", "slime rain",
]

# Common modifiers/adjectives
modifiers = [
    "big", "small", "huge", "tiny", "mega", "ultra", "super", "hyper",
    "double", "triple", "quad", "twin", "dual", "multi", "extra",
    "holy", "sacred", "blessed", "cursed", "haunted", "enchanted",
    "ancient", "legendary", "mythical", "godly", "demonic", "ruthless",
    "lucky", "quick", "deadly", "agile", "murderous", "superior",
]

# Terraria update references
updates = [
    "journey's end", "journeys end", "1.4", "1.4.4", "1.4.5",
    "labor of love", "bold boulder", "otherworld",
    "terraria 2", "terraria otherworld",
]

all_words = npcs + bosses + biomes + items + events + modifiers + updates

print("Testing Terraria-specific combinations...")

found = {}

# Single words
print("\n=== Single Terraria words ===")
for word in all_words:
    result = check_seed(word, verbose=True)
    if result:
        print(f"\n*** FOUND: {result} = '{word}' ***\n")
        found[result] = word

# Two-word combinations
print("\n=== Two-word combinations ===")
for w1, w2 in itertools.product(all_words[:30], all_words[:30]):
    for sep in ["", " "]:
        seed = f"{w1}{sep}{w2}"
        result = check_seed(seed)
        if result:
            print(f"\n*** FOUND: {result} = '{seed}' ***\n")
            found[result] = seed

# Developer references
print("\n=== Developer/easter egg references ===")
dev_refs = [
    "red loves you", "cenx is watching", "redigit was here",
    "andrew is here", "thanks for playing", "you found it",
    "secret found", "easter egg", "hidden treasure", "bonus level",
    "developer mode", "debug world", "test seed", "secret seed",
    "the devs say hi", "relogic", "engine software", "505 games",
    "terraria forever", "dig peons dig", "peon", "peons",
    "for cenx", "for red", "for the team", "thank you",
]

for phrase in dev_refs:
    result = check_seed(phrase, verbose=True)
    if result:
        print(f"\n*** FOUND: {result} = '{phrase}' ***\n")
        found[result] = phrase

print(f"\n=== RESULTS ===")
for effect, seed in found.items():
    print(f"{effect}: {seed}")

remaining = set(TARGETS.keys()) - set(found.keys())
if remaining:
    print(f"\nNot found: {remaining}")
