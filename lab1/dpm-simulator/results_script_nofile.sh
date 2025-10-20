./dpm_simulator -psm example/psm.txt -wl ../workloads/workload_$1.txt -t "$2" \
| grep -E "N. of|Tot. Energy" \
| grep -Eo '[0-9]+(\.[0-9]+)?' \
| awk 'NR==1{first=$0} {last=$0} END{print first; print last}'

