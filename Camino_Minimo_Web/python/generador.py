from random import randint as entero_aleatorio


class GeneradorMatriz:

    def __init__(self, peso_maximo=20):
        if peso_maximo < 0:
            raise ValueError("El peso máximo no puede ser negativo.")

        self._peso_maximo = peso_maximo

    def crear_matriz_vacia(self, cantidad_vertices):
        self._validar_cantidad(cantidad_vertices)
        matriz = []

        for origen in range(cantidad_vertices):
            fila = [None] * cantidad_vertices
            fila[origen] = 0
            matriz.append(fila)

        return matriz

    def generar_matriz(self, cantidad_vertices, dirigido=False):
        matriz = self.crear_matriz_vacia(cantidad_vertices)

        for origen in range(cantidad_vertices):
            for destino in range(cantidad_vertices):
                if origen == destino:
                    continue

                if not dirigido and destino < origen:
                    continue

                if entero_aleatorio(0, 1) == 1:
                    peso = entero_aleatorio(0, self._peso_maximo)
                    matriz[origen][destino] = peso

                    if not dirigido:
                        matriz[destino][origen] = peso

        return matriz

    def _validar_cantidad(self, cantidad_vertices):
        if not 5 <= cantidad_vertices <= 15:
            raise ValueError("El grafo debe tener entre 5 y 15 vértices.")
