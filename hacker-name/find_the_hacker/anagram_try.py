from itertools import permutations

text = "WOYMLDFIGPBVZ"

# จำกัดแค่ลองบางชุดก่อน (ไม่งั้นระเบิดเวลา)
for p in permutations(text, 6):
    word = "".join(p)
    print(word)
    break