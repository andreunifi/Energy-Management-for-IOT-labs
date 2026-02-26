import json
import copy
import os
import sys
import argparse

base_config = {
    "sim_step": 1,
    "sim_len": 7736400,
    "period": 120,
    "vref_bus": 3.3,
    "soc_init": 1.0,
    "selfdisch_factor": 0.0,
    "sensors": [
        {"name": "air_quality_sensor",  "current_on": "48.2", "current_idle": "0.002", "activation_time": "0", "time_on": "30"},
        {"name": "methane_sensor",       "current_on": "18",   "current_idle": "0.002", "activation_time": "0", "time_on": "30"},
        {"name": "temperature_sensor",   "current_on": "0.3",  "current_idle": "0.002", "activation_time": "0", "time_on": "6"},
        {"name": "mic_click_sensor",     "current_on": "0.15", "current_idle": "0.002", "activation_time": "0", "time_on": "12"}
    ],
    "mcu": {
        "states": [{"name": "ON", "current": "13", "time_on": "6"}],
        "current_idle": "0.002"
    },
    "rf": {
        "states": [{"name": "ON", "current": "0.1", "time_on": "24"}],
        "current_idle": "0.001"
    }
}

def validate_activation(sensor, act_time, period):
    """Ensure sensor finishes within the period."""
    time_on = int(sensor["time_on"])
    if act_time + time_on > period:
        print(f"ERROR: {sensor['name']} activation_time={act_time} + time_on={time_on} exceeds period={period}", file=sys.stderr)
        sys.exit(1)

def generate_config(activation_times: list[int], index: int, output_dir: str) -> str:
    os.makedirs(output_dir, exist_ok=True)
    config = copy.deepcopy(base_config)
    period = config["period"]

    for i, sensor in enumerate(config["sensors"]):
        validate_activation(sensor, activation_times[i], period)
        sensor["activation_time"] = str(activation_times[i])

    filename = os.path.join(output_dir, f"config_{index:05d}.json")
    with open(filename, "w") as f:
        json.dump(config, f, indent=4)

    return filename

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a simulator config with given sensor activation times.")
    parser.add_argument("--air",   type=int, required=True, help="activation_time for air_quality_sensor")
    parser.add_argument("--meth",  type=int, required=True, help="activation_time for methane_sensor")
    parser.add_argument("--temp",  type=int, required=True, help="activation_time for temperature_sensor")
    parser.add_argument("--mic",   type=int, required=True, help="activation_time for mic_click_sensor")
    parser.add_argument("--index", type=int, required=True, help="incremental config index (for filename)")
    parser.add_argument("--outdir", type=str, default="sim_settings", help="output directory for config files")
    args = parser.parse_args()

    activation_times = [args.air, args.meth, args.temp, args.mic]
    filename = generate_config(activation_times, args.index, args.outdir)
    print(filename)  # shell script reads this