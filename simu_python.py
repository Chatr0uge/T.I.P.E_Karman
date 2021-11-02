import mph
import jpype
from create_polygon import indice_couple_polygones


def coords(liste):
    L = []
    for k in range(len(liste)):
        L.append([0.03+liste[k][0]*0.04/3, 0.04+liste[k][1]*0.04/3])
    return L


def tables(fichier, N):
    L = []
    f = open(fichier, 'r')
    for line in f:
        B = coords(indice_couple_polygones(
            eval(line.split('||')[-1]), N))
        L.append(B)
    return L


def simulation(fichier, taille_grille, coeurs):
    client = mph.start(cores=coeurs)
    L = tables(fichier, taille_grille)
    pymodel = client.load(
        'C:/Users/andre/OneDrive/Documents/TIPE/Simulmations_Comsol/simu.mph')
    model = pymodel.java
    for k in range(4):
        print(L[k])
        model.component('comp1').geom("geom1").feature("pol1").set(
                "table", L[k])
        model.geom("geom1").run("fin")
        model.study("std1").run()
        model.result().export('data1').set(
            "filename", 'C:/Users/andre/OneDrive/Documents/TIPE/Résultats_simu/Data_'+str(k)+'.txt')
        model.result().export("img1").set(
            "filename", 'C:/Users/andre/OneDrive/Documents/TIPE/Résultats_simu/mesh_'+str(k)+'.txt')
        model.result().export('data2').set(
            "filename", 'C:/Users/andre/OneDrive/Documents/TIPE/Résultats_simu/Data_arrows_'+str(k)+'.txt')
        model.result().export("data1").run()
        model.result().export("img1").run()
        model.result().export("data2").run()
    client.clear()


simulation('C:/Users/andre/OneDrive/Documents/TIPE/simulation/polygones.txt', 4, 1)
