#!/usr/bin/env python3
"""
Obscure references cracker - tries specific cultural references
"""

import bcrypt
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

def check_seed(seed, verbose=True):
    normalized = normalize_seed(seed)
    if not normalized:
        return None

    hashed = bcrypt.hashpw(normalized.encode('utf-8'), BCRYPT_SALT)
    hash_portion = hashed.decode('utf-8')[29:]
    hash_std = bcrypt_b64_to_std_b64(hash_portion)

    if verbose:
        print(f"'{seed}' -> '{normalized}' -> {hash_std[:20]}...")

    for effect, target in TARGETS.items():
        min_len = min(len(hash_std), len(target))
        if hash_std[:min_len] == target[:min_len]:
            return effect
    return None

found = {}

# Obscure references for each effect

# hallowOnTheSurface - Hallow/holy/sacred surface references
hallow_refs = [
    # Religious/spiritual
    "hallowed ground", "holy ground", "sacred ground", "blessed earth",
    "heaven on earth", "paradise found", "garden of eden", "eden",
    "stairway to heaven", "highway to heaven", "knock on heavens door",
    "angels among us", "touched by an angel", "angel on earth",
    "the rapture", "judgement day", "second coming", "risen",
    "holy land", "promised land", "land of milk and honey",
    "above and beyond", "higher ground", "moral high ground",
    "enlightenment", "nirvana", "satori", "awakening", "ascension",
    "transcendence", "elevation", "exaltation", "glorification",

    # Fairy tale / fantasy
    "fairy land", "fairy realm", "fae realm", "enchanted land",
    "magic kingdom", "wonderland", "neverland", "oz",
    "crystal kingdom", "rainbow kingdom", "light kingdom",
    "good kingdom", "pure land", "clean land", "bright land",

    # Nature / light
    "sunshine", "sunlight", "daylight", "starlight", "moonlight",
    "bright side", "silver lining", "ray of light", "beacon of hope",
    "morning glory", "dawn of a new day", "new dawn", "sunrise",

    # Misc
    "topside", "upstairs", "above ground", "surface level",
    "emerged", "risen up", "come up", "brought up", "raised up",
    "holy moly", "holy cow", "holy smokes", "holy mackerel",
    "good heavens", "good gracious", "good lord", "oh my god",

    # Game references
    "light world", "sacred realm", "golden realm", "pure realm",
    "angelic", "divine", "celestial", "ethereal", "heavenly",
]

# portalGunInChests - Portal game references
portal_refs = [
    # Portal game quotes
    "the cake is a lie", "cake is a lie", "still alive", "want you gone",
    "now youre thinking with portals", "thinking with portals",
    "speedy thing goes in", "speedy thing comes out",
    "this was a triumph", "huge success", "im making a note here",
    "we do what we must", "because we can", "for the good of all of us",
    "except the ones who are dead", "but theres no sense crying",
    "youll be dead", "aperture science", "aperture",
    "glados", "cave johnson", "wheatley", "chell", "atlas", "pbody",
    "companion cube", "weighted companion cube", "portal gun", "ashpd",
    "orange portal", "blue portal", "quantum tunneling",

    # Portal 2 references
    "want you gone", "exile vilify", "cara mia", "turret opera",
    "space core", "adventure core", "fact core", "curiosity core",
    "combustible lemons", "lemon grenade", "burn life house down",

    # Valve / Half-Life
    "valve", "half life", "black mesa", "lambda", "gordon freeman",
    "g man", "rise and shine", "the right man", "wrong place",
    "gravity gun", "zero point energy",

    # General gun in chest ideas
    "armed to the teeth", "locked and loaded", "guns blazing",
    "heavy artillery", "big guns", "bring out the big guns",
    "packing heat", "carrying", "strapped",
    "loot box", "prize inside", "jackpot", "treasure trove",
    "mystery box", "surprise inside", "gift", "present",
]

# dualDungeons - Double/twin references
dual_refs = [
    # Twin references
    "twin peaks", "the shining", "here's johnny", "all work no play",
    "double trouble", "seeing double", "double vision", "double take",
    "twice the fun", "two for one", "two of a kind", "two peas in a pod",
    "dynamic duo", "terrible two", "double whammy", "double down",
    "twins", "gemini", "castor and pollux", "romulus and remus",
    "yin and yang", "yin yang", "good and evil", "light and dark",
    "two sides", "both sides", "either side", "mirror image",
    "doppelganger", "shadow self", "alter ego", "split personality",
    "two faced", "double agent", "double life", "second life",

    # Dungeon references
    "dungeon master", "dungeons and dragons", "dnd", "d&d",
    "dungeon crawler", "dungeon delver", "dungeon dive",
    "into the dungeon", "down the dungeon", "escape the dungeon",
    "double dungeon", "twin dungeon", "mirror dungeon", "shadow dungeon",
    "dungeon run", "dungeon raid", "clear the dungeon",

    # Number 2 references
    "take two", "round two", "part two", "volume two", "chapter two",
    "electric boogaloo", "2 fast 2 furious", "back 2 back", "b2b",
    "squared", "doubled", "multiplied", "cloned", "copied", "duplicated",

    # Pairs
    "pair of", "couple of", "both of", "set of two", "duo",
    "binary", "bilateral", "bipartite", "bifurcated",
    "parallel", "symmetric", "mirrored", "reflected",
]

print("Testing obscure references...")
print(f"BCrypt salt: {BCRYPT_SALT.decode()}")
sys.stdout.flush()

print("\n=== Hallow/Surface references ===")
for ref in hallow_refs:
    result = check_seed(ref)
    if result:
        print(f"\n*** FOUND: {result} = '{ref}' ***\n")
        found[result] = ref

print("\n=== Portal/Gun references ===")
for ref in portal_refs:
    result = check_seed(ref)
    if result:
        print(f"\n*** FOUND: {result} = '{ref}' ***\n")
        found[result] = ref

print("\n=== Dual/Twin references ===")
for ref in dual_refs:
    result = check_seed(ref)
    if result:
        print(f"\n*** FOUND: {result} = '{ref}' ***\n")
        found[result] = ref

print(f"\n=== RESULTS ===")
for effect, seed in found.items():
    print(f"{effect}: {seed}")

remaining = set(TARGETS.keys()) - set(found.keys())
if remaining:
    print(f"\nNot found: {remaining}")
