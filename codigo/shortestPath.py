from grafo import Grafo
from collections import deque
import pandas as pd
from math import inf
import matplotlib.pyplot as plt 
from shapely import wkt
import geopandas as gpd
import time


def caminoCorto(grafo: Grafo,inicio, fin,modFun=None):
    return caminoCortoAux(grafo, inicio, fin,modFun)

def caminoCortoAux(grafo: Grafo,inicio, fin,modFun=None):
    n = grafo.tamaño 
    
    visitados = [False] * n
    pesos = [inf] * n
    posiciones = [-1] * n
    pesos[inicio] = 0
  
    for i in range(n):
        visitando = -1
        for j in range(n):
            if (not visitados[j]) and (visitando==-1 or pesos[j]<pesos[visitando]):
                visitando=j
        if pesos[visitando]==inf:
            break
        visitados[visitando]=True

        for vecino in grafo.getSucesores(visitando):
            peso = grafo.getPeso(visitando,vecino,modFun)
            if pesos[visitando]+peso <pesos[vecino]:
                pesos[vecino]=pesos[visitando]+peso
                posiciones[vecino] = visitando
    
    distanciaTotal=pesos[fin]
    camino=deque()
    actual=fin

    while actual!=inicio:
        camino.appendleft(actual)
        actual=posiciones[actual]
        if (actual==-1):
            camino = deque()
            break
    return camino, distanciaTotal

def cargarGrafo(mapa:Grafo):
    datosMapa = pd.read_csv("calles_de_medellin_con_acoso.csv",sep=";", usecols=[0, 1, 2, 3, 4, 5,6])

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
            mapa.crearArista(mapa.vertices[datosMapa["origin"][i]],mapa.vertices[datosMapa["destination"][i]],(datosMapa["name"][i],datosMapa["length"][i],datosMapa["harassmentRisk"][i],datosMapa["geometry"][i]))
        else:
            mapa.crearAristaDirigida(mapa.vertices[datosMapa["origin"][i]],mapa.vertices[datosMapa["destination"][i]],(datosMapa["name"][i],datosMapa["length"][i],datosMapa["harassmentRisk"][i],datosMapa["geometry"][i]))
            
    mapa.tamaño = numeroNodos

def mod1(distancia,riesgo):
    return riesgo

def mod2(distancia,riesgo):
    return distancia

def mod3(distancia,riesgo):
    return distancia+riesgo*100000

def graficarCamino(mapa:Grafo,camino,color,ax):
    for i in range(len(camino)-1):
	    ax.plot(*(wkt.loads(mapa.getData(camino[i],camino[i+1])[4])).xy,color=color)

def main():
    polygon_data = pd.read_csv("poligono_de_medellin.csv",sep=";")
    fig, ax  = plt.subplots()
    poly = wkt.loads(polygon_data.iloc[0]["geometry"])
    p = gpd.GeoSeries(poly)
    p.plot(ax=ax)
    mapa = Grafo()
    cargarGrafo(mapa)

    inicio = time.time()
    resultadoEafitUnal = caminoCorto(mapa,8462,11296,mod1)
    print(f"El camino 1 se demoro {round(time.time()-inicio)} segundos y la distancia fue de {mapa.obtenerDistaciaTotal(resultadoEafitUnal[0])} con un riesgo de {mapa.obtenerRiesgoTotal(resultadoEafitUnal[0])}")
    graficarCamino(mapa,resultadoEafitUnal[0],"red",ax)
    
    inicio = time.time()
    resultadoEafitUnal = caminoCorto(mapa,8462,11296,mod2)
    print(f"El camino 2 se demoro {round(time.time()-inicio)} segundos y la distancia fue de {mapa.obtenerDistaciaTotal(resultadoEafitUnal[0])} con un riesgo de {mapa.obtenerRiesgoTotal(resultadoEafitUnal[0])}")
    graficarCamino(mapa,resultadoEafitUnal[0],"green",ax)

    inicio = time.time()
    resultadoEafitUnal = caminoCorto(mapa,8462,11296,mod3)
    print(f"El camino 3 se demoro {round(time.time()-inicio)} segundos y la distancia fue de {mapa.obtenerDistaciaTotal(resultadoEafitUnal[0])} con un riesgo de {mapa.obtenerRiesgoTotal(resultadoEafitUnal[0])}")
    graficarCamino(mapa,resultadoEafitUnal[0],"purple",ax)

    plt.show()
    
if __name__ == '__main__':
    main()
