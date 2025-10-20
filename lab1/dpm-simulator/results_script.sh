./dpm_simulator -psm example/psm.txt -wl ../workloads/workload_1.txt -t $1 > results/workload1/time_$1.txt
cat results/workload1/time_$1.txt | grep -E "N. of|Tot. Energy" | grep -Eo '[0-9]+(\.[0-9]+)?' > results/workload1/results_$1.txt
rm results/workload1/time_$1.txt 
