# Part1
The result obtained trying different timeout are stored inside
'dpm-simulator/results/part1'

The timeout time have been choosing given this algorithm:
- Obtain T_{BE}
- Initialize 'i'
- Iterate the script trying 'i * T_{BE}'
- Check the difference of number of transition between 
    the current simulation and the 
    previous one (in case of the 
    first simulation the difference is != 0)
- If the difference is 0, so the number of transition is equal,
    make i = i * 2 (Since we are in a space where the times of inactivity are long enough to have zero change between a timeout and the next one)
- If the difference is != 0, make i = i + 1
- When the number of transition is 0 exit the loop

Having this algorithm we're able to simulate the psm, and considering significant timeout value.
The result obtained are pretty easy to confirm studying the psm (analyze\_psm.py helps to read the psm file)
So analyzing the table created with (create\_data.py) and read with (read\_data.py) are that at timeout = 0 the energy
consumed is the lowest.
This is due to the psm definition, since the energy cost to go from RUN to IDLE is pretty low (near to 0) and the 
duration itself id low too.
Given this consideration, is obvious that with a longer timeout, especially longer than breakeven time, the energy consumed is higher and higher

Important code to execute:
- python3 create\_data.py --workload wl
- python3 read\_data.py --workload wl

In any way it is possible to make 
python3 script.py --help
to understand

# Part2
This time is possible to choice to execute the dpm with RUN-\>IDLE or RUN-\>SLEEP policy.
create\_data.py is updated to make possible this task:
- python3 create\_data.py --workload wl --timeoutpolicy to\_pol

This time even the make file is modified, since is needed to build the simulator with 2 possible policies.
To do so:
- make idle
- make sleep
were added to the makefile
