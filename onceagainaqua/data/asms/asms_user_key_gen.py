import secrets

def generate_six_digit_code():
    return f"{secrets.randbelow(1000000):06}"

key_purpose="asms"

code = generate_six_digit_code()
print(f"{key_purpose}{code}")
#stupid ai trying to move key_purpose to the middle
#its still trying to
#print(f"Your verification code for {key_purpose} is: {code}")
#no idiot
#and code is a function so it doesnt need to be in {}
##it is not a variable
#it is a function that returns a string
#way to go ai
#good job