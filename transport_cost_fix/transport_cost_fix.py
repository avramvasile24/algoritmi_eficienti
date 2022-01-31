import os  # librarie pentru citirea fisier din folder
import re  # librarie pentru eliminarea caracterelor dorite
from numpy import zeros
import sys  # determinarea int maxim
import xlsxwriter #librarie pt xls
import time

file = xlsxwriter.Workbook("date.xlsx")  # creeaza fisierul xls
sheet = file.add_worksheet()  # adauga pagina in xls
linie = 1

path = "Input"
for item in os.listdir(path):
    item = os.path.join(path, item)
    Cjk = []
    Fjk = []
    with open(item, "r") as f:
        k = 0
        aux = []
        ok = 0
        oke = 0
        auxiliar = ""
        for line in f:
            if k < 5 or line == '\n':
                k += 1
                continue
            line = re.sub('[\[\n;"]', '', line)
            if line[len(line) - 1] == ']' and oke == 1:
                ok = 1
            line = re.sub('[\]]', '', line)
            variable = line.split(' = ')
            if variable[0] == "instance_name":
                instance_name = str(variable[1])
            elif variable[0] == "d":
                d = int(variable[1])
            elif variable[0] == "r":
                r = int(variable[1])
            elif variable[0] == "SCj":
                SCj = list(map(int, variable[1].split(' ')))
            elif variable[0] == "Dk":
                Dk = list(map(int, variable[1].split(' ')))
                oke = 1
            elif variable[0] == "Cjk":
                auxiliar = "Cjk"
                aux.extend(list(map(int, variable[1].split(' '))))
            elif variable[0] == "Fjk":
                auxiliar = "Fjk"
                aux.extend(list(map(int, variable[1].split(' '))))
            else:
                variable[0] = variable[0].lstrip()
                aux.extend(list(map(int, variable[0].split(' '))))
            if ok == 1 and auxiliar == "Cjk":
                Cjk.append(aux)
                aux = []
                ok = 0
            elif ok == 1 and auxiliar == "Fjk":
                Fjk.append(aux)
                aux = []
                ok = 0

    # print(instance_name)
    # print(d)
    # print(r)
    # print(SCj)
    # print(Dk)
    # print(Cjk)
    print(Fjk)
    start_time = time.perf_counter()
    # transportul in functie de traseul optim
    Xjk = zeros((len(SCj), len(Dk)), dtype=int)

    Uj = zeros(len(SCj), dtype=int) #verifica daca s-au folosit toti furnizorii
    Ujk = zeros((len(SCj),len(Dk)), dtype = int) #verifica care drumuri s-au folosit
    Dk_aux = Dk.copy()  # pastreaca copia cererii clientilor
    SCj_aux = SCj.copy()  # pastreaca copia stocului furnizoriilor

    iteratii = 0

    # print(Xjk)
    while (True):
        minim = max(Dk)  # minimul cereri clientului
        if minim == 0:
            status = 'Rezolvata'
            break
        if max(SCj) == 0:
            status = 'Nerezolvata'
        iteratii += 1
        indice_c = 0  # indice client
        for i in range(0, len(Dk)):
            if minim >= Dk[i] and Dk[i] != 0:
                indice_c = i  # clientul la care s-a gasit minimul
                minim = Dk[i]  # noul minim

        cost_minim = sys.maxsize  # initializare cu cea mai mare val int
        indice_f = 0  # indice furnizor
        for i in range(0, len(SCj)):  # verificare pt fiecare furnizor (cost transport)
            if cost_minim > Cjk[i][indice_c] and SCj[i] != 0:  # verificare cost minim si disponibil
                indice_f = i  # noul furnizor
                cost_minim = Cjk[i][indice_c]  # noul minim de cost

        if SCj[indice_f] > Dk[indice_c]:  # verifica daca cererea este mai mica decat stocul furnizorului
            SCj[indice_f] -= Dk[indice_c]
            Xjk[indice_f][indice_c] = Dk[indice_c]
            Dk[indice_c] -= Dk[indice_c]
        else:
            Dk[indice_c] -= SCj[indice_f]
            Xjk[indice_f][indice_c] = SCj[indice_f]
            SCj[indice_f] -= SCj[indice_f]
        # Xjk cat s-a transportat de la fiecare furnizor la fiecare client
    # print("Xjk = ", Xjk)

    optim = 0
    CostD2R = 0
    CostFixD2R = 0

    for i in range(0, len(SCj)):
        if SCj[i] != SCj_aux[i]:
            Uj[i] = 1  # verifica care dintre magazine au fost folosite 1=da, 0=nu

    for i in range(0, len(SCj)):  # linii
        for j in range(0, len(Dk)):  # coloane
            if Xjk[i][j] != 0:
                Ujk[i][j] = 1 # Ujk gasit

    for i in range(0, len(SCj)):  # linii
        for j in range(0, len(Dk)):  # coloane
            CostD2R += Xjk[i][j] * Cjk[i][j]  # optim gasit

    for i in range(0, len(SCj)):  # linii
        for j in range(0, len(Dk)):  # coloane
            optim += (Xjk[i][j] *Cjk[i][j]) + (Ujk[i][j] * Fjk[i][j])  # optim gasit

    CostFixD2R = optim - CostD2R #CostFixD2R gasit
    # print(instance_name)
    # print(CostFixD2R)

    out_path = "Output/" + instance_name + ".txt"
    with open(out_path, 'w') as out:
        out.write("Xjk = " + str(Xjk) + "\n")
        out.write("Uj = " + str(Uj) + "\n")
        out.write("Dk = " + str(Dk_aux) + "\n")
        out.write("Optim = " + str(optim) + "\n")
        out.write("Cost D2R = " + str(CostD2R) + "\n")
        out.write("Cost Fix D2R = " + str(CostFixD2R) + "\n")

    end_time = round(time.perf_counter() - start_time, 5)

    # punem in fisier xml, rezultatele

    sheet.write('A' + str(linie), instance_name)
    sheet.write('B' + str(linie), str(optim))
    sheet.write('C' + str(linie), str(iteratii))
    sheet.write('D' + str(linie), str(end_time))
    sheet.write('E' + str(linie), status)
    linie += 1

file.close()