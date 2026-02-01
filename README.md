# Terraria Seed Cracker

Tools for cracking BCrypt-hashed Terraria secret seeds.

## Target Seeds (Still Unknown)

| Effect | Hash |
|--------|------|
| hallowOnTheSurface | KYvKIk2LK0oyNY86m+uPhKQ7QbzFmDsRpo |
| portalGunInChests | ALdQZ+bxQA4VdfjVfdhO/sm9q3sZD9dJ |
| dualDungeons | ypBuvKpqKay//OvhG2COriSpGT7f4YY3 |

## Verification Method

1. Take seed string
2. Lowercase it
3. Keep only a-z and 0-9
4. BCrypt hash with salt `fT2JQQzNMJl2NRoMbo9RjA==` (cost 4)
5. Compare with target hash

## Tools

- `crack_seeds.py` - Basic cracker with special Terraria seeds
- `verify_seed.py` - Verify specific seeds against targets
- `pop_culture_crack.py` - Try pop culture references
- `terraria_words_crack.py` - Terraria-specific terminology
- `dictionary_crack.py` - Dictionary-based attack
- `parallel_crack.py` - Multi-threaded brute force
- `short_crack.py` - Exhaustive short string search
- `focused_crack.py` - Short alphanumeric strings
- `intensive_crack.py` - Intensive wordlist attack
- `creative_crack.py` - Dates, versions, patterns

## Usage

```bash
pip install bcrypt
python3 crack_seeds.py
```

## Status

These seeds are currently undiscovered by the Terraria community. The effect names are known from decompiled source code, but the actual seed strings that activate them remain encrypted/unknown.
