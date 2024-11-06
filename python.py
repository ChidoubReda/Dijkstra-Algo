# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 20:21:12 2024

@author: L13
"""

import networkx as nx
import matplotlib.pyplot as plt
import random
import string

def generate_random_graph(num_vertices):
    G = nx.gnp_random_graph(num_vertices, 0.5)
    
    # Générer les labels en alphabet pour les sommets
    labels = []
    alphabet = string.ascii_uppercase
    for i in range(num_vertices):
        if i < 26:
            labels.append(alphabet[i])
        else:
            labels.append(alphabet[(i // 26) - 1] + alphabet[i % 26])
    
    # Mapper les labels sur les sommets
    mapping = {i: labels[i] for i in range(num_vertices)}
    G = nx.relabel_nodes(G, mapping)
    
    # Ajouter un coût aléatoire (poids) pour chaque arête
    for (u, v) in G.edges():
        G.edges[u, v]['weight'] = random.randint(1, 9)
    
    return G

def dijkstra_shortest_path(G, source, target):
    # Calculer le plus court chemin et sa longueur avec Dijkstra
    try:
        path = nx.dijkstra_path(G, source, target, weight='weight')
        path_length = nx.dijkstra_path_length(G, source, target, weight='weight')
    except nx.NetworkXNoPath:
        path = None
        path_length = None
    
    return path, path_length

def draw_graph(G, pos, title="Graphe généré"):
    # Dessiner le graphe entier avec des arêtes en gris
    nx.draw(G, pos, with_labels=True, node_color="skyblue", font_size=10, font_weight="bold", edge_color="lightgray")
    
    # Afficher les poids des arêtes dans le graphe
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
    
    plt.title(title)
    plt.show()

def draw_graph_with_shortest_path(G, pos, path, path_length):
    # Dessiner le graphe entier avec des arêtes en gris
    nx.draw(G, pos, with_labels=True, node_color="skyblue", font_size=10, font_weight="bold", edge_color="lightgray")
    
    # Afficher les poids des arêtes dans le graphe
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
    
    # Dessiner le plus court chemin en rouge s'il existe
    if path:
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color="red", width=2)
        
        # Afficher la longueur du plus court chemin
        plt.title(f"Plus courte distance entre les sommets sélectionnés : {path_length}")
    else:
        plt.title("Aucun chemin trouvé entre les sommets sélectionnés.")
    
    plt.show()

def main():
    nodes = int(input("Saisir le nombre de sommets : "))
    G = generate_random_graph(nodes)
    
    # Générer une disposition fixe pour le graphe
    pos = nx.spring_layout(G)  # Cette disposition sera réutilisée pour tous les affichages
    
    # Afficher le graphe généré avec la disposition initiale
    draw_graph(G, pos, title="Graphe généré - Initial")

    # Demander les sommets source et cible à l'utilisateur
    source = input("Saisir le sommet de départ : ").upper()
    target = input("Saisir le sommet d'arrivée : ").upper()
    
    # Calculer le plus court chemin et sa distance
    path, path_length = dijkstra_shortest_path(G, source, target)
    
    if path:
        print(f"Le plus court chemin de {source} à {target} est : {' -> '.join(path)}")
        print(f"Distance totale : {path_length}")
    else:
        print(f"Aucun chemin trouvé entre {source} et {target}.")
    
    # Dessiner le graphe avec le chemin le plus court en rouge en utilisant la même disposition
    draw_graph_with_shortest_path(G, pos, path, path_length)

if __name__ == "__main__":
    main()
