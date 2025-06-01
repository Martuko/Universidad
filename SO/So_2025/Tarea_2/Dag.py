import matplotlib.pyplot as plt
import networkx as nx
import random
import threading
import time

G = nx.DiGraph()
pos = {}
fig, ax = plt.subplots(figsize=(12, 6))

# Crear grafo tipo DAG
nodos_por_nivel = 5
nodo = 0
niveles = []

for i in range(13):  # 13 niveles intermedios
    nivel = []
    for j in range(nodos_por_nivel if i > 0 else 1):  # Solo un nodo en el nivel 0
        nivel.append(nodo)
        pos[nodo] = (i, -j)
        nodo += 1
    niveles.append(nivel)

# Agregar nodo final (Casa)
nodo_final = nodo  # nodo == 61
G.add_node(nodo_final)
pos[nodo_final] = (13, -2)  # Posición final
niveles.append([nodo_final])  # Nivel 13

# Conectar nodos entre niveles
for i in range(len(niveles) - 1):
    for u in niveles[i]:
        for v in niveles[i + 1]:
            G.add_edge(u, v)

# Función para dibujar el grafo base
def draw_base():
    ax.clear()
    nx.draw(G, pos, ax=ax, with_labels=True, node_size=300, arrowsize=10,
            node_color='lightgray', edge_color='gray')
    fig.canvas.draw()

# Simular rutas
def actualizar_ruta():
    while True:
        ruta = [random.choice(niveles[i]) for i in range(14)]  # 14 niveles incluyendo 'Casa'
        draw_base()
        edges_en_ruta = list(zip(ruta[:-1], ruta[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=edges_en_ruta, ax=ax,
                               edge_color='red', width=2)
        nx.draw_networkx_nodes(G, pos, nodelist=ruta, ax=ax,
                               node_color='orange', node_size=350)
        fig.canvas.draw()
        time.sleep(1)

# Lanzar hilo
threading.Thread(target=actualizar_ruta, daemon=True).start()
plt.show()
