import base64
import pyotp
def generate_totp_code(hex_seed: str) -> str:
    # 1) Convert hex seed to bytes
    seed_bytes = bytes.fromhex(hex_seed)  # 64-hex -> 32 bytes

    # 2) Convert bytes to base32 string
    base32_seed = base64.b32encode(seed_bytes).decode("utf-8")

    # 3) Create TOTP object (SHA1, 30s, 6 digits are pyotp defaults)
    totp = pyotp.TOTP(base32_seed, digits=6, interval=30)  # algorithm=SHA1 by default [web:136][web:140]

    # 4) Generate current TOTP code
    code = totp.now()  # returns 6-digit string [web:136][web:142]

    # 5) Return code
    return code
def verify_totp_code(hex_seed: str, code: str, valid_window: int = 1) -> bool:
    # 1) Convert hex seed to base32 (same as above)
    seed_bytes = bytes.fromhex(hex_seed)
    base32_seed = base64.b32encode(seed_bytes).decode("utf-8")

    # 2) Create TOTP object with base32 seed
    totp = pyotp.TOTP(base32_seed, digits=6, interval=30)  # SHA1 default [web:136][web:140]

    # 3) Verify code with time window tolerance
    # valid_window=1 means accept codes one step before/after current (±30s) [web:136]
    is_valid = totp.verify(code, valid_window=valid_window)

    # 4) Return verification result
    return is_valid
if __name__ == "__main__":
    from decrypt_seed import decrypt_seed, load_private_key, read_encrypted_seed

    # Get hex seed via decryption
    private_key = load_private_key()
    encrypted_seed_b64 = read_encrypted_seed()
    hex_seed = decrypt_seed(encrypted_seed_b64, private_key)

    code = generate_totp_code(hex_seed)
    print("Current TOTP code:", code)

    print("Verify (should be True):", verify_totp_code(hex_seed, code))
