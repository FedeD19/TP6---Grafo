from graph import Graph


AMBIENTES = [
    'Cocina', 'Comedor', 'Cochera', 'Quincho', 'Baño 1', 'Baño 2',
    'Habitación 1', 'Habitación 2', 'Sala de estar', 'Terraza', 'Patio',
]

# El libro no especifica distancias para esta casa: se usan metros de ejemplo. Cocina y Patio tienen 5 aristas cada uno; los demás al menos 3
CONEXIONES = [
    ('Cocina', 'Comedor', 3),
    ('Cocina', 'Sala de estar', 8),
    ('Cocina', 'Patio', 4),
    ('Cocina', 'Quincho', 9),
    ('Cocina', 'Baño 1', 5),
    ('Patio', 'Quincho', 3),
    ('Patio', 'Cochera', 7),
    ('Patio', 'Terraza', 10),
    ('Patio', 'Sala de estar', 6),
    ('Comedor', 'Baño 1', 6),
    ('Comedor', 'Habitación 1', 8),
    ('Cochera', 'Quincho', 8),
    ('Cochera', 'Terraza', 11),
    ('Baño 1', 'Habitación 2', 7),
    ('Baño 2', 'Habitación 1', 3),
    ('Baño 2', 'Habitación 2', 4),
    ('Baño 2', 'Sala de estar', 5),
    ('Habitación 1', 'Sala de estar', 9),
    ('Habitación 2', 'Terraza', 6),
]


def crear_casa():
    # a/b Vértices y aristas en metros, sin dirección
    grafo = Graph(is_dir=False)
    for ambiente in AMBIENTES:
        grafo.add_vertex(ambiente)
    for origen, destino, metros in CONEXIONES:
        grafo.add_edge(metros, origen, destino)
    return grafo


def camino_minimo(grafo, origen, destino):
    pila = grafo.dijkstra(origen)
    datos = {}

    while pila.size() > 0:
        nombre, distancia, anterior = pila.pop()
        datos[nombre] = (distancia, anterior)

    if destino not in datos or datos[destino][0] == float('inf'):
        return [], float('inf')

    camino = []
    actual = destino
    while actual is not None:
        camino.insert(0, actual)
        actual = datos[actual][1]
    return camino, datos[destino][0]



grafo = crear_casa()
print(f'a) Cantidad de ambientes: {len(grafo)}')

print('\nb) Conexiones de cada ambiente:')
for vertice in grafo:
    print(f'{vertice.value}: {len(vertice.edges)} aristas')

print('\nc) Árbol de expansión mínima (Kruskal):')
arbol = grafo.kruskal('Cocina')
metros_totales = 0
for tramo in arbol.split(';'):
    origen, destino, metros = tramo.rsplit('-', 2)
    print(f'{origen} -- {destino}: {metros} m')
    metros_totales += float(metros)
print(f'Total de cable para conectar todos los ambientes: {metros_totales:g} m')

print('\nd) Del router al Smart TV (Dijkstra):')
camino, distancia = camino_minimo(grafo, 'Habitación 1', 'Sala de estar')
if camino:
    print(' -> '.join(camino))
    print(f'Cable necesario: {distancia:g} m')
else:
    print('No existe un camino entre esos ambientes.')