import networkx as nx 
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import os  # ✅ Added to auto-open the GIF

nodes = ['Farmgate', 'Karwan Bazar', 'Tejgaon', 'Mohakhali', 'Gulshan-1',
         'Gulshan-2', 'Banani', 'Airport', 'Uttara-10', 'Mirpur-10']

edges = [
    ('Farmgate', 'Karwan Bazar'), ('Karwan Bazar', 'Tejgaon'), ('Tejgaon', 'Mohakhali'),
    ('Mohakhali', 'Gulshan-1'), ('Gulshan-1', 'Gulshan-2'), ('Gulshan-2', 'Banani'),
    ('Banani', 'Airport'), ('Airport', 'Uttara-10'),
    ('Tejgaon', 'Mirpur-10'), ('Gulshan-2', 'Mirpur-10')
]

# Queue values for 3 stages
queue_stages = {
    'Before': [float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), 2, 0.75, 0.67, float('inf')],
    'During': [12, 10, 9, 8, 7, 6, 4, 1, 0.8, 10],
    'After':  [8, 3.5, 4, 3, 5, 2, 2, 0.75, 0.67, 2.5]
}

G = nx.DiGraph()
G.add_nodes_from(nodes)
G.add_edges_from(edges)
pos = nx.spring_layout(G, seed=42)

fig, ax = plt.subplots(figsize=(10, 6))

def update(frame):
    ax.clear()
    stage = list(queue_stages.keys())[frame]
    Ls = queue_stages[stage]
    sizes = [500 + 100 * (l if l != float('inf') else 10) for l in Ls]
    colors = ['red' if l == float('inf') or l > 8 else 'green' for l in Ls]

    nx.draw(G, pos, node_color=colors, node_size=sizes, with_labels=False, arrows=True, ax=ax)
    labels = {n: f"{n}\nL={Ls[i]}" for i, n in enumerate(nodes)}
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=7, font_color='white', ax=ax)

    ax.set_title(f"Traffic Simulation - {stage}", fontsize=12)
    ax.axis('off')

ani = FuncAnimation(fig, update, frames=3, repeat=True, interval=1500)
ani.save("traffic_animation.gif", writer='pillow')
plt.close()
print("✅ Animated GIF saved as 'traffic_animation.gif'")

# ✅ Automatically open the GIF (Windows only)
os.startfile("traffic_animation.gif")

