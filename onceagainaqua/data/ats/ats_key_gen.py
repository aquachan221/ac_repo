import secrets
import hashlib
from datetime import datetime, UTC

def generate_aqua_api_key(purpose_text):
    purpose_hash = hashlib.sha256(purpose_text.encode()).hexdigest()[:8]
    now = datetime.now(UTC)
    date_str = now.strftime("%y%m%d")
    payload = secrets.token_hex(128)

    key = f"{date_str}_{purpose_hash}_{payload}"
    return key

# Example usage
purpose = "ts"
key = generate_aqua_api_key(purpose)
print(f"Aqua API Key:\n{key}")
print(f"Key length: {len(key)} characters")