import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import folium

#Defining area and downloading road network
place_center = (23.7571, 90.4004)  # Tejgaon center coordinates
G = ox.graph_from_point(place_center, dist=800, network_type='drive')
G = G.to_undirected()

#Selecting 20 key intersections (nodes) manually or randomly
all_nodes = list(G.nodes())
selected_nodes = all_nodes[:20]  # select first 20 for simplicity
congested_nodes = selected_nodes[:3]  # mark first 3 as congested

#Plotting static map using osmnx
fig, ax = ox.plot_graph(G, show=False, close=False, node_size=5, bgcolor='white')

#Getting node coordinates for drawing
positions = {node: (data['x'], data['y']) for node, data in G.nodes(data=True)}

#Plotting selected traffic model nodes in blue
nx.draw_networkx_nodes(
    G, pos=positions,
    nodelist=selected_nodes,
    node_color='blue',
    node_size=50,
    ax=ax,
    label='Traffic Nodes'
)

#Highlighting congested nodes in red
nx.draw_networkx_nodes(
    G, pos=positions,
    nodelist=congested_nodes,
    node_color='red',
    node_size=100,
    ax=ax,
    label='Congested Intersections'
)

#Labeling selected intersections with node ID
for node in selected_nodes:
    x, y = positions[node]
    ax.text(x, y, str(node), fontsize=6, color='black')

plt.title("Real Map Overlay: Tejgaon Traffic Model")
plt.legend()
plt.show()


