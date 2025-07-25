import unicodedata

def print_char_info(code_point):
    cp_int = int(code_point.replace('U+', ''), 16)
    char = chr(cp_int)
    name = unicodedata.name(char, 'Unknown Character')
    print(f"{code_point} → '{char}' ({name})")

# Examples of "invisible-ish" characters
print_char_info('U+2063')  # INVISIBLE SEPARATOR
print_char_info('U+00A0')  # NO-BREAK SPACE
print_char_info('U+200C')  # ZERO WIDTH NON-JOINER
print_char_info('U+200D')  # ZERO WIDTH JOINER
print_char_info('U+2800')  # Braille Pattern Blank