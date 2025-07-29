import secrets

def generate_six_digit_code():
    return f"{secrets.randbelow(1000000):06}"

# Example usage:
code = generate_six_digit_code()
print("Your verification code is:", code)