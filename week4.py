import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

#Defining a non-symmetrical traffic network
intersections = [
    'Farmgate', 'Karwan Bazar', 'Tejgaon', 'Mohakhali',
    'Gulshan-1', 'Gulshan-2', 'Banani', 'Airport', 
    'Uttara-10', 'Mirpur-10'
]

#Defining directional roads (edges)
roads = [
    ('Farmgate', 'Karwan Bazar'),
    ('Karwan Bazar', 'Tejgaon'),
    ('Tejgaon', 'Mohakhali'),
    ('Mohakhali', 'Gulshan-1'),
    ('Gulshan-1', 'Gulshan-2'),
    ('Gulshan-2', 'Banani'),
    ('Banani', 'Airport'),
    ('Airport', 'Uttara-10'),
    ('Tejgaon', 'Mirpur-10'),
    ('Mirpur-10', 'Farmgate'),
    ('Mohakhali', 'Banani'),
]

G = nx.DiGraph()
G.add_nodes_from(intersections)
G.add_edges_from(roads)

#Assigning λ and μ values
lambda_values = {
    'Farmgate': 9,
    'Karwan Bazar': 8,
    'Tejgaon': 10,
    'Mohakhali': 7,
    'Gulshan-1': 6,
    'Gulshan-2': 5,
    'Banani': 4,
    'Airport': 3,
    'Uttara-10': 2,
    'Mirpur-10': 6
}

mu_values = {
    'Farmgate': 7,
    'Karwan Bazar': 7,
    'Tejgaon': 8,
    'Mohakhali': 6,
    'Gulshan-1': 5,
    'Gulshan-2': 5,
    'Banani': 6,
    'Airport': 7,
    'Uttara-10': 5,
    'Mirpur-10': 6
}

#Calculating queue length and congestion
queue_lengths = {}
congestion_flags = {}

def calc_L(lmbda, mu):
    if mu > lmbda:
        return round(lmbda / (mu - lmbda), 2), "No"
    else:
        return float("inf"), "Yes"

for node in G.nodes:
    L, flag = calc_L(lambda_values[node], mu_values[node])
    queue_lengths[node] = L
    congestion_flags[node] = flag

#Visualization
node_colors = ['red' if congestion_flags[n] == "Yes" else 'green' for n in G.nodes]

pos = nx.spring_layout(G, seed=42)

plt.figure(figsize=(12, 8))
nx.draw(G, pos, with_labels=False, node_color=node_colors, node_size=1600, arrowsize=20)

#Adding node labels above, queue length below
for node, (x, y) in pos.items():
    plt.text(x, y + 0.08, node, fontsize=10, ha='center', fontweight='bold')
    q_val = queue_lengths[node]
    plt.text(x, y - 0.08, f"L={q_val if q_val != float('inf') else '∞'}", fontsize=9, color='blue', ha='center')

plt.title("Urban Traffic Simulation: Non-Symmetrical Layout (Week 4)", fontsize=14)
plt.axis('off')

#Printing the table BEFORE showing graph
df = pd.DataFrame({
    "Node": list(G.nodes),
    "λ (Arrival Rate)": [lambda_values[n] for n in G.nodes],
    "μ (Service Rate)": [mu_values[n] for n in G.nodes],
    "Queue Length (L)": [queue_lengths[n] for n in G.nodes],
    "Congestion?": [congestion_flags[n] for n in G.nodes]
})

print("\nQueue Length and Congestion Table (Realistic Layout):\n")
print(df.to_string(index=False))

plt.show()
