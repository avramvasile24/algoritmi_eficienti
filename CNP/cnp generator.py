import random
import os
os.remove("date_generate.txt")


def generare_cnp(j):
    an = random.randrange(1800, 2100)
    if an < 1900:
        s = random.choice([3, 4])
    elif an < 2000:
        s = random.choice([1, 2])
    else:
        s = random.choice([5, 6])
    aa = an % 100

    ll = random.randrange(1, 13)

    if ll == 2:
        zz = random.randrange(1, 29)
    elif ll == 4 or ll == 6 or ll == 9 or ll == 11:
        zz = random.randrange(1, 31)
    else:
        zz = random.randrange(1, 32)

    nnn = random.randrange(1, 1000)
    cnp = (((((s*100) + aa)*100 + ll)*100 + zz)*100 + j)*1000 + nnn
    cnp_copy = cnp
    c = 0

    while cnp_copy > 0:
        c += cnp_copy % 10
        cnp_copy //= 10

    cnp = cnp*10 + c

    file = open("date_generate.txt", "a")
    file.write(str(cnp) + "\n")


with open('populatie_judete.txt') as f:
    lines = f.readlines()

generate = 0
for i in range(0, 42):
    line = lines[i]
    judet = line[:2]
    populatie_reala = line[3:]
    populatie = int(populatie_reala) * 1000000 // 20000000
    for k in range(0, populatie):
        generare_cnp(int(judet))
        generate += 1

for i in range(0, 1000000-generate):
    generare_cnp(40)
