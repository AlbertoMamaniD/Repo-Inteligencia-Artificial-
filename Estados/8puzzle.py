import heapq

META = (1, 2, 3,
        4, 5, 6,
        7, 8, 0)

POS_META = {valor: i for i, valor in enumerate(META)}

def imprimir_tablero(estado):
    """Imprime el tablero 3x3 en un formato amigable"""
    for i in range(0, 9, 3):
        fila = estado[i:i+3]
        print(" ".join(str(x) if x != 0 else " " for x in fila))
    print()

def puede_mover(pos_cero, movimiento):
    """Verifica si el hueco (0) puede moverse en la dirección indicada"""
    fila, col = divmod(pos_cero, 3)
    if movimiento == 'U': return fila > 0     
    if movimiento == 'D': return fila < 2     
    if movimiento == 'L': return col > 0      
    if movimiento == 'R': return col < 2      
    return False

MOVIMIENTOS = {'U': -3, 'D': 3, 'L': -1, 'R': 1}

def vecinos(estado):
    """Genera los estados vecinos moviendo el hueco"""
    cero = estado.index(0)
    for mov, desplaz in MOVIMIENTOS.items():
        if puede_mover(cero, mov):
            nuevo_estado = list(estado)
            nueva_pos = cero + desplaz
            nuevo_estado[cero], nuevo_estado[nueva_pos] = nuevo_estado[nueva_pos], nuevo_estado[cero]
            yield tuple(nuevo_estado), mov

def manhattan(estado):
    """Heurística Manhattan: suma de las distancias de cada ficha a su posición meta"""
    distancia = 0
    for i, valor in enumerate(estado):
        if valor == 0:
            continue
        pos_meta = POS_META[valor]
        f1, c1 = divmod(i, 3)
        f2, c2 = divmod(pos_meta, 3)
        distancia += abs(f1 - f2) + abs(c1 - c2)
    return distancia

def a_estrella(inicio, meta=META):
    """Resuelve el 8-puzzle con búsqueda A* usando heurística Manhattan"""
    frontera = []
    heapq.heappush(frontera, (manhattan(inicio), 0, inicio, []))

    visitados = set()

    while frontera:
        f, g, estado, camino = heapq.heappop(frontera)

        if estado in visitados:
            continue
        visitados.add(estado)

        if estado == meta:
            return camino

        for nuevo_estado, movimiento in vecinos(estado):
            if nuevo_estado not in visitados:
                nuevo_g = g + 1
                nuevo_f = nuevo_g + manhattan(nuevo_estado)
                heapq.heappush(frontera, (nuevo_f, nuevo_g, nuevo_estado, camino + [movimiento]))

    return None  

if __name__ == "__main__":

    inicio = (8, 5, 6,
              2, 1, 0,
              4, 7, 3)

    print("Estado inicial:")
    imprimir_tablero(inicio)

    solucion = a_estrella(inicio)

    if solucion is None:
        print("No se encontró solución.")
    else:
        print("Solución encontrada en", len(solucion), "pasos:")
        print(solucion)

        actual = inicio
        print("\nResolviendo paso a paso:")
        imprimir_tablero(actual)
        for movimiento in solucion:
            for nuevo_estado, mov in vecinos(actual):
                if mov == movimiento:
                    actual = nuevo_estado
                    break
            print(f"Movimiento: {movimiento}")
            imprimir_tablero(actual)
