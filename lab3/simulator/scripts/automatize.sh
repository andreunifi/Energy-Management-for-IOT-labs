#!/usr/bin/env bash
# =============================================================================
# brute_force.sh — Exhaustive activation_time search for max battery life
#
# Iterates all combinations of sensor activation times in multiples of 10
# within 0–100s (capped so sensor finishes within the 120s period).
# Supports resume: if results.csv exists, skips already completed runs.
#
# Usage: ./brute_force.sh [output_dir]
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GENERATOR="/root/Energy-Management-for-IOT-labs/lab3/sim_setting/__settings_generator.py"
SIMULATE="${SIMULATE_CMD:-bash $SCRIPT_DIR/../../simulate.sh}"
OUTDIR="${1:-sim_settings}"
RESULTS_CSV="$SCRIPT_DIR/results.csv"
BEST_CSV="$SCRIPT_DIR/best_result.csv"

AIR_TIME_ON=30
METH_TIME_ON=30
TEMP_TIME_ON=6
MIC_TIME_ON=12
PERIOD=120
STEP=10

max_act() {
    local time_on=$1
    local cap=100
    local max=$(( PERIOD - time_on ))
    echo $(( max < cap ? max : cap ))
}

AIR_MAX=$(max_act $AIR_TIME_ON)
METH_MAX=$(max_act $METH_TIME_ON)
TEMP_MAX=$(max_act $TEMP_TIME_ON)
MIC_MAX=$(max_act $MIC_TIME_ON)

TOTAL=$(( ((AIR_MAX/STEP)+1) * ((METH_MAX/STEP)+1) * ((TEMP_MAX/STEP)+1) * ((MIC_MAX/STEP)+1) ))

echo "============================================================"
echo "  Brute-force energy simulation"
echo "  Combinations to test: $TOTAL"
echo "  Results → $RESULTS_CSV"
echo "============================================================"

# --- Resume logic ---
if [[ -f "$RESULTS_CSV" ]]; then
    LAST=$(tail -1 "$RESULTS_CSV" | cut -d',' -f1)
    if [[ "$LAST" =~ ^[0-9]+$ ]]; then
        RESUME_FROM=$LAST
        echo "  Resuming from index $RESUME_FROM"
    else
        RESUME_FROM=0
    fi
    # Recover best result from existing data
    BEST_LINE=$(tail -n +2 "$RESULTS_CSV" | sort -t',' -k6 -rn | head -1)
    BEST_LIFE=$(echo "$BEST_LINE" | cut -d',' -f6)
    BEST_LIFE="${BEST_LIFE:-0}"
else
    RESUME_FROM=0
    BEST_LIFE=0
    BEST_LINE=""
    echo "index,air_act,meth_act,temp_act,mic_act,battery_life_s" > "$RESULTS_CSV"
fi

INDEX=0

for air in $(seq 0 $STEP $AIR_MAX); do
for meth in $(seq 0 $STEP $METH_MAX); do
for temp in $(seq 0 $STEP $TEMP_MAX); do
for mic in $(seq 0 $STEP $MIC_MAX); do

    INDEX=$(( INDEX + 1 ))

    # Skip already completed runs
    if (( INDEX <= RESUME_FROM )); then
        continue
    fi

    CONFIG=$(python3 "$GENERATOR" \
        --air   "$air"   \
        --meth  "$meth"  \
        --temp  "$temp"  \
        --mic   "$mic"   \
        --index "$INDEX" \
        --outdir "$OUTDIR")

    SIM_OUTPUT=$(bash -c "$SIMULATE $CONFIG" 2>&1) || true

    LIFE=$(echo "$SIM_OUTPUT" | grep -oP '(?<=@)\d+(?= s)' | tail -1)
    LIFE="${LIFE:-0}"

    echo "$INDEX,$air,$meth,$temp,$mic,$LIFE" >> "$RESULTS_CSV"

    if [ "$LIFE" -gt "$BEST_LIFE" ] 2>/dev/null; then
        BEST_LIFE="$LIFE"
        BEST_LINE="$INDEX,$air,$meth,$temp,$mic,$LIFE"
    fi

    if (( INDEX % 100 == 0 )); then
        echo "  [$INDEX/$TOTAL] best so far: ${BEST_LIFE}s  (air=${air} meth=${meth} temp=${temp} mic=${mic})"
    fi

done
done
done
done

echo "index,air_act,meth_act,temp_act,mic_act,battery_life_s" > "$BEST_CSV"
echo "$BEST_LINE" >> "$BEST_CSV"

echo ""
echo "============================================================"
echo "  DONE — $INDEX configurations tested"
echo "  Best battery life: ${BEST_LIFE} s  (~$(( BEST_LIFE / 86400 )) days)"
echo "  Best config: $BEST_LINE"
echo "  Full results: $RESULTS_CSV"
echo "  Best result:  $BEST_CSV"
echo "============================================================"