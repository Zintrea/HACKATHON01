text = "WOYMLDFIGPBVZ"

def shift(s, k):
    out = ""
    for c in s:
        if c.isalpha():
            out += chr((ord(c) - ord('A') + k) % 26 + ord('A'))
        else:
            out += c
    return out

for k in range(1, 26):
    print(k, shift(text, k))