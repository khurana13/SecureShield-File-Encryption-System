import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from utils import derive_key, SALT_SIZE, NONCE_SIZE

def encrypt_file(file_path: str, password: str, output_dir: str = "encrypted_files") -> str:
    """
    Encrypts a file using AES-GCM and saves it to the output directory.
    Format: [SALT (16 bytes)][NONCE (12 bytes)][CIPHERTEXT]
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    # Read original file data
    with open(file_path, "rb") as f:
        data = f.read()

    # Generate salt and derive key
    salt = os.urandom(SALT_SIZE)
    key = derive_key(password, salt)

    # Encrypt data
    aesgcm = AESGCM(key)
    nonce = os.urandom(NONCE_SIZE)
    ciphertext = aesgcm.encrypt(nonce, data, None)

    # Prepare output filename
    base_name = os.path.basename(file_path)
    encrypted_filename = f"{base_name}.enc"
    output_path = os.path.join(output_dir, encrypted_filename)

    # Save to binary file
    with open(output_path, "wb") as f:
        f.write(salt)
        f.write(nonce)
        f.write(ciphertext)

    return output_path
