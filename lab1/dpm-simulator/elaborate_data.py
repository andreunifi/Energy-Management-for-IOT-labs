import pandas as pd
import matplotlib.pyplot as plt
import argparse
import os

# === PARSE PARAMETERS ===
parser = argparse.ArgumentParser(description="Plot Energy and Transitions vs Timeout for a given workload")
parser.add_argument("--workload", type=int, default=1, choices=[1, 2],
                    help="Workload number to plot (1 or 2)")
args = parser.parse_args()
workload_num = args.workload

# === CONFIGURATION ===
table_file = f"results/workload{workload_num}/summary_table.csv"

# Check if file exists
if not os.path.exists(table_file):
    raise FileNotFoundError(f"CSV file not found: {table_file}. Run the create_table script first.")

# === LOAD DATA ===
df = pd.read_csv(table_file)

# Ensure numeric types
df['Timeout'] = pd.to_numeric(df['Timeout'], errors='coerce')
df['Energy'] = pd.to_numeric(df['Energy'], errors='coerce')
df['Transitions'] = pd.to_numeric(df['Transitions'], errors='coerce')

# Remove zero or negative timeouts for logarithmic plotting
#df = df[df['Timeout'] > 0]

# === PLOT: Energy vs Timeout (logarithmic x-axis) ===
plt.figure(figsize=(10, 6))
plt.plot(df['Timeout'], df['Energy'], marker='o', linestyle='-', color='blue', label='Energy')
#plt.xscale('log')
plt.xlabel('Timeout (log scale)')
plt.ylabel('Energy')
plt.title(f'Workload {workload_num}: Energy vs Timeout (Logarithmic)')
plt.grid(True, which="both", ls="--", linewidth=0.5)
plt.legend()
plt.tight_layout()
plt.show()

# === PLOT: Transitions vs Timeout (logarithmic x-axis) ===
plt.figure(figsize=(10, 6))
plt.plot(df['Timeout'], df['Transitions'], marker='x', linestyle='--', color='green', label='Transitions')
#plt.xscale('log')
plt.xlabel('Timeout (log scale)')
plt.ylabel('Number of Transitions')
plt.title(f'Workload {workload_num}: Transitions vs Timeout (Logarithmic)')
plt.grid(True, which="both", ls="--", linewidth=0.5)
plt.legend()
plt.tight_layout()
plt.show()

# === SUMMARY STATISTICS ===
print(f"\n=== Summary Statistics for Workload {workload_num} ===")
print(df.describe())

