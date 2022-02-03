import mph
import jpype
from create_polygon import indice_couple_polygones
from traitement_comsol import oscillations
import shutil


def coords(liste):
    L = []
    for k in range(len(liste)):
        L.append([0.05+liste[k][0]*0.02, 0.03+liste[k][1]*0.02]) 
        #On définit ici les coordonnées de la grille à metre dans Comsol
    return L


def tables(fichier, N): #Permet de lire les coordonnées des polynômes construits précédemment
    L = []
    f = open(fichier, 'r')
    for line in f:
        B = coords(indice_couple_polygones(
            eval(line.split('||')[-1]), N))
        L.append(B) 
    return L


def simulation(fichier, fichier_arr, taille_grille, coeurs):
    client = mph.start(cores=coeurs)
    L = tables(fichier, taille_grille)
    pymodel = client.load(
        'C:/Users/andre/OneDrive/Documents/TIPE/Simulmations_Comsol/simu.mph')
    model = pymodel.java
    for k in range(3):
        model.component('comp1').geom("geom1").feature("pol1").set(
                "table", L[k])
        model.geom("geom1").run("fin")
        model.study("std1").run()
        model.result().export('data1').set(
            "filename", fichier_arr+'/Data_'+str(k)+'.txt')
        model.result().export("img1").set(
            "filename", fichier_arr+'/Mesh_'+str(k))
        model.result().export("data1").run()
        model.result().export("img1").run()
        if oscillations(fichier_arr+'/Data_'+str(k) + '.txt'): 
            #on vérifie si il y'a présence d'oscillations pour le tr
            shutil.move(fichier_arr+'/Data_'+str(k)+'.txt', fichier_arr
                        + '/oscillation')
            shutil.move(fichier_arr+'/Mesh_'+str(k)+'.png', fichier_arr
                        + '/oscillation')
    client.clear()


simulation('C:/Users/andre/OneDrive/Documents/TIPE/simulation/polygones.txt',
           'C:/Users/andre/OneDrive/Documents/TIPE/Résultats_simu', 4, 3)
#   'C:/Users/andre/OneDrive/Documents/TIPE/Résultats_simu
