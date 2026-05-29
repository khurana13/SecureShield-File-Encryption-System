import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from utils import derive_key, SALT_SIZE, NONCE_SIZE

def decrypt_file(encrypted_file_path: str, password: str, output_dir: str = "decrypted_files") -> str:
    """
    Decrypts a file using AES-GCM and restores the original content.
    Expects format: [SALT (16 bytes)][NONCE (12 bytes)][CIPHERTEXT]
    """
    if not os.path.exists(encrypted_file_path):
        raise FileNotFoundError(f"File not found: {encrypted_file_path}")

    with open(encrypted_file_path, "rb") as f:
        salt = f.read(SALT_SIZE)
        nonce = f.read(NONCE_SIZE)
        ciphertext = f.read()

    # Derive key using the same salt and password
    key = derive_key(password, salt)

    # Decrypt data
    aesgcm = AESGCM(key)
    try:
        decrypted_data = aesgcm.decrypt(nonce, ciphertext, None)
    except Exception:
        raise ValueError("Invalid password or corrupted file.")

    # Prepare output filename (remove .enc extension)
    base_name = os.path.basename(encrypted_file_path)
    if base_name.endswith(".enc"):
        decrypted_filename = base_name[:-4]
    else:
        decrypted_filename = f"decrypted_{base_name}"
    
    output_path = os.path.join(output_dir, decrypted_filename)

    # Save original file data
    with open(output_path, "wb") as f:
        f.write(decrypted_data)

    return output_path
