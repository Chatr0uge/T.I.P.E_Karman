import matplotlib.pyplot as plt
"""C:/Users/andre/OneDrive/Documents/TIPE/Résultats_simu/simu1.txt
    C:/Users/andre/OneDrive/Documents/TIPE/simulation/data_2.txt"""
import copy
from mpl_toolkits import mplot3d
import seaborn as sns
import numpy as np


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
    (x, y, u) = (0, 0, 0)
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


# NOTE: print(maximum_spfU('C:/Users/andre/OneDrive/Documents/TIPE/Résultats_simu/Data_3.txt'))
graph_contour(
    'C:/Users/andre/OneDrive/Documents/TIPE/Résultats_simu/Data_3.txt')
