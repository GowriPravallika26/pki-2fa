#!/usr/bin/env python3

# Cron script to log 2FA codes every minute

import os
import sys
from datetime import datetime, timezone

# add /app directory (where totp_utils.py lives) to sys.path
sys.path.append("/app")
from totp_utils import generate_totp_code  # reuse your function

SEED_FILE = "/data/seed.txt"

def main():
    # 1. Read hex seed
    try:
        with open(SEED_FILE, "r", encoding="utf-8") as f:
            hex_seed = f.read().strip()
        if not hex_seed:
            print("No seed in file")
            return
    except FileNotFoundError:
        print("Seed file not found")
        return

    # 2. Generate current TOTP code
    code = generate_totp_code(hex_seed)

    # 3. Current UTC timestamp
    now_utc = datetime.now(timezone.utc)
    ts = now_utc.strftime("%Y-%m-%d %H:%M:%S")

    # 4. Output formatted line
    print(f"{ts} - 2FA Code: {code}")

if __name__ == "__main__":
    main()