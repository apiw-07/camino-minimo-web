from math import isfinite as es_finito


class Grafo:

    def __init__(self, matriz, dirigido=False):
        self._validar_matriz(matriz, dirigido)
        self._matriz = [fila[:] for fila in matriz]
        self._cantidad_vertices = len(matriz)
        self._dirigido = dirigido

    def _validar_matriz(self, matriz, dirigido):
        cantidad_vertices = len(matriz)

        if not 5 <= cantidad_vertices <= 15:
            raise ValueError("El grafo debe tener entre 5 y 15 vértices.")

        for fila in matriz:
            if len(fila) != cantidad_vertices:
                raise ValueError("La matriz debe ser cuadrada.")

        for origen in range(cantidad_vertices):
            for destino in range(cantidad_vertices):
                self._validar_peso(matriz[origen][destino], origen, destino)

        if not dirigido:
            self._validar_simetria(matriz)

    def _validar_peso(self, peso, origen, destino):
        if origen == destino and peso != 0:
            raise ValueError(f"La diagonal debe ser 0 (revisa la posición [{origen}, {destino}]).")

        if peso is None:
            return

        if peso < 0:
            raise ValueError(f"El peso de la posición [{origen}, {destino}] no puede ser negativo.")

        if isinstance(peso, float) and not es_finito(peso):
            raise ValueError(f"El peso de la posición [{origen}, {destino}] debe ser un número finito.")

    def _validar_simetria(self, matriz):
        cantidad_vertices = len(matriz)

        for origen in range(cantidad_vertices):
            for destino in range(origen + 1, cantidad_vertices):
                if matriz[origen][destino] != matriz[destino][origen]:
                    raise ValueError(
                        f"La matriz no es simétrica: las posiciones [{origen}, {destino}] "
                        f"y [{destino}, {origen}] son distintas."
                    )

    def _validar_vertice(self, vertice):
        if not 0 <= vertice < self._cantidad_vertices:
            raise ValueError("El vértice no pertenece al grafo.")

    def obtener_cantidad_vertices(self):
        return self._cantidad_vertices

    def es_dirigido(self):
        return self._dirigido

    def obtener_matriz(self):
        return [fila[:] for fila in self._matriz]

    def obtener_peso(self, origen, destino):
        self._validar_vertice(origen)
        self._validar_vertice(destino)
        return self._matriz[origen][destino]

    def obtener_vecinos(self, vertice):
        self._validar_vertice(vertice)
        vecinos = []

        for vecino, peso in enumerate(self._matriz[vertice]):
            if vecino != vertice and peso is not None:
                vecinos.append((vecino, peso))

        return vecinos

    def obtener_aristas(self):
        aristas = []

        for origen in range(self._cantidad_vertices):
            for destino, peso in self.obtener_vecinos(origen):
                if self._dirigido or origen < destino:
                    aristas.append((origen, destino, peso))

        return aristas
