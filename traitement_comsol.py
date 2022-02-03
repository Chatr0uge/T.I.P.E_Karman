import matplotlib.pyplot as plt
"""C:/Users/andre/OneDrive/Documents/TIPE/Résultats_simu/simu1.txt
    C:/Users/andre/OneDrive/Documents/TIPE/simulation/data_2.txt"""
import copy
import seaborn as sns
import numpy as np
from scipy import interpolate
from scipy.fft import fft


def tableau(fichier):
    f = open(fichier, 'r')
    S = []
    for line in f:
        L = line.split()
        for i in range(len(L)):
            L[i] = float(L[i])
        S.append(L)
    return S


def graph_sonde(fichier):
    S = []
    tableau(
        fichier)
    X = []
    Y = []
    for k in range(len(S)):
        X.append(S[k][0])
        Y.append(S[k][1])
    fig, ax = plt.subplots()
    plt.plot(X, Y, color='coral', linewidth=0.5)
    plt.show()


def graph_node(fichier):
    u = 0
    X = []
    Y = []
    u = 0
    f = open(fichier, 'r')
    for line in f:
        u = u+1
        if u == 1:
            L1 = line.split()
            for z in range(len(L1)):
                X.append(float((L1[z])))
        if u == 2:
            L2 = line.split()
            for z in range(len(L2)):
                Y.append(float(L2[z]))
        if u > 3:
            break
    fig, ax = plt.subplots()
    plt.scatter(X, Y, s=0.1, color='k')
    plt.show()


def graph_contour(fichier):
    sns.set_context("paper")
    (x, y, u) = (0, 0, 0)
    X = []
    Y = []
    U = []
    f = open(fichier, 'r')
    for line in f:
        u = u+1
        if u == 1:
            L1 = line.split()
            for z in range(len(L1)):
                X.append(float((L1[z])))
        if u == 2:
            L2 = line.split()
            for z in range(len(L2)):
                Y.append(float(L2[z]))
        if u > 3:
            W = []
            L3 = line.split()
            for z in range(len(L3)):
                W.append(float(L3[z]))
            U.append(copy.deepcopy(W))
    fig, ax = plt.subplots()
    plt.subplot(2, 1, 1)
    surf = plt.tricontourf(X, Y, U[5], levels=30,  cmap='viridis')
    plt.scatter(maximum_spfU(fichier)[1][0], maximum_spfU(
        fichier)[1][1], marker="o", s=4, facecolors='none', edgecolors='coral')
    fig.colorbar(surf)
    plt.subplot(2, 1, 2)
    surf = plt.tricontourf(X, Y, U[15], levels=30, cmap='viridis')
    plt.scatter(maximum_spfU(fichier)[1][0], maximum_spfU(
        fichier)[1][1], marker="o", s=5, facecolors='none', edgecolors='coral')
    fig.colorbar(surf)
    plt.show()
    #plt.savefig(
    #'C:/Users/andre/OneDrive/Documents/TIPE/simulation/écoulement.png', dpi=600)


def graph_3D(fichier):
    sns.set_context("paper")
    u = 0
    X = []
    Y = []
    U = []
    f = open(fichier, 'r')
    for line in f:
        u = u+1
        if u == 1:
            L1 = line.split()
            for z in range(len(L1)):
                X.append(float((L1[z])))
        if u == 2:
            L2 = line.split()
            for z in range(len(L2)):
                Y.append(float(L2[z]))
        if u >= 3:
            W = []
            L3 = line.split()
            for z in range(len(L3)):
                W.append(float(L3[z]))
            U.append(copy.deepcopy(W))
    fig = plt.figure(figsize=plt.figaspect(0.5))
    ax = fig.add_subplot(2, 1, 1, projection='3d')
    ax.scatter(X, Y, U[5], s=0.1, c=U[5], cmap='viridis')
    ax = fig.add_subplot(2, 1, 2, projection='3d')
    ax.scatter(X, Y, U[10], s=0.1, c=U[5], cmap='viridis')
    plt.show()


def graph_arrows(fichier):
    sns.set_context("paper")
    L = tableau(fichier)
    X = []
    Y = []
    vx = []
    vy = []
    for k in range(len(L)):
        X.append(L[k][0])
        Y.append(L[k][1])
        vx.append(L[k][2])
        vy.append(L[k][3])
    color = np.asarray(vx)**2+np.asarray(vy)**2
    plt.quiver(X, Y, vx, vy, color, angles='xy')
    plt.show()


def maximum_spfU(fichier):  # NOTE:  il faudra rajouter un domaine de recherche
    sns.set_context("paper")
    u = 0
    X = []
    Y = []
    U = []
    Max = []
    Index = []
    f = open(fichier, 'r')
    for line in f:
        u = u+1
        if u == 1:
            L1 = line.split()
            for z in range(len(L1)):
                X.append(float((L1[z])))
        if u == 2:
            L2 = line.split()
            for z in range(len(L2)):
                Y.append(float(L2[z]))
        if u >= 3:
            W = []
            L3 = line.split()
            for z in range(len(L3)):
                W.append(float(L3[z]))
            U.append(copy.deepcopy(W))
    i = 0
    for u in U:
        i += 1
        Max.append(max(u))
        Index.append((i-2, u.index(max(u))))
    m = max(Max)
    i = Index[Max.index(m)][1]
    return (m, (X[i], Y[i]))


def select_noeud(fichier, domaine):
    """on demande en entrée une liste de tuple, [(xmin,xmax),(ymin,ymax)]"""
    u = 0
    X = []
    Y = []
    Xres = []
    Yres = []
    indice = []
    f = open(fichier, 'r')
    for line in f:
        u = u+1
        if u == 1:
            L1 = line.split()
            for z in range(len(L1)):
                X.append(float((L1[z])))
        if u == 2:
            L2 = line.split()
            for z in range(len(L2)):
                Y.append(float(L2[z]))
        if u > 3:
            break
    for k in range(len(X)):
        if domaine[1][0] < Y[k] < domaine[1][1] and domaine[0][0] < X[k] < domaine[0][1]:
            indice.append(k)
            """Xres.append([X[k], k])
            Yres.append([Y[k], k])"""
    return indice
    """fig, ax = plt.subplots()
    plt.scatter(Xres, Yres, s=0.1, color='k')
    ax.set(xlim=(0, 0.2),
           ylim=(0, 0.08),
           autoscale_on=False)
    plt.show()"""


def oscillations(fichier):
    """ici on veut retourner vrai/faux"""
    t = [k/10 for k in range(0, 12, 2)] + \
        [k/1000 for k in range(1100, 2004, 4)]
    """[k/100 for k in range(110, 202, 2)]"""
    [k/1000 for k in range(1100, 2002, 2)]
    t = t[7:]
    U = []
    u = 0
    Point = []
    Courbe_interp = []
    fourier = []
    f = open(fichier, 'r')
    for line in f:
        u = u+1
        if u >= 3:
            W = []
            L3 = line.split()
            for z in range(len(L3)):
                W.append(float(L3[z]))
            U.append(copy.deepcopy(W))
    for k in select_noeud(fichier, [(0.08, 0.081), (0.02, 0.1)]):
        P = []
        for z in range(7, len(U)):
            P.append(U[z][k])
        Point.append(P)
    num = 300
    t1 = np.linspace(t[0], t[-1], num)
    for k in Point:
        f = interpolate.interp1d(t, np.asarray(k), kind='cubic')
        k1 = f(t1)
        Courbe_interp.append(k1)
        fourier.append(
            2.0/num * np.abs(fft(k1)[:num//2])/(np.linalg.norm(2.0/num * np.abs(fft(k1)[:num//2]))))
    freq = np.linspace(0.0, 1.0/(2.0*(t[-1]-t[0])/num), num//2)
    """fig, ax = plt.subplots()
    plt.subplot(2, 1, 1)

    plt.plot(t1, Courbe_interp[10])
    plt.scatter(t, Point[10], s=4, c='coral')

    plt.subplot(2, 1, 2)

    ax.set(xlim=(0, 5))
    plt.plot(freq, fourier[15])
    plt.show()"""
    
    prec = 0.01
    for k in fourier:
        for j in range(len(k)):
            if freq[j] > 2:
                if k[j] > prec:
                    return True
    return False

