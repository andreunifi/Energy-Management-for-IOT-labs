#!/bin/bash

# -----------------------------
# Configuration
# -----------------------------
ITER=10
VARIATIONS=(0.05 0.1 0.15 0.20)
NEWVDDS=(14 13 12)
REPEATS=2

# -----------------------------
# Check input argument
# -----------------------------
if [ $# -eq 0 ]; then
    echo "Usage: $0 [basic | dvs | all]"
    exit 1
fi

MODE=$1

# -----------------------------
# Basic Simulation Function
# -----------------------------
run_basic() {
    echo "===== BASIC SIMULATIONS ====="
    for var in "${VARIATIONS[@]}"; do
        for ((i=1; i<=REPEATS; i++)); do
            echo "Running basic_sim | variation=$var | repeat=$i"
			make basic_simulation ITER=$ITER VAR=$var
        done
    done
}

# -----------------------------
# DVS Simulation Function
# -----------------------------
run_dvs() {
    echo "===== DVS SIMULATIONS ====="
    for var in "${VARIATIONS[@]}"; do
        for vdd in "${NEWVDDS[@]}"; do
            for ((i=1; i<=REPEATS; i++)); do
                echo "Running dvs_sim | variation=$var | newvdd=$vdd | repeat=$i"
				make dvs_simulation ITER=$ITER VAR=$var NEWVDD=$vdd
            done
        done
    done
}

# -----------------------------
# Mode Selection
# -----------------------------
case $MODE in
    basic)
        run_basic
        ;;
    dvs)
        run_dvs
        ;;
    all)
        run_basic
        run_dvs
        ;;
    *)
        echo "Invalid option: $MODE"
        echo "Usage: $0 [basic | dvs | all]"
        exit 1
        ;;
esac

echo "All requested simulations completed."

