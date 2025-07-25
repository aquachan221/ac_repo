from datetime import datetime, timedelta, UTC

# Example usage
unified_key = "250711_9f86d081_42c8b2c929095a06a452967181f784e4"
lifespan_days = 45

try:
    date_str, hashed_purpose, secret = unified_key.split("_")

    created_date = datetime.strptime(date_str, "%y%m%d").date()
    expires_date = created_date + timedelta(days=lifespan_days)
    today = datetime.now(UTC).date()  # Timezone-aware now

    expired = today > expires_date

    decoded = {
        "created_date": created_date.isoformat(),
        "expires_at": expires_date.isoformat(),
        "is_expired": expired,
        "hashed_purpose": hashed_purpose,
        "key_payload": secret
    }
except ValueError:
    decoded = {
        "error": "Invalid key format. Expected format: DATE_HASH_PURPOSE"
    }

print(decoded)