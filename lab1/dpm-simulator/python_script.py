import subprocess
import os
import time

# Paths
results_dir = "results/workload1"
script_path = "./results_script.sh"
table_file = f"{results_dir}/summary_table.csv"

# Ensure directory exists
os.makedirs(results_dir, exist_ok=True)

# Timeout ranges
timeouts_int = range(0, 1001)                     # 0–1000
timeouts_float = [round(x * 0.1, 1) for x in range(0, 11)]  # 0.0–1.0
timeouts = list(dict.fromkeys(list(timeouts_int) + timeouts_float))
total = len(timeouts)

# Create / overwrite the summary table
with open(table_file, "w") as out:
    out.write("Timeout,Transitions,Energy\n")

# Main loop
for i, t in enumerate(timeouts, start=1):
    timeout_str = str(t)
    results_file = f"{results_dir}/results_{timeout_str}.txt"

    try:
        subprocess.run(
            ["bash", script_path, timeout_str],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except subprocess.CalledProcessError:
        continue

    if not os.path.exists(results_file):
        continue

    with open(results_file, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    if len(lines) < 2:
        continue

    num_transitions = lines[0]
    energy = lines[-1]

    with open(table_file, "a") as out:
        out.write(f"{timeout_str},{num_transitions},{energy}\n")

    # Print progress percentage
    percent = (i / total) * 100
    print(f"\rProgress: {percent:.1f}% ({i}/{total})", end="", flush=True)

    time.sleep(0.05)

print(f"\n✅ All results saved to {table_file}")

