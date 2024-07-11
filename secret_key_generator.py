"""
This module is for generating secret keys for the database configuration.
You can choose from the three which type of key you want to generate.
"""

import os
import secrets

# Generate a random secret key
os_secret_key = os.urandom(24)
print("os_generated:", os_secret_key) # 24 bytes for a secure key

s_secret_key = secrets.token_hex(16)  # Generate a random 32-character hexadecimal string (16 bytes)
print("\nsecrets_generated:", s_secret_key)

by_secret_key = secrets.token_bytes(24)  # Generate a random 24-byte string
print("\ntoken bytes", by_secret_key.hex())

"""
Flask recommends using a secure random generator to ensure the key is unpredictable and secure. Here are a few methods you can use:
Using os.urandom()

Python's os.urandom() function provides a suitable source of randomness for generating secure keys. It returns random bytes suitable for cryptographic use.

python

import os

secret_key = os.urandom(24)  # Generate a random 24-byte string
print(secret_key.hex())

Using secrets.token_hex()

The secrets module in Python provides functions for generating secure tokens, including hex-encoded strings that can be used as secret keys.

python

import secrets

secret_key = secrets.token_hex(16)  # Generate a random 32-character hexadecimal string (16 bytes)
print(secret_key)

Using secrets.token_bytes()

Another function from the secrets module is token_bytes(), which generates random bytes that can be directly used as a secret key.

python

import secrets

secret_key = secrets.token_bytes(24)  # Generate a random 24-byte string
print(secret_key.hex())

Recommendations

    Length of the Secret Key: Flask recommends using a key with at least 24 bytes (32 characters) for security.
    Storing the Key: Store the generated secret key securely and avoid exposing it in public repositories or environments.
    Regeneration: If the secret key is compromised or needs to be changed, regenerate it using one of the methods above and update your application configuration accordingly.

Choose the method that best fits your application's security requirements and ensure you store the secret key safely in your application configuration (app.config['SECRET_KEY']) and in your db.yaml file if needed.
"""