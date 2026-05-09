.PHONY: c_run, q_run

real_main:
	python main.py -r

sim_main:
	python main.py

c_run:
	python src/classical.py

q_run:
	python src/quantum.py