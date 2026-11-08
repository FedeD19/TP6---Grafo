from graph import Graph

EQUIPOS = [
    ('Red Hat', 'notebook'),
    ('Debian', 'notebook'),
    ('Arch', 'notebook'),
    ('Manjaro', 'pc'),
    ('Fedora', 'pc'),
    ('Parrot', 'pc'),
    ('Ubuntu', 'pc'),
    ('Mint', 'pc'),
    ('Guaraní', 'servidor'),
    ('MongoDB', 'servidor'),
    ('Router 1', 'router'),
    ('Router 2', 'router'),
    ('Router 3', 'router'),
    ('Switch 1', 'switch'),
    ('Switch 2', 'switch'),
    ('Impresora', 'impresora'),
]

CONEXIONES = [
    ('Debian', 'Switch 1', 17),
    ('Ubuntu', 'Switch 1', 18),
    ('Mint', 'Switch 1', 80),
    ('Impresora', 'Switch 1', 22),
    ('Switch 1', 'Router 1', 29),
    ('Router 1', 'Router 2', 37),
    ('Router 1', 'Router 3', 43),
    ('Router 2', 'Red Hat', 25),
    ('Router 2', 'Guaraní', 9),
    ('Router 2', 'Router 3', 50),
    ('Router 3', 'Switch 2', 61),
    ('Switch 2', 'Manjaro', 40),
    ('Switch 2', 'Parrot', 12),
    ('Switch 2', 'MongoDB', 5),
    ('Switch 2', 'Fedora', 3),
    ('Switch 2', 'Arch', 56),
]


def crear_red():
    grafo = Graph(is_dir=False)
    for nombre, tipo in EQUIPOS:
        grafo.add_vertex(nombre, {'tipo': tipo})
    for origen, destino, peso in CONEXIONES:
        grafo.add_edge(peso, origen, destino)
    return grafo


def camino_minimo(grafo, origen, destino):
    pila = grafo.dijkstra(origen)
    datos = {}

    while pila.size() > 0:
        nombre, costo, anterior = pila.pop()
        datos[nombre] = (costo, anterior)

    if destino not in datos or datos[destino][0] == float('inf'):
        return [], float('inf')

    recorrido = []
    actual = destino
    while actual is not None:
        recorrido.insert(0, actual)
        actual = datos[actual][1]

    return recorrido, datos[destino][0]


def mostrar_camino(grafo, origen, destino):
    recorrido, costo = camino_minimo(grafo, origen, destino)
    if recorrido:
        print(f'{origen} -> {destino}: {" -> ".join(recorrido)} (peso {costo:g})')
    else:
        print(f'No hay camino entre {origen} y {destino}')


def recorridos_notebooks(grafo):
    # b) Recorrido en profundidad y en amplitud desde tres notebooks.
    for origen in ('Red Hat', 'Debian', 'Arch'):
        print(f'\nDFS desde {origen}:')
        grafo.deep_show(origen)
        print(f'BFS desde {origen}:')
        grafo.amplitude_show(origen)


def pc_mas_cercana_a_guarani(grafo):
    # e) Excluye notebooks; el enunciado pide PC.
    mejor = None
    for vertice in grafo:
        if vertice.other_values['tipo'] == 'pc':
            recorrido, costo = camino_minimo(grafo, vertice.value, 'Guaraní')
            if recorrido and (mejor is None or costo < mejor[0]):
                mejor = (costo, vertice.value, recorrido)
    return mejor


def computadora_del_switch_1_mas_cercana(grafo):
    # f) Solo PC y notebooks conectadas directamente con Switch 1.
    pos = grafo.search('Switch 1', 'value')
    switch = grafo[pos]
    mejor = None
    for arista in switch.edges:
        pos_equipo = grafo.search(arista.destination, 'value')
        equipo = grafo[pos_equipo]
        if equipo.other_values['tipo'] in ('pc', 'notebook'):
            recorrido, costo = camino_minimo(grafo, equipo.value, 'MongoDB')
            if recorrido and (mejor is None or costo < mejor[0]):
                mejor = (costo, equipo.value, recorrido)
    return mejor


def mover_impresora(grafo):
    # g) El diagrama no establece el peso de la NUEVA conexión.
    # Se utiliza 22, igual al de la conexión antigua, como ejemplo.
    grafo.delete_edge('Switch 1', 'Impresora')
    grafo.add_edge(22, 'Router 2', 'Impresora')



grafo = crear_red()
print(f'a/h) {len(grafo)} equipos, grafo no dirigido.')

print('\nb) Recorridos desde notebooks:')
recorridos_notebooks(grafo)

print('\nc) Caminos hacia la impresora:')
for equipo in ('Manjaro', 'Red Hat', 'Fedora'):
    mostrar_camino(grafo, equipo, 'Impresora')

print('\nd) Árbol de expansión mínima (Kruskal):')
arbol = grafo.kruskal('Red Hat')
peso_total = 0
for tramo in arbol.split(';'):
    origen, destino, peso = tramo.rsplit('-', 2)
    print(f'{origen} -- {destino}: {peso}')
    peso_total += float(peso)
print(f'Peso total del árbol: {peso_total:g}')

print('\ne) PC con menor camino al servidor Guaraní:')
costo, nombre, recorrido = pc_mas_cercana_a_guarani(grafo)
print(f'{nombre}: {" -> ".join(recorrido)} (peso {costo:g})')

print('\nf) Computadora de Switch 1 más cercana a MongoDB:')
costo, nombre, recorrido = computadora_del_switch_1_mas_cercana(grafo)
print(f'{nombre}: {" -> ".join(recorrido)} (peso {costo:g})')

print('\ng) Mover la impresora al Router 2 y repetir b):')
mover_impresora(grafo)
recorridos_notebooks(grafo)