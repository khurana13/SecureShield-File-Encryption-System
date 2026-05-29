import os
import hashlib
import base64
import json
from datetime import datetime
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Constants
SALT_SIZE = 16
NONCE_SIZE = 12
ITERATIONS = 100000

def derive_key(password: str, salt: bytes) -> bytes:
    """Derives a 32-byte key from a password and salt using PBKDF2."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=ITERATIONS,
    )
    return kdf.derive(password.encode())

def get_file_hash(file_path: str) -> str:
    """Generates a SHA-256 hash of a file for integrity verification."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def check_password_strength(password: str) -> tuple:
    """Checks if a password is strong (min 8 chars, 1 digit, 1 special)."""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not any(char.isdigit() for char in password):
        return False, "Password must contain at least one digit."
    if not any(not char.isalnum() for char in password):
        return False, "Password must contain at least one special character."
    return True, "Strong password."

HISTORY_FILE = "history.json"

def log_action(action: str, original_path: str, output_path: str):
    """Logs an encryption or decryption action to history.json."""
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "action": action,
        "filename": os.path.basename(original_path),
        "output_path": os.path.abspath(output_path)
    }
    
    history = []
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                history = json.load(f)
        except:
            history = []
            
    history.insert(0, entry)  # Add new entry at the top
    
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

def get_history():
    """Returns the history list from history.json."""
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except:
        return []
