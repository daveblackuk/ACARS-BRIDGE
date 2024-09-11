import hashlib
import random
import string

def generate_random_4_letter_string(base_string):
    # Ensure the base_string is exactly 12 characters
    if len(base_string) != 12:
        raise ValueError("Base string must be exactly 12 characters long")

    # Hash the base string using SHA-256
    hash_object = hashlib.sha256(base_string.encode())
    hex_dig = hash_object.hexdigest()

    # Seed the random number generator with a portion of the hash
    random.seed(hex_dig[:8])  # Use the first 8 characters of the hash for seeding

    # Define the character set
    chars = string.ascii_letters  # Use letters only

    # Generate a random 4-letter string
    random_4_letter_string = ''.join(random.choice(chars) for _ in range(4))

    return random_4_letter_string.upper()

