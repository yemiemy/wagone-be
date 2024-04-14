import random
import string
import hashlib
from core.utils import get_uuid


def generate_code():
    return random.SystemRandom().randrange(100000, 999999)


def generate_hash(val):
    return hashlib.sha256(get_uuid().encode() + val.encode()).hexdigest()


def avatar_file_name(instance, filename):
    return "/".join(
        [
            "images",
            "avatars",
            "{}_{}_{}".format(instance.username, get_uuid(), filename).lower(),
        ]
    )


def generate_random_password(length=16):
    """Generates a random string of the specified length with at least one
    uppercase, lowercase, digit and punctuation character.

    Args:
      length: The desired length of the random string (default: 16).

    Returns:
      A random string of the specified length.
    """

    all_chars = string.ascii_letters + string.digits + string.punctuation
    char_sets = [
        string.ascii_uppercase,
        string.ascii_lowercase,
        string.digits,
        string.punctuation,
    ]

    # Guarantee at least one character from each character set
    guaranteed_chars = "".join(
        random.choice(char_set) for char_set in char_sets
    )

    # Fill the remaining characters with random selections from the entire pool
    remaining_chars = random.sample(all_chars, length - len(guaranteed_chars))

    # Combine guaranteed and random characters
    final_string = guaranteed_chars + "".join(remaining_chars)

    # Shuffle the final string for better randomness
    return "".join(random.sample(final_string, len(final_string)))
