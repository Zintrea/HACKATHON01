import string

text = "WOYMLDFIGPBVZ"
key = "NEXUS_CART"

alphabet = string.ascii_uppercase

def vigenere_decrypt(text, key):
    result = ""
    key = key.replace("_", "")
    
    for i, c in enumerate(text):
        k = key[i % len(key)]
        
        t = alphabet.index(c)
        k = alphabet.index(k)
        
        result += alphabet[(t - k) % 26]
    
    return result

print(vigenere_decrypt(text, key))