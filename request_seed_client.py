import requests

def request_seed(student_id: str, github_repo_url: str, api_url: str) -> None:
    # 1) Read student public key from PEM file
    with open("student_public.pem", "r", encoding="utf-8") as f:
        public_key = f.read()  # keep BEGIN/END lines and newlines

    # 2) Prepare JSON payload
    payload = {
        "student_id": student_id,
        "github_repo_url": github_repo_url,
        "public_key": public_key
    }

    # 3) Send POST request to instructor API
    response = requests.post(api_url, json=payload, timeout=10)
    response.raise_for_status()          # raise if HTTP error

    data = response.json()

    # 4) Parse JSON response
    encrypted_seed = data["encrypted_seed"]

    # 5) Save encrypted seed to file (do NOT commit this file)
    with open("encrypted_seed.txt", "w", encoding="utf-8") as f:
        f.write(encrypted_seed)

if __name__ == "__main__":
    request_seed(
        student_id="23A91A05B6",
        github_repo_url="https://github.com/GowriPravallika26/pki-2fa.git",  # your exact repo URL
        api_url="https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws"  # copy exactly from assignment
    )
