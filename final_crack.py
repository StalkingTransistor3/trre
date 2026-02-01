#!/usr/bin/env python3
"""
Final comprehensive cracker - tries everything including unusual patterns
"""

import bcrypt
import re
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

def check_batch(batch):
    results = []
    for seed in batch:
        result = check_seed(seed)
        if result:
            results.append((result, seed))
    return results

# Generate final comprehensive list
candidates = []

# Song titles and lyrics
songs = [
    "here comes the sun", "let it be", "hey jude", "yesterday",
    "imagine", "bohemian rhapsody", "stairway to heaven", "hotel california",
    "sweet home alabama", "smells like teen spirit", "come as you are",
    "enter sandman", "nothing else matters", "one", "fade to black",
    "highway to hell", "back in black", "thunderstruck", "you shook me all night long",
    "we will rock you", "we are the champions", "dont stop me now", "killer queen",
    "under pressure", "another one bites the dust", "somebody to love",
    "smoke on the water", "purple haze", "all along the watchtower",
    "free bird", "simple man", "sweet emotion", "dream on",
    "crazy train", "mr crowley", "bark at the moon", "shot in the dark",
    "welcome to the jungle", "sweet child o mine", "paradise city",
    "livin on a prayer", "wanted dead or alive", "its my life",
    "pour some sugar on me", "photograph", "rock of ages",
    "eye of the tiger", "jump", "panama", "hot for teacher",
    "more than a feeling", "peace of mind", "foreplay longtime",
    "carry on wayward son", "dust in the wind", "point of know return",
    "dont fear the reaper", "burnin for you", "godzilla",
    "runnin with the devil", "aint talkin bout love", "eruption",
]
candidates.extend(songs)

# Book/movie quotes
quotes = [
    "to be or not to be", "all the worlds a stage", "what light through yonder window",
    "it was the best of times", "it was a dark and stormy night",
    "call me ishmael", "it is a truth universally acknowledged",
    "in a hole in the ground", "there lived a hobbit",
    "in the beginning", "let there be light", "and god said",
    "once upon a time", "happily ever after", "the end",
    "may the force be with you", "i am your father", "do or do not",
    "i see dead people", "heres looking at you kid", "frankly my dear",
    "youre gonna need a bigger boat", "say hello to my little friend",
    "ill be back", "hasta la vista baby", "come with me if you want to live",
    "houston we have a problem", "one small step for man", "space the final frontier",
    "these are not the droids", "help me obi wan kenobi", "use the force luke",
    "elementary my dear watson", "the game is afoot", "no shit sherlock",
    "bond james bond", "shaken not stirred", "the names bond",
    "life is like a box of chocolates", "run forrest run", "stupid is as stupid does",
    "here be dragons", "beyond here there be dragons", "terra incognita",
]
candidates.extend(quotes)

# Internet memes and culture
memes = [
    "doge", "much wow", "very scare", "so amaze", "such coin",
    "nyan cat", "keyboard cat", "ceiling cat", "longcat", "tacgnol",
    "all your base", "somebody set up us the bomb", "you have no chance to survive",
    "over 9000", "its over 9000", "what 9000", "thats impossible",
    "arrow to the knee", "i used to be an adventurer", "then i took an arrow",
    "do you even lift", "bro do you even lift", "come at me bro",
    "y u no", "forever alone", "okay face", "rage face",
    "one does not simply", "walk into mordor", "this is sparta",
    "winter is coming", "you know nothing", "jon snow",
    "hodor", "hold the door", "the north remembers",
    "bazinga", "soft kitty warm kitty", "penny penny penny",
    "thats what she said", "twss",
    "deez nuts", "got em", "ligma", "sugma", "bofa",
    "amogus", "sus", "when the imposter is sus", "red sus",
    "ez clap", "gg ez", "get rekt", "no scope", "360 no scope",
]
candidates.extend(memes)

# Terraria internal references
terraria = [
    "dig", "fight", "explore", "build",
    "terraria dig fight explore build",
    "guide voodoo doll", "wall of flesh summoning item",
    "suspicious looking eye", "suspicious looking skull",
    "mechanical eye", "mechanical skull", "mechanical worm",
    "night's edge", "true night's edge", "terra blade",
    "meowmere", "star wrath", "seedler", "influx waver",
    "zenith", "terraprisma", "last prism", "lunar flare",
    "solar eruption", "daybreak", "nebula arcanum", "nebula blaze",
    "vortex beater", "phantasm", "stardust cell staff", "stardust dragon staff",
    "for redigit", "for cenx", "for the devs", "thanks re logic",
    "dig peons", "dig peons dig", "peon",
    "andrew spinks", "whitney spinks", "cenx", "redigit",
    "re logic", "relogic", "505 games", "engine software",
    "thank you for playing", "thanks for playing terraria",
]
candidates.extend(terraria)

# Random ideas and experiments
random_ideas = [
    # Simple patterns
    "aaa", "bbb", "ccc", "abc", "xyz", "zzz",
    "111", "222", "333", "123", "321", "000",
    "a1", "b2", "c3", "1a", "2b", "3c",

    # Possible dev jokes
    "todo", "fixme", "hack", "bug", "debug",
    "null", "void", "none", "empty", "blank",
    "true", "false", "yes", "no", "maybe",
    "error", "undefined", "nan", "inf",

    # Common typos
    "teh", "pwn", "powned", "hax", "haxx", "h4x",
    "noob", "n00b", "newb", "scrub", "pleb",
    "leet", "l33t", "1337", "elite", "pro",

    # Programming references
    "foo", "bar", "baz", "qux", "quux",
    "hello world", "hello terraria", "hello hallow",
    "print hello", "echo hello", "console log",
    "main", "init", "start", "begin", "run",

    # Short codes
    "gg", "wp", "gl", "hf", "ns", "nt", "mb", "ty", "np",
    "lol", "lmao", "rofl", "xd", "kek", "kappa",
    "omg", "wtf", "bruh", "oof", "rip", "f",
    "pog", "poggers", "pogchamp", "monka", "pepe",

    # Effect-specific short
    "hs", "hos", "hots", "hot surface", "h on s",
    "pg", "pgic", "pgin", "gun chest", "g in c",
    "dd", "2d", "d2", "dual d", "2 dungeon",
]
candidates.extend(random_ideas)

def batch_gen(lst, size=500):
    for i in range(0, len(lst), size):
        yield lst[i:i+size]

if __name__ == '__main__':
    print(f"BCrypt salt: {BCRYPT_SALT.decode()}")
    print(f"Testing {len(candidates)} candidates...")
    sys.stdout.flush()

    found = {}

    with Pool(cpu_count()) as pool:
        for results in pool.imap_unordered(check_batch, batch_gen(candidates)):
            for effect, seed in results:
                print(f"\n*** FOUND: {effect} = '{seed}' ***\n")
                found[effect] = seed
                sys.stdout.flush()

    print(f"\n=== RESULTS ===")
    for effect, seed in found.items():
        print(f"{effect}: {seed}")

    remaining = set(TARGETS.keys()) - set(found.keys())
    if remaining:
        print(f"\nNot found: {remaining}")
