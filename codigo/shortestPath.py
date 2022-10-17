from grafo import Grafo
from collections import deque
import pandas as pd
from math import inf

def caminoCorto(grafo: Grafo,inicio, fin):
    return caminoCortoAux(grafo, inicio, fin)

def caminoCortoAux(grafo: Grafo,inicio, fin):


    n = grafo.tamaño 
    
    visitados = [False] * n
    distancias = [inf] * n
    posiciones = [-1] * n
    distancias[inicio] = 0

    for i in range(n):
        visitando = -1
        for j in range(n):
            if (not visitados[j]) and (visitando==-1 or distancias[j]<distancias[visitando]):
                visitando=j
        if distancias[visitando]==inf:
            break
        visitados[visitando]=True

        for vecino in grafo.getSucesores(visitando):
            metros=grafo.getDistance(visitando,vecino)

            if distancias[visitando]+metros <distancias[vecino]:
                distancias[vecino]=distancias[visitando]+metros
                posiciones[vecino] = visitando
    
    distanciaTotal=distancias[fin]
    camino=deque()
    actual=fin

    while actual!=inicio:
        camino.appendleft(actual)
        actual=posiciones[actual]
        if (actual==-1):
            camino = deque()
            break

        camino.appendleft(inicio)
    return camino, distanciaTotal

def cargarGrafo(mapa:Grafo):

    datosMapa = pd.read_csv("isa/calles_de_medellin_con_acoso .csv",sep=";", usecols=[0, 1, 2, 3, 4, 5])

    numeroNodos = 0

    for i in range(len(datosMapa)):
        if datosMapa["origin"][i] not in mapa.vertices.keys():
            mapa.vertices[datosMapa["origin"][i]] = numeroNodos
            numeroNodos += 1
        if datosMapa["destination"][i] not in mapa.vertices.keys():
            mapa.vertices[datosMapa["destination"][i]] = numeroNodos
            numeroNodos += 1      

    mapa.iniciarLista(numeroNodos)

    for i in range(len(datosMapa)):
        if datosMapa["oneway"][i]:
            mapa.crearArista(mapa.vertices[datosMapa["origin"][i]],mapa.vertices[datosMapa["destination"][i]],(datosMapa["name"][i],datosMapa["length"][i],datosMapa["harassmentRisk"][i]))
        else:
            mapa.crearAristaDirigida(mapa.vertices[datosMapa["origin"][i]],mapa.vertices[datosMapa["destination"][i]],(datosMapa["name"][i],datosMapa["length"][i],datosMapa["harassmentRisk"][i]))

    mapa.tamaño = numeroNodos




def main():

    mapa = Grafo()


    cargarGrafo(mapa)

    resultadoEafitUdea = caminoCorto(mapa,8462,11296)


    print('distancia:',resultadoEafitUdea[1])


    print("camino:",resultadoEafitUdea[0])


    

    



if __name__ == '__main__':
    main()




