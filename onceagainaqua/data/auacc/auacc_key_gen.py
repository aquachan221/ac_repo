import datetime
import base64
import json
import os
import secrets

MARKER = "::END::"

def create_user_base64(username: str, is_verified: bool, is_trusted: bool) -> str:
    now_utc = datetime.datetime.now(datetime.UTC)
    formatted_time = now_utc.strftime("%Y-%m-%dT%H:%M:%SZ")

    raw_string = f"{username}{formatted_time}{int(is_verified)}{int(is_trusted)}"
    base64_encoded = base64.b64encode(raw_string.encode('utf-8')).decode('utf-8')

    marked_base64 = base64_encoded + MARKER

    max_length = 512
    remaining_length = max_length - len(marked_base64)

    if remaining_length > 0:
        random_bytes = secrets.token_bytes(remaining_length)
        random_base64 = base64.b64encode(random_bytes).decode('utf-8')
        marked_base64 += random_base64[:remaining_length]

    return marked_base64

def decode_user_base64(base64_code: str) -> dict:
    try:
        original_base64 = base64_code.split(MARKER)[0]
        decoded_str = base64.b64decode(original_base64.encode('utf-8')).decode('utf-8', errors='ignore')

        timestamp_index = decoded_str.find("T") - 10
        username = decoded_str[:timestamp_index]
        created_at = decoded_str[timestamp_index:timestamp_index + 20]
        is_verified = bool(int(decoded_str[timestamp_index + 20]))
        is_trusted = bool(int(decoded_str[timestamp_index + 21]))

        if not username or len(created_at) != 20:
            raise ValueError("Invalid structure")

        return {
            "username": username,
            "created_at": created_at,
            "is_verified": is_verified,
            "is_trusted": is_trusted
        }
    except Exception:
        return None

def write_user_to_file(base64_code: str, decoded_data: dict, password: str,
                       first_name: str, last_name: str, gender: str,
                       filename: str = "acuacc.json"):
    if decoded_data is None:
        print("Skipped writing: decoded data is invalid.")
        return

    user_entry = {
        "base64_code": base64_code,
        "password": password,
        "first_name": first_name,
        "last_name": last_name,
        "gender": gender,
        **decoded_data
    }

    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if not isinstance(data, list):
                    data = [data]
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    data.append(user_entry)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

# 🧑‍💻 Example usage — organized user input!
user_info = {
    "username": "sigmascout69",
    "password": "sigmarizz69",
    "first_name": "goon",
    "last_name": "gooner",
    "gender": "none of the above",
    "is_verified": True,
    "is_trusted": True
}

base64_code = create_user_base64(
    user_info["username"],
    user_info["is_verified"],
    user_info["is_trusted"]
)

decoded = decode_user_base64(base64_code)

write_user_to_file(
    base64_code,
    decoded,
    password=user_info["password"],
    first_name=user_info["first_name"],
    last_name=user_info["last_name"],
    gender=user_info["gender"]
)

print("woo!")