from create_polygon import trier_angle, dedoublonneCL, indice_couple_polygones
import copy


def tableau(fichier):
    f = open(fichier, 'r')
    L = []
    for line in f:
        L.append(eval(line))
    return L


def create_polygon_5(n):
    L = tableau(
        'C:/Users/andre/OneDrive/Documents/TIPE/simulation/polygones.txt')
    LL = copy.deepcopy(L)
    for h in range(len(LL)):
        LL[h] = indice_couple_polygones(LL[h], n)
    for k in L:
        A = k
        for j in range(n**2):
            if j not in k:
                A.append(j)
                B = trier_angle(indice_couple_polygones(A, n))
                LL.append(B)
    return dedoublonneCL(LL)


print(len(create_polygon_5(5)))
