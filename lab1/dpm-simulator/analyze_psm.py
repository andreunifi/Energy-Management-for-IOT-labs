# Analyze_psm.py
# This script will analyze the PSM and obtain the BreakEven time

import os

def calculate_Tbe(T_tr, P_tr, P_on, P_off):
    if(P_tr < P_on) :
        return T_tr
    return T_tr + T_tr*(P_tr - P_on)/(P_on - P_off)

def Tbe_data():
    psm_filename = f"./example/psm.txt"
    if not os.path.exists(psm_filename):
        raise FileNotFoundError(f"PSM description not found: {psm_filename}")

    psm = open(psm_filename, "r")

    # The first line is the description of energy consumption in each state
    line = psm.readline()   
    tmp = line.split()
    RUN_Energy = float(tmp[0])
    IDLE_Energy = float(tmp[1])
    SLEEP_Energy = float(tmp[2])

    # Transition to RUN state
    line = psm.readline()
    tmp = line.split()  # RUN -> RUN ignored (index 0)
    IDLE2RUN            = tmp[1].split("/")
    IDLE2RUN_Energy     = float(IDLE2RUN[0])
    IDLE2RUN_Time       = float(IDLE2RUN[1])
    SLEEP2RUN           = tmp[2].split("/")
    SLEEP2RUN_Energy    = float(SLEEP2RUN[0])
    SLEEP2RUN_Time      = float(SLEEP2RUN[1])

    # Transition to IDLE state
    line = psm.readline()
    tmp = line.split()  # IDLE -> IDLE ignored (index 1)
    RUN2IDLE            = tmp[0].split("/")
    RUN2IDLE_Energy     = float(RUN2IDLE[0])
    RUN2IDLE_Time       = float(RUN2IDLE[1])
    SLEEP2IDLE          = tmp[2].split("/")
    SLEEP2IDLE_Energy   = float(SLEEP2IDLE[0])
    SLEEP2IDLE_Time     = float(SLEEP2IDLE[1])

    # Transition to SLEEP state
    line = psm.readline()
    tmp = line.split()  # SLEEP -> SLEEP ignored (index 2)
    RUN2SLEEP           = tmp[0].split("/")
    RUN2SLEEP_Energy    = float(RUN2SLEEP[0])
    RUN2SLEEP_Time      = float(RUN2SLEEP[1])
    IDLE2SLEEP          = tmp[1].split("/")
    IDLE2SLEEP_Energy   = float(IDLE2SLEEP[0])
    IDLE2SLEEP_Time     = float(IDLE2SLEEP[1])

    # Lets compute the BreakEven Time of Run to Idle
    T_be_R2I = calculate_Tbe(RUN2IDLE_Time + IDLE2RUN_Time, max(RUN2IDLE_Energy, IDLE2RUN_Energy), RUN_Energy, IDLE_Energy) 
    # Lets compute the BreakEven Time of Run to Sleep
    T_be_R2S = calculate_Tbe(RUN2SLEEP_Time + SLEEP2RUN_Time, max(RUN2SLEEP_Energy, SLEEP2RUN_Energy), RUN_Energy, SLEEP_Energy) 

    return (T_be_R2I, T_be_R2S)


def main() :
    psm_filename = f"./example/psm.txt"
    if not os.path.exists(psm_filename):
        raise FileNotFoundError(f"PSM description not found: {psm_filename}")

    psm = open(psm_filename, "r")

    # The first line is the description of energy consumption in each state
    line = psm.readline()   
    tmp = line.split()
    RUN_Energy = float(tmp[0])
    IDLE_Energy = float(tmp[1])
    SLEEP_Energy = float(tmp[2])

    # Transition to RUN state
    line = psm.readline()
    tmp = line.split()  # RUN -> RUN ignored (index 0)
    IDLE2RUN            = tmp[1].split("/")
    IDLE2RUN_Energy     = float(IDLE2RUN[0])
    IDLE2RUN_Time       = float(IDLE2RUN[1])
    SLEEP2RUN           = tmp[2].split("/")
    SLEEP2RUN_Energy    = float(SLEEP2RUN[0])
    SLEEP2RUN_Time      = float(SLEEP2RUN[1])

    # Transition to IDLE state
    line = psm.readline()
    tmp = line.split()  # IDLE -> IDLE ignored (index 1)
    RUN2IDLE            = tmp[0].split("/")
    RUN2IDLE_Energy     = float(RUN2IDLE[0])
    RUN2IDLE_Time       = float(RUN2IDLE[1])
    SLEEP2IDLE          = tmp[2].split("/")
    SLEEP2IDLE_Energy   = float(SLEEP2IDLE[0])
    SLEEP2IDLE_Time     = float(SLEEP2IDLE[1])

    # Transition to SLEEP state
    line = psm.readline()
    tmp = line.split()  # SLEEP -> SLEEP ignored (index 2)
    RUN2SLEEP           = tmp[0].split("/")
    RUN2SLEEP_Energy    = float(RUN2SLEEP[0])
    RUN2SLEEP_Time      = float(RUN2SLEEP[1])
    IDLE2SLEEP          = tmp[1].split("/")
    IDLE2SLEEP_Energy   = float(IDLE2SLEEP[0])
    IDLE2SLEEP_Time     = float(IDLE2SLEEP[1])

    # Print data
    print("RUN:  ", RUN_Energy) 
    print("IDLE: ", IDLE_Energy) 
    print("SLEEP:", SLEEP_Energy)

    print()

    print("RUN to IDLE   -> time: %4.2f, energy %4.2f" % (RUN2IDLE_Time, RUN2IDLE_Energy))
    print("RUN to SLEEP  -> time: %4.2f, energy %4.2f" % (RUN2SLEEP_Time, RUN2SLEEP_Energy))

    print()

    print("IDLE to RUN   -> time: %4.2f, energy %4.2f" % (IDLE2RUN_Time, IDLE2RUN_Energy))
    print("IDLE to SLEEP -> time: %4.2f, energy %4.2f" % (IDLE2SLEEP_Time, IDLE2SLEEP_Energy))

    print()

    print("SLEEP to RUN  -> time: %4.2f, energy %4.2f" % (SLEEP2RUN_Time, SLEEP2RUN_Energy))
    print("SLEEP to IDLE -> time: %4.2f, energy %4.2f" % (SLEEP2IDLE_Time, SLEEP2IDLE_Energy))

    # Lets compute the BreakEven Time of Run to Idle
    T_be_R2I = calculate_Tbe(RUN2IDLE_Time + IDLE2RUN_Time, max(RUN2IDLE_Energy, IDLE2RUN_Energy), RUN_Energy, IDLE_Energy) 
    # Lets compute the BreakEven Time of Run to Sleep
    T_be_R2S = calculate_Tbe(RUN2SLEEP_Time + SLEEP2RUN_Time, max(RUN2SLEEP_Energy, SLEEP2RUN_Energy), RUN_Energy, SLEEP_Energy) 

    print()
    
    print("Time of Breakeven for Run to Idle:  ", T_be_R2I); 
    print("Time of Breakeven for Run to Sleep: ", T_be_R2S);

    return (T_be_R2I, T_be_R2S)

if __name__ == "__main__":
    main()
