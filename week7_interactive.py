import osmnx as ox
import networkx as nx
import folium
import os
import webbrowser

#Downloading road network for Tejgaon area
place_center = (23.7571, 90.4004)  # Tejgaon central point
G = ox.graph_from_point(place_center, dist=800, network_type='drive')
G = G.to_undirected()

#Selecting 20 intersections and 3 congested nodes
selected_nodes = list(G.nodes())[:20]
congested_nodes = selected_nodes[:3]  # First 3 are congested

#Creating interactive folium map
m = folium.Map(location=place_center, zoom_start=16)

#Adding selected traffic model nodes (blue markers)
for node in selected_nodes:
    lat = G.nodes[node]['y']
    lon = G.nodes[node]['x']
    folium.CircleMarker(
        location=(lat, lon),
        radius=5,
        color='blue',
        fill=True,
        fill_opacity=0.7,
        popup=f"Node {node}"
    ).add_to(m)

#Highlighting congested nodes (red markers)
for node in congested_nodes:
    lat = G.nodes[node]['y']
    lon = G.nodes[node]['x']
    folium.CircleMarker(
        location=(lat, lon),
        radius=7,
        color='red',
        fill=True,
        fill_opacity=1,
        popup=f"🚨 Congestion at Node {node}"
    ).add_to(m)

#Saving the interactive map to an HTML file
map_file = "tejgaon_traffic_model.html"
m.save(map_file)

#Opening the map automatically in Google Chrome
full_path = os.path.abspath(map_file)
chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"

try:
    webbrowser.get(chrome_path).open("file://" + full_path)
    print("✅ Map saved and opened in Google Chrome.")
except:
    # Fallback to default browser if Chrome not found
    webbrowser.open("file://" + full_path)
    print("✅ Map saved. Opened in default browser (Chrome not found at expected path).")





