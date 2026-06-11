import string

cipher = "WOYMLDFIGPBVZ"

# alphabet ที่มีในระบบ
custom_alpha = "ABCDEFGILMNOPRSTUVWXYZ_"

# map A-Z ปกติ -> custom alphabet
plain = string.ascii_uppercase + "_"

mapping = {c: p for c, p in zip(custom_alpha, plain)}

decoded = "".join(mapping.get(c, "?") for c in cipher)

print(decoded)