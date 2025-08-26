# Import libraries
import networkx as nx
import matplotlib.pyplot as plt

#Defining a directed graph
G = nx.DiGraph()

#Adding nodes (intersections)
intersections = ['A', 'B', 'C', 'D', 'E']
G.add_nodes_from(intersections)

#Adding directed edges (roads) with travel time as weights (in minutes)
roads = [
    ('A', 'B', {'travel_time': 3}),
    ('B', 'C', {'travel_time': 2}),
    ('C', 'D', {'travel_time': 4}),
    ('D', 'E', {'travel_time': 2}),
    ('E', 'A', {'travel_time': 3}),
    ('A', 'C', {'travel_time': 5}),
    ('B', 'D', {'travel_time': 4}),
]
G.add_edges_from(roads)

#Identifying high-traffic nodes (e.g., based on congestion)
high_traffic_nodes = ['B']  # Mark node B as congested

#Assigning node colors: red = high traffic, skyblue = normal
node_colors = ['red' if node in high_traffic_nodes else 'skyblue' for node in G.nodes]

#Setting up the graph layout
pos = nx.spring_layout(G, seed=42)  # Positioning layout

#Plotting the graph
plt.figure(figsize=(10, 7))
nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=2000)
nx.draw_networkx_edges(G, pos, arrows=True, arrowstyle='->', arrowsize=20)
nx.draw_networkx_labels(G, pos, font_size=14, font_weight='bold')

#Adding edge labels (travel time in minutes)
edge_labels = {(u, v): f"{d['travel_time']} min" for u, v, d in G.edges(data=True)}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='gray', font_size=12)

#Adding title and displaying/saving the figure
plt.title("Urban Traffic Network Visualization", fontsize=16)
plt.axis('off')
plt.tight_layout()

#Saving the graph as an image
plt.savefig("urban_traffic_network_graph.png")  # This will save the image in the same folder
plt.show()  # Displaying the graph
