from datetime import datetime, timezone

def load_hash_table(filename="hash_table.txt"):
    hash_map = {}
    try:
        with open(filename, "r") as file:
            for line in file:
                if ":" in line:
                    hash_val, label = line.strip().split(":", 1)
                    hash_map[hash_val] = label
    except FileNotFoundError:
        return None
    return hash_map

def read_aqua_api_key(api_key, hash_table_path="hash_table.txt"):
    try:
        date_str, purpose_hash, payload = api_key.split("_")
        created_date = datetime.strptime(date_str, "%y%m%d").date()
        today = datetime.now(timezone.utc).date()
        in_date = today >= created_date

        hash_map = load_hash_table(hash_table_path)
        if hash_map is None:
            decoded_purpose = "hash_table.txt not found"
        else:
            decoded_purpose = hash_map.get(purpose_hash, "unknown")

        return {
            "created_date": created_date.isoformat(),
            "is_in_date": in_date,
            "hashed_purpose": purpose_hash,
            "decoded_purpose": decoded_purpose,
            "payload": payload,
            "payload_length": len(payload)
        }
    except ValueError:
        return {"error": "Invalid key format. Expected: DATE_HASH_PAYLOAD"}

key = "250711_44ad63f6_f1d56e32765488babf5239517e43a2694e4ddcd4b34352e2c54db82dd60cfdfc0c71688cf4385efadba7943f56be7ef157e32ff4a82d40be3f63eb68fabc4760986cf377d38c023abb252fdd0adbe8fddef4a5e2e90919b260351d365aab6084fc1ea1ac963a9d488e23f333975a18665a4c3f19f95ade6e7917d6cca89ec403"
result = read_aqua_api_key(key)
print(result)