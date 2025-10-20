import subprocess
import os
from concurrent.futures import ProcessPoolExecutor, as_completed
import pandas as pd
import argparse

# === PARSE PARAMETERS ===
parser = argparse.ArgumentParser(description="Run DPM simulations and create a summary table")
parser.add_argument("--workload", type=int, default=1, choices=[1, 2],
                    help="Workload number to run (1 or 2)")
args = parser.parse_args()
workload_num = str(args.workload)

# === CONFIGURATION ===
results_dir = f"results/workload{workload_num}"
script_path = "./results_script_nofile.sh"
table_file = f"{results_dir}/summary_table.csv"
max_workers = os.cpu_count() or 4  # use all available cores

# Ensure directory exists
os.makedirs(results_dir, exist_ok=True)

# Timeout ranges
timeouts_int = range(0, 1001)                      # 0–1000
timeouts_float = [round(x * 0.1, 1) for x in range(0, 11)]  # 0.0–1.0
timeouts = list(dict.fromkeys(list(timeouts_int) + timeouts_float))
total = len(timeouts)

# === FUNCTION TO RUN ONE SIMULATION ===
def run_timeout(t):
    timeout_str = str(t)
    try:
        result = subprocess.run(
            ["bash", script_path, workload_num, timeout_str],
            capture_output=True,
            text=True,
            check=True
        )
        lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
        if len(lines) >= 2:
            return timeout_str, lines[0], lines[-1]
    except subprocess.CalledProcessError:
        pass
    return None

# === MAIN EXECUTION ===
with open(table_file, "w") as out:
    out.write("Timeout,Transitions,Energy\n")

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(run_timeout, t): t for t in timeouts}
        completed = 0

        for future in as_completed(futures):
            completed += 1
            result = future.result()
            if result:
                timeout_str, transitions, energy = result
                out.write(f"{timeout_str},{transitions},{energy}\n")
                out.flush()

            percent = (completed / total) * 100
            print(f"\rProgress: {percent:.1f}% ({completed}/{total})", end="", flush=True)

print(f"\n✅ All results saved to {table_file}")

# === SORT THE TABLE ===
df = pd.read_csv(table_file)

# Convert Timeout to numeric for proper sorting
df['Timeout'] = pd.to_numeric(df['Timeout'], errors='coerce')

# Sort by Timeout
df = df.sort_values(by='Timeout').reset_index(drop=True)

# Save the sorted table (overwrite)
df.to_csv(table_file, index=False)

# Print the sorted table
print("\n=== Sorted Table ===")
print(df)

