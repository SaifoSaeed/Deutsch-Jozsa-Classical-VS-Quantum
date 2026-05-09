import json
import argparse
import numpy as np
from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit, transpile
from qiskit.primitives import BackendSamplerV2
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
import logging
logging.getLogger("qiskit_ibm_runtime").setLevel(logging.ERROR)

def build_dj_oracle(n, f_type):
    qc = QuantumCircuit(n + 1)
    
    if f_type == "Constant":
        if np.random.randint(2) == 1:
            qc.x(n)
            
    else:
        mask = format(np.random.randint(1, 2**n), f'0{n}b')
        
        for i, bit in enumerate(mask):
            if bit == '1': 
                qc.x(i)
                
        for i in range(n):
            qc.cx(i, n)
            
        for i, bit in enumerate(mask):
            if bit == '1': 
                qc.x(i)
                
    return qc.to_gate(label="U_f")

def test_queries(real_flag, n_range):
    
    pm = None
    
    if real_flag:
        print("Authenticating IBMQ... Allocating least busy QPU.")
        with open("ibm-qc-apikey.json", 'r') as f:
            api_info = json.load(f)
        service = QiskitRuntimeService(channel="ibm_quantum_platform", token=api_info["apikey"])
        backend = service.least_busy(operational=True, simulator=False, min_num_qubits=127)
        sampler = SamplerV2(mode=backend)
        pm = generate_preset_pass_manager(target=backend.target, optimization_level=3)
    else:
        print("Instantiating local AerSimulator instance.")
        backend = AerSimulator()
        sampler = BackendSamplerV2(backend=backend)
        
    for n in n_range:
        for f_type in ["Constant", "Balanced"]:
            oracle = build_dj_oracle(n, f_type)
            qc = QuantumCircuit(n + 1, n)
            
            qc.x(n)
            qc.h(range(n + 1))
            
            qc.barrier()
            qc.compose(oracle, inplace=True)
            qc.barrier()
            
            qc.h(range(n))
            qc.measure(range(n), range(n))
            
            if pm:
                qc_isa = pm.run(qc)
            else:
                qc_isa = transpile(qc, backend)
                
            job = sampler.run([qc_isa], shots=1)
            res = job.result()
            
            meas_data = list(res[0].data.values())[0]
            counts = meas_data.get_counts()
            bitstring = list(counts.keys())[0]
            
            deduced_type = "Constant" if bitstring == "0" * n else "Balanced"
            
            print(f"[n={n} | Set: {f_type}] "
                  f"Queries: 1 | Output Reg: |{bitstring}> | Deduced: {deduced_type}")

def main(real_flag=False, min_n=3, max_n=20, step=1):
    n_range = [ i for i in range( min_n, max_n, step ) ]

    time_taken = test_queries(real_flag, n_range)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deutsch-Jozsa Qiskit Implementation")
    parser.add_argument('-r', '--real', action='store_true', help="Execute on IBM Quantum QPU via Qiskit Runtime")
    args = parser.parse_args()

    main(args.real)