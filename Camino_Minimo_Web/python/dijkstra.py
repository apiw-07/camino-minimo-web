from math import inf as infinito

from grafo import Grafo


class Dijkstra:

    def __init__(self, grafo):
        if not isinstance(grafo, Grafo):
            raise ValueError("El algoritmo necesita un objeto de la clase Grafo.")

        self._grafo = grafo

    def resolver(self, origen, destino):
        self._validar_vertices(origen, destino)
        cantidad_vertices = self._grafo.obtener_cantidad_vertices()

        distancias = [infinito] * cantidad_vertices
        predecesores = [None] * cantidad_vertices
        fijados = [False] * cantidad_vertices
        distancias[origen] = 0

        pasos = [self._crear_paso(0, None, distancias, predecesores, fijados, [])]

        while True:
            actual = self._seleccionar_vertice(distancias, fijados)

            if actual is None:
                break

            fijados[actual] = True

            relajaciones = []

            if actual != destino:
                relajaciones = self._relajar_vecinos(
                    actual,
                    distancias,
                    predecesores,
                    fijados
                )

            pasos.append(
                self._crear_paso(
                    len(pasos),
                    actual,
                    distancias,
                    predecesores,
                    fijados,
                    relajaciones
                )
            )

            if actual == destino:
                break

        alcanzable = distancias[destino] != infinito
        camino = []
        costo = infinito

        if alcanzable:
            camino = self._reconstruir_camino(destino, predecesores)
            costo = self._calcular_costo(camino)

            if costo != distancias[destino]:
                raise ValueError("El costo de la ruta no coincide con la distancia calculada.")

        return {
            "origen": origen,
            "destino": destino,
            "alcanzable": alcanzable,
            "camino": camino,
            "costo": costo,
            "pasos": pasos
        }

    def _validar_vertices(self, origen, destino):
        cantidad_vertices = self._grafo.obtener_cantidad_vertices()

        for vertice in (origen, destino):
            if not 0 <= vertice < cantidad_vertices:
                raise ValueError("El vértice no pertenece al grafo.")

    def _crear_paso(
        self,
        iteracion,
        vertice_actual,
        distancias,
        predecesores,
        fijados,
        relajaciones
    ):
        return {
            "iteracion": iteracion,
            "vertice_actual": vertice_actual,
            "distancias": distancias[:],
            "predecesores": predecesores[:],
            "fijados": fijados[:],
            "relajaciones": relajaciones
        }

    def _seleccionar_vertice(self, distancias, fijados):
        actual = None
        menor_distancia = infinito

        for vertice in range(len(distancias)):
            if not fijados[vertice] and distancias[vertice] < menor_distancia:
                actual = vertice
                menor_distancia = distancias[vertice]

        return actual

    def _relajar_vecinos(self, actual, distancias, predecesores, fijados):
        relajaciones = []

        for vecino, peso in self._grafo.obtener_vecinos(actual):
            if fijados[vecino]:
                continue

            distancia_anterior = distancias[vecino]
            distancia_propuesta = distancias[actual] + peso

            if distancia_propuesta == infinito:
                raise ValueError("Los pesos son demasiado grandes para calcular el costo.")

            mejora = distancia_propuesta < distancia_anterior

            relajaciones.append({
                "origen": actual,
                "destino": vecino,
                "peso": peso,
                "distancia_anterior": distancia_anterior,
                "distancia_propuesta": distancia_propuesta,
                "mejora": mejora
            })

            if mejora:
                distancias[vecino] = distancia_propuesta
                predecesores[vecino] = actual

        return relajaciones

    def _reconstruir_camino(self, destino, predecesores):
        camino = []
        actual = destino

        while actual is not None:
            camino.append(actual)
            actual = predecesores[actual]

        camino.reverse()
        return camino

    def _calcular_costo(self, camino):
        costo = 0

        for posicion in range(len(camino) - 1):
            costo += self._grafo.obtener_peso(
                camino[posicion],
                camino[posicion + 1]
            )

        return costo
