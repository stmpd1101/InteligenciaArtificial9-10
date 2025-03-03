#Flores Soto Gael Eduardo 
#Inteligencia Artificial 9-10
#Algoritmo A* para puzzle8


import heapq
import numpy as np
import random

class Puzzle8:
    def __init__(self, estado_inicial, estado_objetivo):
        # Inicializa el estado inicial y objetivo
        self.estado_inicial = tuple(map(tuple, estado_inicial))
        self.estado_objetivo = tuple(map(tuple, estado_objetivo))
        self.n = 3  # Tamaño del puzzle 3x3

    def distancia_manhattan(self, estado):
        # Calcula la distancia de Manhattan como heurística
        distancia = 0
        for i in range(self.n):
            for j in range(self.n):
                if estado[i][j] != 0:
                    x_obj, y_obj = divmod(self.estado_objetivo_flat.index(estado[i][j]), self.n)
                    distancia += abs(i - x_obj) + abs(j - y_obj)
        return distancia
    
    def obtener_vecinos(self, estado):
        # Genera los estados vecinos moviendo el espacio vacío
        estado = np.array(estado)
        if 0 not in estado:
            raise ValueError("El estado no contiene el número 0 (espacio vacío). Verifica tu entrada.")

        x, y = np.where(estado == 0)
        x, y = int(x[0]), int(y[0])

        vecinos = []
        movimientos = [(0,1, "Derecha"), (0,-1, "Izquierda"), (1,0, "Abajo"), (-1,0, "Arriba")] 

        for dx, dy, direccion in movimientos:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.n and 0 <= ny < self.n:
                nuevo_estado = estado.copy()
                nuevo_estado[x, y], nuevo_estado[nx, ny] = nuevo_estado[nx, ny], nuevo_estado[x, y]
                vecinos.append((tuple(map(tuple, nuevo_estado)), direccion))
        
        return vecinos
    
    def resolver(self):
        # Implementa A* para resolver el puzzle
        self.estado_objetivo_flat = [num for fila in self.estado_objetivo for num in fila]
        cola_prioridad = []
        heapq.heappush(cola_prioridad, (0, self.estado_inicial, [], "Inicio"))
        visitados = set()
        
        while cola_prioridad:
            costo, estado, camino, movimiento = heapq.heappop(cola_prioridad)
            if estado == self.estado_objetivo:
                return camino + [(estado, movimiento)]
            if estado in visitados:
                continue
            visitados.add(estado)
            for vecino, direccion in self.obtener_vecinos(estado):
                if vecino not in visitados:
                    nuevo_costo = len(camino) + 1 + self.distancia_manhattan(vecino)
                    heapq.heappush(cola_prioridad, (nuevo_costo, vecino, camino + [(estado, movimiento)], direccion))
        return None

# Cuenta el número de inversiones en el estado

def contar_inversiones(estado):
    estado_plano = [num for fila in estado for num in fila if num != 0]
    inversiones = sum(1 for i in range(len(estado_plano)) for j in range(i + 1, len(estado_plano)) if estado_plano[i] > estado_plano[j])
    return inversiones

# Verifica si el puzzle es resoluble

def es_resoluble(estado_inicial, estado_objetivo):
    return contar_inversiones(estado_inicial) % 2 == contar_inversiones(estado_objetivo) % 2

# Convierte una cadena en matriz 3x3

def obtener_matriz(entrada):
    return [list(map(int, entrada[i:i+3])) for i in range(0, len(entrada), 3)]

# Genera un estado inicial aleatorio con solución

def generar_estado_aleatorio(estado_objetivo):
    while True:
        numeros = list(range(9))
        random.shuffle(numeros)
        estado_aleatorio = obtener_matriz(numeros)
        if es_resoluble(estado_aleatorio, estado_objetivo):
            return estado_aleatorio

# Bucle principal del juego

def jugar():
    while True:
        estado_objetivo = input("Ingrese el estado objetivo (9 dígitos, con 0 como espacio vacío): ")
        estado_objetivo = obtener_matriz(estado_objetivo)
        
        opcion = input("¿Desea ingresar el estado inicial manualmente? (s/n): ").strip().lower()
        
        if opcion == 's':
            estado_inicial = input("Ingrese el estado inicial (9 dígitos, con 0 como espacio vacío): ")
            estado_inicial = obtener_matriz(estado_inicial)
        else:
            estado_inicial = generar_estado_aleatorio(estado_objetivo)
            print("Estado inicial generado automáticamente:")
            for fila in estado_inicial:
                print(" ".join(map(str, fila)))
        
        if not es_resoluble(estado_inicial, estado_objetivo):
            print("Este 8-Puzzle no tiene solución.")
        else:
            puzzle = Puzzle8(estado_inicial, estado_objetivo)
            solucion = puzzle.resolver()
            
            if solucion:
                print("\nSolución encontrada:")
                for paso, (estado, movimiento) in enumerate(solucion):
                    print(f"Paso {paso} ({movimiento}):")
                    for fila in estado:
                        print(" ".join(map(str, fila)))
                    print()
            else:
                print("No se encontró solución.")
        
        repetir = input("¿Desea jugar de nuevo? (s/n): ").strip().lower()
        if repetir != 's':
            print("Gracias por jugar")
            break

if __name__ == "__main__":
    jugar()
