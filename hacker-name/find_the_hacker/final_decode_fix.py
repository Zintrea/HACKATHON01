import string

cipher = "WOYMLDFIGPBVZ"

custom_alpha = "ABCDEFGILMNOPRSTUVWXYZ_"

# สร้าง reverse index แบบ positional
decoded = ""

for c in cipher:
    if c in custom_alpha:
        idx = custom_alpha.index(c)
        decoded += string.ascii_uppercase[idx]
    else:
        decoded += "?"

print(decoded)