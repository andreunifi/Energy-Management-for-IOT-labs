.PHONY: run open basic_simulation dvs_simulation

ITER ?= 150
VAR ?= 0.2
NEWVDD ?= 14

basic_simulation: lab2_1.py
	python3 lab2_1.py --type basic_sim --iteration $(ITER) --variation $(VAR)

dvs_simulation: lab2_1.py
	python3 lab2_1.py --type dvs_sim --iteration $(ITER) --variation $(VAR) --newvdd $(NEWVDD)

run: lab2_1.py
	python3 lab2_1.py --type no_sim --variation $(VAR)

open: 
	nvim lab2_1.py
