#!/usr/bin/env python3
"""
Optimized cracker focusing on likely patterns based on known Terraria seeds
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

def check_batch(batch):
    results = []
    for seed in batch:
        normalized = normalize_seed(seed)
        if not normalized:
            continue

        hashed = bcrypt.hashpw(normalized.encode('utf-8'), BCRYPT_SALT)
        hash_portion = hashed.decode('utf-8')[29:]
        hash_std = bcrypt_b64_to_std_b64(hash_portion)

        for effect, target in TARGETS.items():
            min_len = min(len(hash_std), len(target))
            if hash_std[:min_len] == target[:min_len]:
                results.append((effect, seed))
                break
    return results

# Looking at known Terraria seed patterns:
# "for the worthy" -> fortheworthy (3 words)
# "not the bees" -> notthebees (3 words)
# "drunk world" -> drunkworld (2 words)
# "the constant" -> theconstant (2 words)
# "get fixed boi" -> getfixedboi (3 words)
# "bring a towel" -> bringatowel (3 words)
# "i am error" -> iamerror (3 words)

# Patterns seem to be 2-4 common English words forming phrases

# Common English words for seed-like phrases
words1 = [
    # Starters
    "the", "a", "an", "my", "your", "our", "its", "this", "that",
    "i", "you", "we", "they", "he", "she", "it",
    "be", "am", "is", "are", "was", "were", "been",
    "have", "has", "had", "do", "does", "did",
    "get", "got", "let", "make", "made", "take", "took",
    "go", "went", "come", "came", "see", "saw", "find", "found",
    "give", "gave", "tell", "told", "ask", "asked",
    "use", "try", "need", "want", "like", "love", "hate",
    "think", "know", "feel", "believe", "remember", "forget",
    "here", "there", "where", "when", "why", "how", "what", "who",
    "all", "some", "any", "no", "not", "none", "each", "every",
    "more", "most", "less", "least", "much", "many", "few",
    "good", "bad", "great", "best", "worst", "better", "worse",
    "big", "small", "large", "little", "huge", "tiny",
    "old", "new", "young", "ancient", "modern",
    "high", "low", "up", "down", "top", "bottom",
    "first", "last", "next", "final", "only",
    "just", "still", "already", "yet", "never", "always", "ever",
    "very", "really", "quite", "too", "so", "such",
    "now", "then", "today", "tomorrow", "yesterday",
    "day", "night", "time", "year", "week", "month",
]

words2 = [
    # Middle/action words
    "on", "in", "at", "to", "for", "with", "from", "by", "of", "about",
    "into", "onto", "upon", "over", "under", "above", "below",
    "through", "across", "along", "around", "between", "among",
    "before", "after", "during", "until", "since", "while",
    "and", "or", "but", "if", "then", "else", "so", "yet",
    "can", "could", "will", "would", "shall", "should", "may", "might", "must",
]

words3 = [
    # End words / nouns
    "world", "earth", "land", "ground", "surface", "sky", "space", "heaven", "hell",
    "sun", "moon", "star", "light", "dark", "shadow", "fire", "water", "ice", "air",
    "king", "queen", "lord", "lady", "master", "god", "angel", "demon", "devil",
    "man", "woman", "boy", "girl", "child", "baby", "people", "person",
    "life", "death", "love", "hate", "war", "peace", "hope", "fear",
    "home", "house", "room", "door", "window", "wall", "floor", "roof",
    "way", "road", "path", "street", "place", "point", "end", "beginning",
    "hand", "eye", "head", "heart", "mind", "body", "soul", "spirit",
    "thing", "stuff", "part", "side", "name", "word", "story", "idea",
    "game", "play", "fun", "work", "job", "money", "power", "magic",
    "secret", "mystery", "treasure", "gold", "key", "lock", "code",
    "chest", "box", "bag", "pack", "gun", "sword", "shield", "armor",
    "dungeon", "castle", "tower", "cave", "forest", "mountain", "river", "sea",
    "hallow", "sacred", "holy", "blessed", "cursed", "evil", "good",
    "portal", "gate", "door", "warp", "rift", "void", "abyss",
    "twin", "dual", "double", "pair", "two", "second", "both",
]

def generate_phrases():
    # Two-word phrases
    for w1 in words1:
        for w2 in words3:
            yield f"{w1} {w2}"

    # Three-word phrases (word1 + word2 + word3)
    for w1 in words1[:30]:
        for w2 in words2[:20]:
            for w3 in words3[:50]:
                yield f"{w1} {w2} {w3}"

    # Three-word phrases (word1 + word3 + word3)
    for w1 in words1[:20]:
        for w2 in words3[:30]:
            for w3 in words3[:30]:
                yield f"{w1} {w2} {w3}"

    # Four-word phrases
    for w1 in words1[:15]:
        for w2 in words2[:10]:
            for w3 in words1[:10]:
                for w4 in words3[:20]:
                    yield f"{w1} {w2} {w3} {w4}"

def batch_gen(gen, size=500):
    batch = []
    for item in gen:
        batch.append(item)
        if len(batch) >= size:
            yield batch
            batch = []
    if batch:
        yield batch

if __name__ == '__main__':
    print(f"BCrypt salt: {BCRYPT_SALT.decode()}")
    print(f"Using {cpu_count()} CPU cores")
    print("Trying English phrase patterns...")
    sys.stdout.flush()

    found = {}
    count = 0

    with Pool(cpu_count()) as pool:
        for results in pool.imap_unordered(check_batch, batch_gen(generate_phrases())):
            count += 500
            if count % 50000 == 0:
                print(f"Progress: {count}")
                sys.stdout.flush()

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
