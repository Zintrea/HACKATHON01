# Suffix Pattern Hunt — Endpoint Variants

> Purpose: ตรวจ endpoint แปลก ๆ ที่เติม suffix หลัง endpoint ปกติ เช่น `/cart_`, `/searchE`, `/productsA` แล้วเรียง suffix เพื่อดู clue ที่อาจซ่อนอยู่

## Method

- Source: `output/endpoint_summary.csv`
- ใช้ `endpoint_summary.csv` เพราะเป็น output ที่รวม endpoint และ status split แล้ว ไม่ต้องไล่อ่าน raw log manual
- เทียบ endpoint กับ base ปกติ: `/cart`, `/search`, `/products`, `/checkout`, `/api/v1/user`, `/index.html`
- ถ้ามีตัวอักษร/สัญลักษณ์ต่อท้าย และ endpoint นั้นมี `status_5xx > 0` จะถือเป็น suspicious suffix variant
- เรียง suffix ตาม `first_rank` คืออันดับแรกที่ suffix นั้นปรากฏใน endpoint_summary ซึ่งถูก sort ตาม impact/error pattern

## Ordered Suffixes

```text
_EASRTOLNUYWIMGFDZXVBPC
```

## Suffix Table

| Order | Suffix | Total 5xx | Status 500 | Status 504 | Endpoint Count | Max Unique IPs | Examples |
|---:|---|---:|---:|---:|---:|---:|---|
| 1 | `_` | 914673 | 458468 | 456205 | 6 | 19 | `/cart_;/search_;/api/v1/user_;/products_;/checkout_;/index_.html` |
| 2 | `E` | 679253 | 339596 | 339657 | 6 | 19 | `/searchE;/indexE.html;/cartE;/productsE;/api/v1/userE;/checkoutE` |
| 3 | `A` | 589133 | 294892 | 294241 | 6 | 19 | `/api/v1/userA;/productsA;/cartA;/checkoutA;/searchA;/indexA.html` |
| 4 | `S` | 357632 | 179019 | 178613 | 6 | 19 | `/checkoutS;/api/v1/userS;/cartS;/searchS;/indexS.html;/productsS` |
| 5 | `R` | 332698 | 166291 | 166407 | 6 | 19 | `/searchR;/checkoutR;/productsR;/cartR;/indexR.html;/api/v1/userR` |
| 6 | `T` | 315862 | 157754 | 158108 | 6 | 19 | `/cartT;/api/v1/userT;/searchT;/productsT;/checkoutT;/indexT.html` |
| 7 | `O` | 306732 | 153901 | 152831 | 6 | 19 | `/checkoutO;/indexO.html;/productsO;/cartO;/api/v1/userO;/searchO` |
| 8 | `L` | 207519 | 103816 | 103703 | 6 | 19 | `/indexL.html;/productsL;/checkoutL;/cartL;/api/v1/userL;/searchL` |
| 9 | `N` | 196493 | 97954 | 98539 | 6 | 19 | `/checkoutN;/cartN;/productsN;/indexN.html;/searchN;/api/v1/userN` |
| 10 | `U` | 192295 | 96166 | 96129 | 6 | 19 | `/cartU;/checkoutU;/api/v1/userU;/searchU;/productsU;/indexU.html` |
| 11 | `Y` | 189126 | 93850 | 95276 | 6 | 19 | `/api/v1/userY;/productsY;/cartY;/checkoutY;/indexY.html;/searchY` |
| 12 | `W` | 152426 | 76274 | 76152 | 6 | 19 | `/searchW;/cartW;/indexW.html;/productsW;/api/v1/userW;/checkoutW` |
| 13 | `I` | 150682 | 75184 | 75498 | 6 | 19 | `/checkoutI;/api/v1/userI;/indexI.html;/searchI;/cartI;/productsI` |
| 14 | `M` | 145520 | 72937 | 72583 | 6 | 19 | `/api/v1/userM;/checkoutM;/searchM;/cartM;/indexM.html;/productsM` |
| 15 | `G` | 97010 | 48573 | 48437 | 6 | 19 | `/searchG;/checkoutG;/productsG;/indexG.html;/api/v1/userG;/cartG` |
| 16 | `F` | 81332 | 40590 | 40742 | 6 | 19 | `/searchF;/productsF;/cartF;/api/v1/userF;/checkoutF;/indexF.html` |
| 17 | `D` | 79990 | 40046 | 39944 | 6 | 19 | `/indexD.html;/api/v1/userD;/cartD;/productsD;/searchD;/checkoutD` |
| 18 | `Z` | 70896 | 35244 | 35652 | 6 | 19 | `/searchZ;/cartZ;/checkoutZ;/indexZ.html;/api/v1/userZ;/productsZ` |
| 19 | `X` | 70783 | 35297 | 35486 | 6 | 19 | `/productsX;/searchX;/api/v1/userX;/indexX.html;/cartX;/checkoutX` |
| 20 | `V` | 68715 | 34157 | 34558 | 6 | 19 | `/cartV;/indexV.html;/productsV;/searchV;/api/v1/userV;/checkoutV` |
| 21 | `B` | 65738 | 32920 | 32818 | 6 | 19 | `/api/v1/userB;/productsB;/cartB;/checkoutB;/searchB;/indexB.html` |
| 22 | `P` | 54849 | 27311 | 27538 | 6 | 19 | `/api/v1/userP;/searchP;/indexP.html;/checkoutP;/productsP;/cartP` |
| 23 | `C` | 53544 | 26767 | 26777 | 6 | 19 | `/searchC;/cartC;/indexC.html;/productsC;/api/v1/userC;/checkoutC` |

## Interpretation

- ถ้า suffix ที่เรียงได้กลายเป็นคำ/วลี อาจเป็น hidden clue หรือ signature ของ attacker
- ถ้า suffix มีหลาย endpoint ต่อ base เดียวกัน แปลว่า attacker ยิง pattern เป็นชุด ไม่ใช่ path เดี่ยว
- ต้อง validate ต่อด้วย raw evidence หรือ suspicious IP group ก่อนฟันธงว่าเป็น hidden bonus

## Presentation wording

> We noticed that suspicious endpoints are not random. They are normal endpoints with added suffix characters. By grouping these suffixes in impact order, the sequence becomes a potential hidden clue and also explains the attack pattern.
