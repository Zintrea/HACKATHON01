import string

text = "WOYMLDFIGPBVZ"
key = "NEXUSCART"

alphabet = string.ascii_uppercase

def decrypt(text, key):
    result = ""
    
    for i, c in enumerate(text):
        t = alphabet.index(c)
        k = alphabet.index(key[i % len(key)])
        
        result += alphabet[(t - k) % 26]
    
    return result

print(decrypt(text, key))