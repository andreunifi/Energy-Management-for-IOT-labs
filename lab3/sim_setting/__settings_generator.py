import json
import copy
import os

# Base configuration provided previously
base_config = {
    "sim_step": 1,
    "sim_len": 7736400,
    "period": 120, 
    "vref_bus": 3.3,
    "soc_init": 1.0,
    "selfdisch_factor": 0.0,
    "sensors": [
        {"name": "air_quality_sensor", "current_on": "48.2", "current_idle": "0.002", "activation_time": "0", "time_on": "30"},
        {"name": "methane_sensor", "current_on": "18", "current_idle": "0.002", "activation_time": "0", "time_on": "30"},
        {"name": "temperature_sensor", "current_on": "0.3", "current_idle": "0.002", "activation_time": "0", "time_on": "6"},
        {"name": "mic_click_sensor", "current_on": "0.15", "current_idle": "0.002", "activation_time": "0", "time_on": "12"}
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

def generate_all_schedules():
    os.makedirs('sim_setting', exist_ok=True)
    period = base_config["period"]

    # 1. PARALLEL: All activate at time 0
    parallel_config = copy.deepcopy(base_config)
    for sensor in parallel_config['sensors']:
        sensor['activation_time'] = "0"
    
    with open('sim_setting/parallel.json', 'w') as f:
        json.dump(parallel_config, f, indent=4)
    print("Generated: sim_setting/parallel.json")

    # 2. SEQUENTIAL: Back-to-back activation
    seq_config = copy.deepcopy(base_config)
    current_time_offset = 0
    for sensor in seq_config['sensors']:
        sensor['activation_time'] = str(current_time_offset)
        current_time_offset += int(sensor['time_on'])
        
    with open('sim_setting/sequential.json', 'w') as f:
        json.dump(seq_config, f, indent=4)
    print("Generated: sim_setting/sequential.json")

    # 3. MAXIMIZE EVERYTHING: All components ON for the entire period
    max_config = copy.deepcopy(base_config)
    for sensor in max_config['sensors']:
        sensor['activation_time'] = "0"
        sensor['time_on'] = str(period)
    
    # Also maximize MCU and RF
    max_config['mcu']['states'][0]['time_on'] = str(period)
    max_config['rf']['states'][0]['time_on'] = str(period)

    with open('sim_setting/maximize_everything.json', 'w') as f:
        json.dump(max_config, f, indent=4)
    print("Generated: sim_setting/maximize_everything.json")

if __name__ == "__main__":
    generate_all_schedules()