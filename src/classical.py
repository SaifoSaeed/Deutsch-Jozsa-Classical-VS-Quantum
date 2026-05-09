import numpy as np
import time

#Random oracle generator.
def generate_dj_oracle(n):
    domain_size = 1 << n
    #Approx. half will be constant.
    is_constant = np.random.choice([True, False])
    
    if is_constant:
        output_val = np.random.choice([0, 1])
        truth_table = np.full(domain_size, output_val)
        f_type = "Constant"
    else:
        truth_table = np.concatenate([
            np.zeros(domain_size >> 1, dtype=int), 
            np.ones(domain_size >> 1, dtype=int)
        ])
        np.random.shuffle(truth_table)
        f_type = "Balanced"
        
    func = lambda x: truth_table[x]
    
    return func, f_type

#Find number of classical queries experimentally.
def test_queries(n_range=[3,4,5]):
    query_counts = []
    efficiency = []
    time_taken = []
    for n_val in n_range:
        func, f_type = generate_dj_oracle(n_val)
        start_t = time.perf_counter()
        print(f"Generated Type: {f_type}")
        
        query_count, zero_count, one_count = 0, 0, 0
        found_type = ""
        
        space = (2**n_val) - 1
        max_lim = (2**(n_val-1)) + 1

        for i in range(space):  #No limit set for attempts, but logical break at max_lim.
            query_count+=1
            query = func(i)
            
            if query == 1:
                one_count+=1
            else:
                zero_count+=1

            sum = one_count + zero_count
            if sum > 1:
                if (one_count == max_lim and zero_count == 0) or (one_count == 0 and zero_count == max_lim):
                    found_type = "Constant"

                elif (one_count < max_lim and zero_count > 0) or (one_count > 0 and zero_count < max_lim):
                    found_type = "Balanced"

            if found_type == f_type:
                end_t = time.perf_counter()
                query_counts.append(query_count)
                efficiency.append(query_count/max_lim)
                time_taken.append(end_t - start_t)
                break

    return query_counts, efficiency, time_taken

def main(min_n=3, max_n=20, step=1):
    n_range = [ i for i in range( min_n, max_n, step ) ]

    query_counts, efficiency, time_taken = test_queries(n_range)
    print(f"query_counts = {query_counts}")
    print(f"efficiency = {efficiency}")
    print(f"time_taken = {time_taken}")

    return

if __name__ == "__main__":
    main()