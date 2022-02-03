import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import math
import copy


def indice_couple_polygones(A, n):
    L = []
    for k in A:
        L.append([k % n, k//n])
    return L


# NOTE: Ici encore on utilisera une liste de coords / indices
def couple_indice_polygones(A, n):
    L = []
    for k in A:
        L.append(k[1]*n+k[0])
    return L


def dedoublonneCL(L):
    s = []
    [s.append(u) for u in L if u not in s]
    return s


def trier_angle(A):
    """Avec A une liste de tuples"""
    """Algorithme de l'oursin"""
    xg = 0
    yg = 0
    for k in range(len(A)):
        xg += A[k][0]
        yg += A[k][1]
        G = (xg/len(A), yg/len(A))

        def ordre(p1):
            v1 = [p1[0]-G[0], p1[1]-G[1]]
            # les cas d'égalité se compensent de tous les côtés
            return math.atan2(v1[1], -v1[0])
    return sorted(A, key=ordre)

# NOTE:  il faut éviter les doublons par symétrie ou par translation


def aire_poly(K):
    # NOTE:  On rentre ici une liste de coordonnées
    S = 0
    for q in range(len(K)-1):
        S += K[q][0]*K[q+1][1]-K[q+1][0]*K[q][1]
    S = 0.5*(S+K[-1][0]*K[0][1]-K[0][0]*K[-1][1])
    return S


def verif_poly(L, n):
    """Prend en entrée une liste d'indice, sans doublons"""
    W = []
    for D in L:
        v = 0
        # NOTE: Pour Toute Translation dans le plan
        for z1 in range(-min([k % n for k in D]), n-max([k % n for k in D])):
            for z2 in range(-min([(k+z1) // n for k in D]), n-max([(k+z1) // n for k in D])):
                if couple_indice_polygones(trier_angle(indice_couple_polygones([k+z1+n*z2 for k in D], n)), n) in W:
                    v = 1
        if v == 0:
            W.append(D)
    return W


def polygones(n):
    L = []
    for k in range(n**2):
        for j in range(n**2):
            for i in range(n**2):
                for r in range(n**2):
                    if len(dedoublonneCL([k, j, i, r])) >= 3:
                        K = trier_angle(indice_couple_polygones(
                            dedoublonneCL([k, j, i, r]), n))
                        if aire_poly(K) != 0:
                            L.append(couple_indice_polygones(K, n))
    L = dedoublonneCL(L)
    return verif_poly(L, n)


def poly_txt(N, fichier, liste):
    f = open(fichier, 'w')
    L = [indice_couple_polygones(k, N) for k in liste]
    for k in range(len(L)):
        S = 0
        for q in range(len(L[k])-1):
            S += L[k][q][0]*L[k][q+1][1]-L[k][q+1][0]*L[k][q][1]
        area = (1/2)*S+L[k][-1][0]*L[k][0][1]-L[k][0][0]*L[k][-1][1]
        text = ("poly %d || %s || area : %f ||%s \n") % (
            k, str(L[k]), area, str(couple_indice_polygones(L[k], N)))
        # text = ("%s \n") % (str((couple_indice_polygones(L[k], N))))
        f.write(text)


def tracer_polygones(fichier, fichier_arr, N):
    P = []
    L = []
    for k in range(N):
        for j in range(N):
            P.append([k, j])

    figure, axes = plt.subplots()
    axes.set_xlim(-1, N)
    axes.set_ylim(-1, N)
    plt.axis('off')
    plt.grid()
    poly1 = axes.add_patch(Polygon([[10000, 10000]], closed=True, fill=False))

    for k in P:
        plt.plot(k[0], k[1], marker="o", markersize=2, color='k')

    f = open(fichier, 'r')
    for line in f:
        L.append(eval(line.split('||')[-1]))

    for j in range(len(L)):
        L[j] = indice_couple_polygones(L[j], N)
        poly1.set_xy([k for k in L[j]])
        plt.savefig(
            fichier_arr + '/poly_'+str(j)+'.png')


def create_polygon_5(fichier):
    """NOTE: Permer de créer une liste de pentagones à partir d'une liste
     préenregistrée de quadrilatères"""
    L = []
    f = open(fichier, 'r')
    for line in f:
        L.append(eval(line.split('||')[-1]))
    # NOTE: On va mtn modifier L : on rajoute 1 colonne à D et une ligne en H
    for k in range(len(L)):
        L[k] = [r+r//4 for r in L[k]]
    C = copy.deepcopy(L)
    for k in C:
        for j in range(25):
            B = trier_angle(indice_couple_polygones(dedoublonneCL(k+[j]), 5))
            # NOTE: On décide de trier ici
            if aire_poly(B) != 0 and couple_indice_polygones(B, 5) not in L:
                L.append(couple_indice_polygones(B, 5))
    return verif_poly(L, 5)
    #C:/Users/andre/OneDrive/Documents/TIPE/simulation/polygones.txt
