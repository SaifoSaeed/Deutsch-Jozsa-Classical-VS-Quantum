import argparse
import time
import numpy as np
import matplotlib.pyplot as plt
import src.classical as classical
import src.quantum as quantum

def run_experiment(real_flag, min_n, max_n, step, t):
    n_range = list(range(min_n, max_n, step))
    
    c_queries_runs, c_times_runs, q_times_runs = [], [], []
    
    for i in range(t):
        print(f"\n=== Iteration {i+1}/{t} ===")
        print("--- Running Classical ---")
        c_q, _, c_t = classical.test_queries(n_range)
        c_queries_runs.append(c_q)
        c_times_runs.append(c_t)
        
        print("--- Running Quantum ---")
        q_t = []
        for n in n_range:
            start_t = time.perf_counter()
            quantum.test_queries(real_flag, [n])
            end_t = time.perf_counter()
            q_t.append(end_t - start_t)
        q_times_runs.append(q_t)
        
    cq_arr = np.array(c_queries_runs)
    ct_arr = np.array(c_times_runs)
    qt_arr = np.array(q_times_runs)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Plot 1: Algorithmic Efficiency (Queries)
    ax1.plot(n_range, cq_arr.min(axis=0), 'o--', label='Classical (Best)')
    ax1.plot(n_range, cq_arr.mean(axis=0), 'o-', label='Classical (Avg)')
    ax1.plot(n_range, cq_arr.max(axis=0), 'o:', label='Classical (Worst)')
    ax1.plot(n_range, np.ones(len(n_range)), 's-', label='Quantum (O(1))')
    
    ax1.set(xlabel='Input Register Size (n)', ylabel='Queries Required', title='Oracle Query Complexity')
    ax1.legend(bbox_to_anchor=(0.02, 1.0), loc='upper left')
    ax1.grid(True)
    
    # Plot 2: Hardware/Sim Execution Time
    ax2.plot(n_range, ct_arr.min(axis=0), 'o--', label='Classical CPU (Best)')
    ax2.plot(n_range, ct_arr.mean(axis=0), 'o-', label='Classical CPU (Avg)')
    ax2.plot(n_range, ct_arr.max(axis=0), 'o:', label='Classical CPU (Worst)')
    ax2.plot(n_range, qt_arr.min(axis=0), 's--', label='Quantum Sim/QPU (Best)')
    ax2.plot(n_range, qt_arr.mean(axis=0), 's-', label='Quantum Sim/QPU (Avg)')
    ax2.plot(n_range, qt_arr.max(axis=0), 's:', label='Quantum Sim/QPU (Worst)')
    
    ax2.set(xlabel='Input Register Size (n)', ylabel='Wall-clock Time (s)', title='Execution Overhead')
    ax2.legend(bbox_to_anchor=(1.05, 0.1), loc='lower right')
    ax2.grid(True)
    
    plt.tight_layout()
    plt.savefig('benchmark.png', dpi = 600)
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deutsch-Jozsa Benchmark Runner")
    parser.add_argument('-r', '--real', action='store_true', help="Route payload to IBM QPU")
    parser.add_argument('-n', '--min', type=int, default=3, help="Minimum n value")
    parser.add_argument('-x', '--max', type=int, default=12, help="Maximum n value")
    parser.add_argument('-t', '--times', type=int, default=10, help="Number of repetitions per n")
    args = parser.parse_args()
        
    run_experiment(args.real, args.min, args.max, 1, args.times)