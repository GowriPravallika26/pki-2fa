import base64
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
def decrypt_seed(encrypted_seed_b64: str, private_key) -> str:
    # 1) Base64 decode the encrypted seed string
    ciphertext = base64.b64decode(encrypted_seed_b64)

    # 2) RSA/OAEP decrypt with SHA-256
    plaintext_bytes = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

    # 3) Decode bytes to UTF-8 string
    hex_seed = plaintext_bytes.decode("utf-8")

    # 4) Validate: must be 64-character hex string
    if len(hex_seed) != 64:
        raise ValueError("Seed length is not 64 characters")

    allowed = set("0123456789abcdef")
    if not set(hex_seed).issubset(allowed):
        raise ValueError("Seed is not hexadecimal")

    # 5) Return hex seed
    return hex_seed
def load_private_key():
    with open("student_private.pem", "rb") as f:
        key_data = f.read()
    return serialization.load_pem_private_key(
        key_data,
        password=None,
        backend=default_backend(),
    )

def read_encrypted_seed():
    with open("encrypted_seed.txt", "r", encoding="utf-8") as f:
        return f.read().strip()

if __name__ == "__main__":
    private_key = load_private_key()
    encrypted_seed_b64 = read_encrypted_seed()
    hex_seed = decrypt_seed(encrypted_seed_b64, private_key)
    print("Decrypted seed:", hex_seed)
