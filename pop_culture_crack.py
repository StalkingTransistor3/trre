#!/usr/bin/env python3
"""
Cracker focusing on pop culture references and patterns from known Terraria seeds
"""

import bcrypt
import re

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

def check_seed(seed, verbose=False):
    normalized = normalize_seed(seed)
    if not normalized:
        return None

    hashed = bcrypt.hashpw(normalized.encode('utf-8'), BCRYPT_SALT.encode('utf-8'))
    hash_str = hashed.decode('utf-8')
    hash_portion = hash_str[29:]
    hash_std = bcrypt_b64_to_std_b64(hash_portion)

    if verbose:
        print(f"  '{seed}' -> '{normalized}' -> {hash_std[:20]}...")

    for effect, target in TARGETS.items():
        min_len = min(len(hash_std), len(target))
        if hash_std[:min_len] == target[:min_len]:
            return effect

    return None

found = {}

# Pop culture references that might relate to these effects
candidates = [
    # hallowOnTheSurface - Halloween/Hallow themed
    "trick or treat", "halloween", "all hallows eve", "samhain",
    "jack o lantern", "spooky scary", "skeleton dance",
    "nightmare before christmas", "this is halloween",
    "monster mash", "thriller", "ghostbusters",
    "holy ground", "sacred ground", "blessed land",
    "fairy tale", "fairytale", "enchanted forest",
    "rainbow connection", "over the rainbow", "somewhere over the rainbow",
    "good vibrations", "good vibes", "positive energy",
    "heaven on earth", "paradise", "eden", "garden of eden",
    "elysium", "valhalla", "nirvana", "utopia", "shangri la",
    "crystal palace", "crystal kingdom", "glass castle",
    "fairy kingdom", "fairy realm", "fae realm", "seelie court",
    "blessed be", "may the light", "let there be light",

    # portalGunInChests - Portal game references
    "the cake is a lie", "cake is a lie", "still alive",
    "want you gone", "you monster", "for science",
    "aperture science", "aperture", "glados", "gladys",
    "wheatley", "chell", "companion cube", "weighted cube",
    "thinking with portals", "now youre thinking with portals",
    "speedy thing goes in", "speedy thing goes out",
    "blue portal", "orange portal", "quantum tunneling",
    "we do what we must", "because we can",
    "this was a triumph", "im making a note here",
    "huge success", "its hard to overstate my satisfaction",
    "valve", "half life", "black mesa", "resonance cascade",
    "crowbar", "gravity gun", "zero point energy",
    "freeman", "gordon freeman", "g man",

    # dualDungeons - Two/dual themed
    "double trouble", "twice the fun", "two of a kind",
    "double dragon", "double dare", "double down",
    "twins", "gemini", "two sides", "mirror mirror",
    "doppelganger", "shadow clone", "copy that",
    "twice upon a time", "second time around",
    "double or nothing", "all in", "split decision",
    "fork in the road", "two paths", "two roads",
    "two roads diverged", "road less traveled",
    "yin yang", "yin and yang", "balance", "harmony",
    "opposites attract", "polar opposites",
    "east meets west", "north south", "left right",
    "alpha omega", "beginning and end", "first and last",
    "dynamic duo", "batman robin", "bonnie clyde",
    "peanut butter jelly", "salt pepper", "fire ice",

    # More generic gaming seeds
    "hidden treasure", "secret stash", "buried treasure",
    "x marks the spot", "treasure map", "treasure hunt",
    "easter egg hunt", "egg hunt", "found it",
    "developer room", "debug mode", "test level",
    "bonus stage", "secret level", "hidden level",
    "warp zone", "minus world", "world -1",
    "secret passage", "hidden door", "secret door",
    "behind the waterfall", "under the stairs",

    # Numeric patterns
    "2", "22", "222", "2222", "1234", "4321",
    "111", "333", "444", "555", "666", "777", "888", "999",
    "007", "420", "69", "1337", "9001", "42",
    "314159", "271828", "161803", "141421",

    # Simple words
    "holy", "sacred", "blessed", "divine", "celestial",
    "portal", "gate", "gateway", "door", "doorway",
    "double", "dual", "twin", "pair", "duo", "couple",
    "two", "second", "twice", "both", "either", "neither",

    # Movie quotes
    "here's johnny", "i'll be back", "hasta la vista",
    "may the force", "use the force", "i am your father",
    "you shall not pass", "my precious", "one ring",
    "there is no spoon", "follow the white rabbit",
    "welcome to the real world", "red pill blue pill",

    # Internet/meme culture
    "its over 9000", "barrel roll", "do a barrel roll",
    "all your base", "all your base are belong to us",
    "arrow to the knee", "took an arrow", "fus ro dah",
    "never gonna give you up", "rick roll", "rickroll",
    "leroy jenkins", "leeroy", "at least i have chicken",
]

print("Testing pop culture and themed candidates...")
for seed in candidates:
    result = check_seed(seed, verbose=True)
    if result:
        print(f"\n*** FOUND: {result} = '{seed}' ***\n")
        found[result] = seed

print("\n=== RESULTS ===")
for effect, seed in found.items():
    print(f"{effect}: {seed}")

remaining = set(TARGETS.keys()) - set(found.keys())
if remaining:
    print(f"\nNot found: {remaining}")
