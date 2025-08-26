import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

# Updated realistic intersection names and edges
nodes = [
    'Farmgate', 'Karwan Bazar', 'Tejgaon', 'Mohakhali',
    'Gulshan-1', 'Gulshan-2', 'Banani', 'Airport',
    'Uttara-10', 'Mirpur-10'
]

edges = [
    ('Farmgate', 'Karwan Bazar'),
    ('Karwan Bazar', 'Tejgaon'),
    ('Tejgaon', 'Mohakhali'),
    ('Mohakhali', 'Gulshan-1'),
    ('Gulshan-1', 'Gulshan-2'),
    ('Gulshan-2', 'Banani'),
    ('Banani', 'Airport'),
    ('Airport', 'Uttara-10'),
    ('Tejgaon', 'Mirpur-10'),
    ('Gulshan-2', 'Mirpur-10'),
]

# Optimized traffic parameters
arrival_rates = {
    'Farmgate': 8, 'Karwan Bazar': 7, 'Tejgaon': 8, 'Mohakhali': 6,
    'Gulshan-1': 5, 'Gulshan-2': 4, 'Banani': 4, 'Airport': 3,
    'Uttara-10': 2, 'Mirpur-10': 5
}

service_rates = {
    'Farmgate': 9, 'Karwan Bazar': 9, 'Tejgaon': 10, 'Mohakhali': 8,
    'Gulshan-1': 6, 'Gulshan-2': 6, 'Banani': 6, 'Airport': 7,
    'Uttara-10': 5, 'Mirpur-10': 7
}

# M/M/1 Calculation
def calc_L(lmbda, mu):
    if mu > lmbda:
        return round(lmbda / (mu - lmbda), 2), "No"
    else:
        return float("inf"), "Yes"

queue_lengths = {}
congestion_flags = {}
for node in nodes:
    L, flag = calc_L(arrival_rates[node], service_rates[node])
    queue_lengths[node] = L
    congestion_flags[node] = flag

# Table output
df = pd.DataFrame({
    'Node': nodes,
    'λ (Arrival Rate)': [arrival_rates[n] for n in nodes],
    'μ (Service Rate)': [service_rates[n] for n in nodes],
    'Queue Length (L)': [queue_lengths[n] for n in nodes],
    'Congestion?': [congestion_flags[n] for n in nodes]
})

print(df)    

# Graph creation
G = nx.DiGraph()
G.add_nodes_from(nodes)
G.add_edges_from(edges)
pos = nx.spring_layout(G, seed=42)

# Node coloring
colors = ['green' if congestion_flags[node] == 'No' else 'red' for node in G.nodes]

# Draw graph
plt.figure(figsize=(12, 8))
nx.draw(G, pos, with_labels=False, node_color=colors, node_size=1800, arrowsize=20)
queue_labels = {node: f"{node}\nL={queue_lengths[node]}" for node in G.nodes}
nx.draw_networkx_labels(G, pos, labels=queue_labels, font_size=8, font_color='white', font_weight='bold')

plt.title("Post-Optimization Traffic Network (Week 5)", fontsize=14)
plt.axis('off')
plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)
plt.show()



