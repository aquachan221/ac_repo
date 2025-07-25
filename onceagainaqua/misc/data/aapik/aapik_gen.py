import secrets
from datetime import datetime, timedelta, UTC
import hashlib

def generate_aqua_api_key(purpose="general", length=32, expires_in_days=45):
    created = datetime.now(UTC)
    expires = created + timedelta(days=expires_in_days)

    # Date prefix
    date_prefix = created.strftime("%y%m%d")  # e.g. "250711"

    # Hashed/encrypted purpose (shortened to 8 chars for brevity)
    hashed_purpose = hashlib.sha256(purpose.encode()).hexdigest()[:8]

    # Secure random hex
    secret_key = secrets.token_hex(length // 2)  # 32-character total

    # Unified string
    unified_key = f"{date_prefix}_{hashed_purpose}_{secret_key}"

    return {
        "key": unified_key,
        "purpose": purpose,
        "created_at": created.isoformat(),
        "expires_at": expires.isoformat()
    }

# Example usage
api_key_data = generate_aqua_api_key("test")
print(f"🔐 Key: {api_key_data['key']}")
print(f"📦 Purpose: {api_key_data['purpose']}")
print(f"📅 Created: {api_key_data['created_at']}")
print(f"⏳ Expires: {api_key_data['expires_at']}")