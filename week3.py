import pandas as pd

#Assigning λ (arrival rate) and μ (service rate) to each node
traffic_data = {
    'Node': ['A', 'B', 'C', 'D', 'E'],
    'Lambda (λ)': [5, 6, 4, 3, 5],  # arrival rates
    'Mu (μ)': [7, 5, 6, 4, 6]       # service rates
}

#Defining a function to compute queue length L = λ / (μ - λ)
def calculate_queue_length(lmbda, mu):
    if mu > lmbda:
        L = round(lmbda / (mu - lmbda), 2)
        congestion = "No"
    else:
        L = float('inf')  # infinite queue means congestion
        congestion = "Yes"
    return L, congestion

#Applying the function to each node
queue_lengths = []
congestion_flags = []

for i in range(len(traffic_data['Node'])):
    lmbda = traffic_data['Lambda (λ)'][i]
    mu = traffic_data['Mu (μ)'][i]
    L, flag = calculate_queue_length(lmbda, mu)
    queue_lengths.append(L)
    congestion_flags.append(flag)

#Building the final table
traffic_data['Queue Length (L)'] = queue_lengths
traffic_data['Congestion?'] = congestion_flags

df_queues = pd.DataFrame(traffic_data)
print(df_queues.head())
