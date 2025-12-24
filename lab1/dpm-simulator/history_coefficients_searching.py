from concurrent.futures import ProcessPoolExecutor, as_completed
import itertools, subprocess, re, multiprocessing, sys

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
            return (None, params, result.stdout)
        energy = round(float(match.group(1)), 10)
        return (energy, params, None)
    except subprocess.TimeoutExpired:
        return (None, params, "TIMEOUT")

if __name__ == "__main__":
    # ====== PARAMETER RANGES ======
    #k0_values = [0.0, 2.5, 5.0] # First gen
    #k0_values = [0.0, 0.5, 1.0] # Second gen
    #k0_values = [0.5, 1.0, 1.5] # Nineth gen
    #k0_values = [1.0, 1.5, 2.0] # 13° gen
    #k0_values = [1.4, 1.5, 1.6] # 15° gen
    k0_values = [1.3, 1.4, 1.5] 

    #k1_values = [0.0, 2.5, 5.0] # Third gen
    #k1_values = [0.0, 0.5, 1.0] # 14° gen
    k1_values = [0.4, 0.5, 0.6]

    #k2_values = [0.0, 2.5, 5.0] # Fourth gen
    #k2_values = [2.0, 2.5, 3.0] # 10° gen
    k2_values = [3.0, 3.5, 4.0]

    #k3_values = [0.0, 2.5, 5.0] # Fifth gen
    #k3_values = [2.0, 2.5, 3.0] # Eigth gen
    #k3_values = [2.5, 3.0, 3.5] # 11° gen
    #k3_values = [3.0, 3.5, 4.0] # 12° gen
    k3_values = [3.5, 4.0, 4.5]

    #k4_values = [0.0, 2.5, 5.0] # Sixth gen
    #k4_values = [2.0, 2.5, 3.0] # Seventh gen
    k4_values = [2.5, 3.0, 3.5]

    param_combinations = list(itertools.product(k0_values, k1_values, k2_values, k3_values, k4_values))
    total = len(param_combinations)
    num_workers = multiprocessing.cpu_count()

    print(f"🔧 Running {total} simulations using {num_workers} cores...\n")

    results = []
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = {executor.submit(run_simulation, p): p for p in param_combinations}
        for i, future in enumerate(as_completed(futures), 1):
            energy, params, err = future.result()
            sys.stdout.write(f"\rProgress: {(i/total)*100:.2f}%")
            sys.stdout.flush()
            if energy is not None:
                results.append((energy, params))
            elif err:
                print(f"\n⚠️ Error with params {params}: {err[:200]}")

    results.sort()  # sort by energy
    best_energy, best_params = results[0] if results else (None, None)

    print("\n\n==== BEST RESULT ====")
    if best_params:
        print(f"Params: k0={best_params[0]}, k1={best_params[1]}, k2={best_params[2]}, k3={best_params[3]}, k4={best_params[4]}")
        print(f"Lowest Tot. Energy w DPM = {best_energy:.10f}J")
    else:
        print("No valid results found.")

