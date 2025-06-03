import matplotlib.pyplot as plt
import networkx as nx
import threading
import time
import os

G = nx.DiGraph()
pos = {}
fig, ax = plt.subplots(figsize=(12, 6))


nodos_por_nivel = 5
nodo = 0
niveles = []

for i in range(13):  
    nivel = []
    for j in range(nodos_por_nivel if i > 0 else 1):  
        nivel.append(nodo)
        pos[nodo] = (i, -j)
        nodo += 1
    niveles.append(nivel)


nodo_final = nodo  
G.add_node(nodo_final)
pos[nodo_final] = (13, -2)  
niveles.append([nodo_final])  


for i in range(len(niveles) - 1):
    for u in niveles[i]:
        for v in niveles[i + 1]:
            G.add_edge(u, v)


def draw_base():
    ax.clear()
    nx.draw(G, pos, ax=ax, with_labels=True, node_size=300, arrowsize=10,
            node_color='lightgray', edge_color='gray')
    fig.canvas.draw()


def leer_ruta_csv():
    if not os.path.exists("actual.csv"):
        return []
    with open("actual.csv", "r") as f:
        linea = f.readline().strip().strip(',')
        if not linea:
            return []
        try:
            return list(map(int, linea.split(',')))
        except:
            return []


def actualizar_ruta():
    while True:
        draw_base()
        ruta = leer_ruta_csv()
        if len(ruta) > 1:
            edges_en_ruta = list(zip(ruta[:-1], ruta[1:]))
            nx.draw_networkx_edges(G, pos, edgelist=edges_en_ruta, ax=ax,
                                   edge_color='red', width=2)
            nx.draw_networkx_nodes(G, pos, nodelist=ruta, ax=ax,
                                   node_color='orange', node_size=350)
        fig.canvas.draw()
        time.sleep(1)

threading.Thread(target=actualizar_ruta, daemon=True).start()
plt.show()
