import itertools
import subprocess
import re
import sys
import numpy as np

def run_simulation(params):
    k0, k1, k2, k3, k4 = params
    cmd = [
        "stdbuf", "-oL", "-eL", "./dpm_simulator",
        "-psm", "example/psm.txt",
        "-wl", "../workloads/workload_1.txt",
        "-h", str(k0), str(k1), str(k2), str(k3), str(k4), "0.8", "5"
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        match = re.search(r"Tot\. Energy w DPM\s*=\s*([\d\.Ee+-]+)J", result.stdout)
        if not match:
            print(f"\n⚠️ No energy found for params {params}")
            return None
        return round(float(match.group(1)), 10)
    except subprocess.TimeoutExpired:
        print(f"\n⏱️ Timeout for params {params}")
        return None

def refine_range(center, width, step, min_val=None, max_val=None):
    start = center - width/2
    end = center + width/2
    if min_val is not None: start = max(start, min_val)
    if max_val is not None: end = min(end, max_val)
    return np.arange(start, end + step/2, step)

if __name__ == "__main__":
    # Initial coarse ranges
    k0_values = np.arange(1.3, 1.6+0.05, 0.05)
    k1_values = np.arange(0.4, 0.6+0.05, 0.05)
    k2_values = np.arange(3.0, 4.0+0.25, 0.25)
    k3_values = np.arange(3.5, 4.5+0.25, 0.25)
    k4_values = np.arange(2.5, 3.5+0.25, 0.25)

    # Min/max bounds for safety
    k_bounds = {
        "k0": (1.0, 2.0),
        "k1": (0.0, 1.0),
        "k2": (2.0, 4.5),
        "k3": (3.0, 5.0),
        "k4": (2.0, 4.0)
    }

    iterations = 3  # number of refinement iterations
    step_reduction = 0.5  # reduce step by factor each iteration

    best_energy = float("inf")
    best_params = None

    for iter_num in range(1, iterations+1):
        print(f"\n🔹 Iteration {iter_num} - exploring {len(k0_values)*len(k1_values)*len(k2_values)*len(k3_values)*len(k4_values)} combinations")
        param_combinations = list(itertools.product(k0_values, k1_values, k2_values, k3_values, k4_values))
        total = len(param_combinations)

        for i, params in enumerate(param_combinations, 1):
            energy = run_simulation(params)
            sys.stdout.write(f"\rProgress: {(i / total) * 100:.2f}%")
            sys.stdout.flush()

            if energy is not None and energy < best_energy:
                best_energy = energy
                best_params = params

        # Refine ranges around best parameters
        if best_params:
            k0_values = refine_range(best_params[0], width=0.1, step=0.05*step_reduction, min_val=k_bounds["k0"][0], max_val=k_bounds["k0"][1])
            k1_values = refine_range(best_params[1], width=0.1, step=0.05*step_reduction, min_val=k_bounds["k1"][0], max_val=k_bounds["k1"][1])
            k2_values = refine_range(best_params[2], width=0.25, step=0.25*step_reduction, min_val=k_bounds["k2"][0], max_val=k_bounds["k2"][1])
            k3_values = refine_range(best_params[3], width=0.25, step=0.25*step_reduction, min_val=k_bounds["k3"][0], max_val=k_bounds["k3"][1])
            k4_values = refine_range(best_params[4], width=0.25, step=0.25*step_reduction, min_val=k_bounds["k4"][0], max_val=k_bounds["k4"][1])

    print("\n\n==== FINAL BEST RESULT ====")
    if best_params:
        print(f"Params: k0={best_params[0]:.3f}, k1={best_params[1]:.3f}, k2={best_params[2]:.3f}, "
              f"k3={best_params[3]:.3f}, k4={best_params[4]:.3f}")
        print(f"Lowest Tot. Energy w DPM = {best_energy:.10f}J")
    else:
        print("No valid results found.")

