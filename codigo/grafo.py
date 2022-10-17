from collections import deque

class Grafo:
    
    def __init__(self): 
        
        self.diccionarioVisita = {}
        
        self.vertices = {}
        
        self.tamaño = 0
        
        self.listaGrafo = None
        
        

        # Array of linked Lists with tuples where ( vertice, weight)

    def verticeValido(self, vertice):

        return 0 <= vertice < self.tamaño
    
    def iniciarLista(self,tamaño):
        
        self.tamaño = tamaño
        
        self.listaGrafo = [0]*self.tamaño
        
        for i in range(tamaño):
            self.listaGrafo[i] = deque()

    def crearAristaDirigida(self, vertice, vertice2, weight):

        if self.verticeValido(vertice) and self.verticeValido(vertice2):
            self.listaGrafo[vertice].append((vertice2, weight[0],weight[1],weight[2]))     # X -> (Y,nombre,distancia,indice))
        else:
            print("Los nodos no son validos")
            
    def crearArista(self, vertice, vertice2, weight):
        
        self.crearAristaDirigida(vertice,vertice2,weight)
        self.crearAristaDirigida(vertice2,vertice,weight)
        
        

    def getSucesores(self, vertice):
    
        if self.verticeValido(vertice):
            
            list1 = []
        
            verticeSuccesores = self.listaGrafo[vertice]
            
            for i in range(len(verticeSuccesores)):
                list1.append(verticeSuccesores[i][0])
                
            return list1

    def getData(self, inicio, destino):
        
        if self.verticeValido(inicio) and self.verticeValido(destino):
        
            inicioAdjacentes = self.listaGrafo[inicio]
            
            for i in inicioAdjacentes:
                
                if i[0] == destino:
                    return i
        
        else:
            print("Los vertices escogidos no son validos")

    def getDistance(self,inicio,destino):
            return self.getData(inicio,destino)[2]
            