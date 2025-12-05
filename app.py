from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import time

from decrypt_seed import decrypt_seed, load_private_key
from totp_utils import generate_totp_code, verify_totp_code

app = FastAPI()

class DecryptRequest(BaseModel):
    encrypted_seed: str

class VerifyRequest(BaseModel):
    code: str

DATA_PATH = "/data"
SEED_FILE = os.path.join(DATA_PATH, "seed.txt")

os.makedirs(DATA_PATH, exist_ok=True)

# Endpoint 1: POST /decrypt-seed
@app.post("/decrypt-seed")
def decrypt_seed_endpoint(body: DecryptRequest):
    try:
        private_key = load_private_key()
        hex_seed = decrypt_seed(body.encrypted_seed, private_key)  # validates 64-hex

        with open(SEED_FILE, "w", encoding="utf-8") as f:
            f.write(hex_seed)

        return {"status": "ok"}
    except Exception:
        raise HTTPException(status_code=500, detail="Decryption failed")

# Endpoint 2: GET /generate-2fa
@app.get("/generate-2fa")
def generate_2fa():
    if not os.path.exists(SEED_FILE):
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")

    with open(SEED_FILE, "r", encoding="utf-8") as f:
        hex_seed = f.read().strip()

    code = generate_totp_code(hex_seed)

    now = int(time.time())
    valid_for = 30 - (now % 30)  # 0–29 seconds remaining

    return {"code": code, "valid_for": valid_for}

# Endpoint 3: POST /verify-2fa
@app.post("/verify-2fa")
def verify_2fa(body: VerifyRequest):
    if not body.code:
        raise HTTPException(status_code=400, detail="Missing code")

    if not os.path.exists(SEED_FILE):
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")

    with open(SEED_FILE, "r", encoding="utf-8") as f:
        hex_seed = f.read().strip()

    is_valid = verify_totp_code(hex_seed, body.code, valid_window=1)
    return {"valid": bool(is_valid)}
