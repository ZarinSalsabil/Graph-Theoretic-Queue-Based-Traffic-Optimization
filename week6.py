import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Defining intersections
nodes = [
    'Farmgate', 'Karwan Bazar', 'Tejgaon', 'Mohakhali',
    'Gulshan-1', 'Gulshan-2', 'Banani', 'Airport',
    'Uttara-10', 'Mirpur-10'
]

# λ and μ values
lambda_before = {
    'Farmgate': 9, 'Karwan Bazar': 8, 'Tejgaon': 10, 'Mohakhali': 7,
    'Gulshan-1': 6, 'Gulshan-2': 5, 'Banani': 4, 'Airport': 3,
    'Uttara-10': 2, 'Mirpur-10': 6
}
mu_before = {
    'Farmgate': 7, 'Karwan Bazar': 7, 'Tejgaon': 8, 'Mohakhali': 6,
    'Gulshan-1': 5, 'Gulshan-2': 5, 'Banani': 6, 'Airport': 7,
    'Uttara-10': 5, 'Mirpur-10': 6
}
lambda_after = {
    'Farmgate': 8, 'Karwan Bazar': 7, 'Tejgaon': 8, 'Mohakhali': 6,
    'Gulshan-1': 5, 'Gulshan-2': 4, 'Banani': 4, 'Airport': 3,
    'Uttara-10': 2, 'Mirpur-10': 5
}
mu_after = {
    'Farmgate': 9, 'Karwan Bazar': 9, 'Tejgaon': 10, 'Mohakhali': 8,
    'Gulshan-1': 6, 'Gulshan-2': 6, 'Banani': 6, 'Airport': 7,
    'Uttara-10': 5, 'Mirpur-10': 7
}

# L calculation
def calc_L(lmbda, mu):
    return round(lmbda / (mu - lmbda), 2) if mu > lmbda else float('inf')

L_before_raw = [calc_L(lambda_before[n], mu_before[n]) for n in nodes]
L_after_raw = [calc_L(lambda_after[n], mu_after[n]) for n in nodes]

# Replacing inf with a capped value like 10 for plotting
L_before = [val if val != float('inf') else 10 for val in L_before_raw]
L_after = [val if val != float('inf') else 10 for val in L_after_raw]

# Improvement %
def improvement(lb, la):
    if lb == float('inf') and la != float('inf'):
        return 100.0
    elif lb == float('inf') and la == float('inf'):
        return 0.0
    else:
        return round((lb - la) / lb * 100, 2) if lb != 0 else 0.0

improvements = [improvement(L_before[i], L_after[i]) for i in range(len(nodes))]

# Table
df_compare = pd.DataFrame({
    'Node': nodes,
    'λ': [lambda_after[n] for n in nodes],
    'μ': [mu_after[n] for n in nodes],
    'L Before': L_before,
    'L After': L_after,
    'Improvement (%)': improvements
})

# Sensitivity: λ ±1
sensitive_nodes = ['Tejgaon', 'Farmgate', 'Mirpur-10']
sensitivity_data = []
for node in sensitive_nodes:
    base_lambda = lambda_after[node]
    mu = mu_after[node]
    for delta in [-1, 0, 1]:
        new_lambda = base_lambda + delta
        L = calc_L(new_lambda, mu)
        sensitivity_data.append({
            'Node': node,
            'λ': new_lambda,
            'μ': mu,
            'Queue Length (L)': L
        })
df_sensitivity = pd.DataFrame(sensitivity_data)

# Before vs After Plot
plt.figure(figsize=(12, 6))
x = np.arange(len(nodes))
width = 0.35
plt.bar(x - width/2, L_before, width, label='Before', color='lightcoral')
plt.bar(x + width/2, L_after, width, label='After', color='mediumseagreen')
plt.xticks(x, nodes, rotation=45)
plt.ylabel("Queue Length (L)")
plt.title("Queue Length Before vs After Optimization")
plt.legend()
plt.tight_layout()
plt.show()

# Heatmap-style View
plt.figure(figsize=(12, 6))
colors = ['red' if L > 6 else 'orange' if L > 3 else 'green' for L in L_after]
plt.bar(nodes, L_after, color=colors)
plt.xticks(rotation=45)
plt.ylabel("Queue Length (L After)")
plt.title("Post-Optimization Traffic Intensity (Heatmap View)")
plt.tight_layout()
plt.show()

# Showing tables
print("\n Queue Length Comparison Table:")
print(df_compare)
print("\n Sensitivity Analysis Table:")
print(df_sensitivity)


