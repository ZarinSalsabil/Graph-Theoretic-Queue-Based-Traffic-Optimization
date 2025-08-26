import math                  
import numpy as np           
import matplotlib.pyplot as plt
import collections         

 #Calculating the average number of vehicles in an M/M/c queue system
def mmc_queue_length(lam, mu, c):
    if lam <= 0:
        return 0.0    # If arrival rate is zero or negative, no queue forms, so returning 0
    rho = lam / (c * mu)   # Calculating traffic intensity
    if rho >= 1.0:
        return np.inf    # System is unstable if traffic intensity >= 1, so queue length tends to infinity
    lam_over_mu = lam / mu  # ratio
    # Sum over n=0 to c-1 for the probability calculation denominator
    sum_terms = sum((lam_over_mu ** n) / math.factorial(n) for n in range(c))
    # Last term in denominator for probability of zero vehicles in system P0
    last_term = (lam_over_mu ** c) / (math.factorial(c) * (1.0 - rho))
    P0 = 1.0 / (sum_terms + last_term)  # Probability system is empty (no vehicles)
    # Average number of vehicles waiting in queue (Lq)
    Lq = (P0 * (lam_over_mu ** c) * rho) / (math.factorial(c) * (1.0 - rho) ** 2)
    L = Lq + lam / mu  # Average number in system = in queue + in service
    return L  

mu = 10 
time_hours = np.arange(6, 22, 1)  # Hours from 6 AM to 9 PM in 1-hour intervals

def lambda_t(hour):
    # Defining time-dependent arrival rate λ(t) based on hour of the day
    if 7 <= hour <= 9:
        return 12.0  # Morning peak arrival rate
    elif 17 <= hour <= 19:
        return 14.0  # Evening peak arrival rate
    else:
        return 6.0   # Off-peak arrival rate

lanes_list = [1, 2, 3]  

def main():
    results = {c: [] for c in lanes_list}  # Initializing a dictionary to store results for each lane count
    for c in lanes_list:  # Loop over lane counts (1, 2, 3)
        for h in time_hours:  # Loop over each hour in the day
            lam = lambda_t(h)  # Getting arrival rate for this hour
            L = mmc_queue_length(lam, mu, c)  # Computing average vehicles in system
            results[c].append(L)  # Storing result in dictionary

    # Collecting all finite values for setting y-axis limits in the plot
    finite_vals = [v for vals in results.values() for v in vals if np.isfinite(v)]
    y_max = max(finite_vals) if finite_vals else 10.0  # Maximum finite queue length found
    y_cap = max(10.0, y_max * 1.6)  # Capping for y-axis to give space for plotting infinity markers

    plt.figure(figsize=(11, 6))  # Creating a figure with specific size
    for c in lanes_list:
        y = np.array(results[c], dtype=float)  # Converting results list to numpy array
        y_plot = np.where(np.isfinite(y), y, np.nan)  # Replacing infinite values with NaN for plotting
        plt.plot(time_hours, y_plot, marker='o', label=f"{c} Lane(s)")  # Plotting queue length over time

        # Finding indices where the queue length is infinite (unstable system)
        inf_indices = np.where(~np.isfinite(y))[0]
        for idx in inf_indices:
            hour = time_hours[idx]  # Hour at which instability occurs
            marker_y = y_cap * 0.98  # Positioning marker near top of y-axis
            plt.scatter([hour], [marker_y], marker='^', color='red', s=80, zorder=5)  # Red triangle marker
            plt.text(hour, marker_y * 1.04, "∞", fontsize=12, ha='center', va='bottom', color='red')  # Labeling infinity

    # Adding horizontal line showing high congestion threshold L=10
    plt.axhline(y=10, color='r', linestyle='--', linewidth=1.0, label='High Congestion Threshold (L=10)')
    # Highlighting morning and evening peak period on the plot
    plt.axvspan(7, 9, color='orange', alpha=0.15, label='Morning Peak (7-9)')
    plt.axvspan(17, 19, color='purple', alpha=0.12, label='Evening Peak (17-19)')

    # Setting plot title and axis labels
    plt.title("Time-Dependent Queue Length (M/M/c) — 1 vs 2 vs 3 Lanes", fontsize=14)
    plt.xlabel("Hour of Day")
    plt.ylabel("Average Vehicles in System (L)")
    plt.xticks(time_hours)  # Setting x-axis ticks for each hour
    plt.ylim(0, y_cap * 1.05)  # Setting y-axis limits to include all data and markers
    plt.grid(True, linestyle='--', alpha=0.5) 

    # Creating legend with ordered labels to avoid duplicates
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = collections.OrderedDict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(),
               loc='upper center', bbox_to_anchor=(0.5, 0.95), ncol=2, frameon=False)

    # Adding a note below the plot explaining the markers and rates
    plt.text(0.02, -0.15,
             "Note: '∞' markers indicate instability (arrival rate ≥ capacity).\n"
             "Service rate μ = 10 veh/min per lane. λ(t) = 12 (7-9), 14 (17-19), 6 otherwise.",
             transform=plt.gca().transAxes, fontsize=9, va='top')

    plt.tight_layout(rect=[0, 0.03, 1, 0.88])  
    plt.show()  # Displaying the plot
if __name__ == "__main__":
    main()  # Running main function if script is executed directly
