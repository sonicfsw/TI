import numpy as np
from math import comb


def entropy(probabilities):
    return -sum(p * np.log2(p) for p in probabilities if p > 0)

total1 = 7
blue1 = 4
white1 = 3

P_SS = comb(blue1, 2) / comb(total1, 2)
P_SB = (comb(blue1, 1) * comb(white1, 1)) / comb(total1, 2)
P_BB = comb(white1, 2) / comb(total1, 2)


H1 = entropy([P_SS, P_SB, P_BB])

total2 = 16
blue2 = 11
white2 = 5


P_SSS = comb(blue2, 3) / comb(total2, 3)
P_SSB = (comb(blue2, 2) * comb(white2, 1)) / comb(total2, 3)
P_SBB = (comb(blue2, 1) * comb(white2, 2)) / comb(total2, 3)
P_BBB = comb(white2, 3) / comb(total2, 3)

H2 = entropy([P_SSS, P_SSB, P_SBB, P_BBB])


print("Первая урна (выбор 2 шаров):")
print(f"P(SS)  = {P_SS:.4f} (два синих)")
print(f"P(SB)  = {P_SB:.4f} (один синий, один белый)")
print(f"P(BB)  = {P_BB:.4f} (два белых)")
print(f"Энтропия первой урны: H1 = {H1:.4f}\n")

print("Вторая урна (выбор 3 шаров):")
print(f"P(SSS) = {P_SSS:.4f} (три синих)")
print(f"P(SSB) = {P_SSB:.4f} (два синих, один белый)")
print(f"P(SBB) = {P_SBB:.4f} (один синий, два белых)")
print(f"P(BBB) = {P_BBB:.4f} (три белых)")
print(f"Энтропия второй урны: H2 = {H2:.4f}\n")

if H1 > H2:
    print("Первая урна имеет большую неопределенность.")
elif H1 < H2:
    print("Вторая урна имеет большую неопределенность.")
else:
    print("Обе урны имеют одинаковую неопределенность.")
