# SecureShield-File-Encryption-System

## Overview

SecureShield is a Python-based File Encryption and Decryption System developed to securely protect sensitive files from unauthorized access using modern cryptographic techniques.

The application uses AES-256 encryption in GCM mode along with password-based authentication to ensure confidentiality, integrity, and secure access control. The project also includes a user-friendly graphical interface for performing encryption and decryption operations efficiently.

---

## Features

* AES-256 File Encryption
* AES-GCM Authenticated Encryption
* Password-Based Authentication
* PBKDF2 Secure Key Derivation
* SHA-256 Integrity Verification
* GUI-Based File Encryption System
* Secure File Handling
* Encryption & Decryption History Logging
* Password Strength Validation

---

## Technologies Used

* Python 3.x
* Tkinter
* Cryptography Library
* Hashlib
* OS Module
* JSON
* File Handling

---

## Project Structure

```bash id="1gkp1j"
SecureShield/
│
├── encrypt.py
├── decrypt.py
├── gui.py
├── utils.py
├── main.py
├── requirements.txt
├── history.json
├── README.md
├── encrypted_files/
└── decrypted_files/
```

---

## How the System Works

1. User selects a file.
2. User enters a secure password.
3. PBKDF2 derives a secure encryption key.
4. AES-GCM encrypts the file contents.
5. Encrypted data is stored securely.
6. During decryption, the same password regenerates the key.
7. The file is restored only if authentication succeeds.

---

## Security Mechanisms Used

### AES-256 Encryption

The project uses AES-GCM mode, which provides:

* Data Confidentiality
* Authentication
* Integrity Protection

### PBKDF2 Key Derivation

Passwords are converted into secure cryptographic keys using PBKDF2 with SHA-256 hashing and multiple iterations.

### SHA-256 Hashing

Used for integrity verification and secure hashing operations.

### Random Salt and Nonce Generation

Every encryption process generates:

* Unique Salt
* Unique Nonce

This improves security and prevents replay attacks.

---

## GUI Features

The graphical user interface allows users to:

* Browse and select files
* Encrypt files securely
* Decrypt encrypted files
* Enter secure passwords
* Toggle password visibility
* View encryption/decryption history

---

## Installation

### Clone Repository

```bash id="jlwm5y"
git clone https://github.com/your-username/SecureShield.git
cd SecureShield
```

### Install Dependencies

```bash id="3jts2s"
pip install -r requirements.txt
```

### Run Application

```bash id="0mk8wh"
python main.py
```

---

## Data Structures and Algorithms Used

### Data Structures

* Strings
* Lists
* Dictionaries
* Binary File Buffers

### Algorithms

* AES Encryption Algorithm
* PBKDF2 Key Derivation
* SHA-256 Hashing
* Password Validation Algorithm
* File Handling Algorithms

---

## Learning Outcomes

This project helped in understanding:

* Applied Cryptography
* Cybersecurity Fundamentals
* Secure File Storage
* AES-GCM Encryption
* Hashing Techniques
* GUI Development in Python
* Secure Key Management
* Modular Programming

---

## Future Enhancements

* Drag-and-drop file support
* Multi-file encryption
* Cloud storage integration
* Biometric authentication
* Malware scanning before encryption
* Secure file sharing
* Cross-platform mobile support

---

## Results

The system successfully encrypts and decrypts files while ensuring:

* Data Confidentiality
* File Integrity
* Secure Authentication
* Efficient File Protection

The project demonstrates the practical implementation of cybersecurity concepts in a real-world desktop application.

---

## References

1. Python Cryptography Documentation
2. NIST AES Encryption Standards
3. PBKDF2 Documentation
4. SHA-256 Cryptographic Standards
5. Python Tkinter Documentation
6. Python Official Documentation
7. Cryptography Library Documentation

---

