import csv
import concurrent.futures
from collections import OrderedDict
import numpy as np  # Added import for NaN handling
import time  # Added import for measuring execution time

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        if key in self.cache:
            # Move the accessed key to the end
            self.cache.move_to_end(key)
            return self.cache[key]
        return -1

    def put(self, key, value):
        if key in self.cache:
            # Move the existing key to the end
            self.cache.move_to_end(key)
        elif len(self.cache) >= self.capacity:
            # Remove the first (least recently used) item
            self.cache.popitem(last=False)
        self.cache[key] = value

class LFUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        self.frequency = {}

    def get(self, key):
        if key in self.cache:
            # Increment frequency and move to the correct heap
            self.frequency[key] += 1
            return self.cache[key]
        return -1

    def put(self, key, value):
        if self.capacity > 0:
            if key in self.cache:
                # Update value and increment frequency
                self.cache[key] = value
                self.frequency[key] += 1
            else:
                # Check and remove the least frequently used item if at capacity
                if len(self.cache) >= self.capacity:
                    min_key = min(self.frequency, key=lambda k: (self.frequency[k], k))
                    del self.cache[min_key]
                    del self.frequency[min_key]
                # Add new item
                self.cache[key] = value
                self.frequency[key] = 1

class FIFOCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        return self.cache.get(key, -1)

    def put(self, key, value):
        if key in self.cache:
            # Update value
            self.cache[key] = value
        elif len(self.cache) >= self.capacity:
            # Remove the first (oldest) item
            self.cache.popitem(last=False)
        self.cache[key] = value

def simulate(cpu_operations, cache_type, cache_capacity, output_filename):
    if cache_type == 'LRU':
        cache = LRUCache(cache_capacity)
    elif cache_type == 'LFU':
        cache = LFUCache(cache_capacity)
    elif cache_type == 'FIFO':
        cache = FIFOCache(cache_capacity)
    else:
        raise ValueError("Invalid cache type. Choose from 'LRU', 'LFU', or 'FIFO'.")

    results = []

    with open(output_filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Operation', 'Cache Size', 'Result'])

        for i, operation in enumerate(cpu_operations):
            op_type, *op_args = operation

            if op_type == 'get':
                key = op_args[0]
                result = cache.get(key)
                results.append(result)
                cache_size = len(cache.cache)
                print(f"Operation {i + 1}: Cache Size: {cache_size}, Result: {result}")
                csvwriter.writerow([f'Operation {i + 1}', cache_size, result])

            elif op_type == 'put':
                key, value = op_args
                cache.put(key, value)
                cache_size = len(cache.cache)
                print(f"Operation {i + 1}: Cache Size: {cache_size}, Cache Updated: {cache.cache}")
                csvwriter.writerow([f'Operation {i + 1}', cache_size, 'N/A'])

            elif op_type == 'compute':
                # Simulate a CPU compute operation (no effect on cache in this example)
                print(f"Operation {i + 1}: Compute Task Executed")

            else:
                print(f"Operation {i + 1}: Unknown Operation")

    return results

def simulate_sequential(cpu_operations, cache_types, cache_capacity, output_filenames):
    for cache_type, output_filename in zip(cache_types, output_filenames):
        simulate(cpu_operations, cache_type, cache_capacity, output_filename)

def simulate_parallel(cpu_operations, cache_types, cache_capacity, output_filenames):
    with concurrent.futures.ThreadPoolExecutor() as executor:  # Change to ProcessPoolExecutor for parallel processes
        futures = [executor.submit(simulate, cpu_operations, cache_type, cache_capacity, output_filename)
                   for cache_type, output_filename in zip(cache_types, output_filenames)]
        concurrent.futures.wait(futures)

def simulate_with_metrics(cpu_operations, cache_type, cache_capacity, output_filename):
    cache_hits = 0
    cache_misses = 0

    if cache_type == 'LRU':
        cache = LRUCache(cache_capacity)
    elif cache_type == 'LFU':
        cache = LFUCache(cache_capacity)
    elif cache_type == 'FIFO':
        cache = FIFOCache(cache_capacity)
    else:
        raise ValueError("Invalid cache type. Choose from 'LRU', 'LFU', or 'FIFO'.")

    with open(output_filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Operation', 'Cache Size', 'Result'])

        for i, operation in enumerate(cpu_operations):
            op_type, *op_args = operation

            if op_type == 'get':
                key = op_args[0]
                result = cache.get(key)
                cache_size = len(cache.cache)
                if result != -1:
                    cache_hits += 1
                else:
                    cache_misses += 1

                print(f"Operation {i + 1}: Cache Size: {cache_size}, Result: {result}")
                csvwriter.writerow([f'Operation {i + 1}', cache_size, result])

            elif op_type == 'put':
                key, value = op_args
                cache.put(key, value)
                cache_size = len(cache.cache)
                print(f"Operation {i + 1}: Cache Size: {cache_size}, Cache Updated: {cache.cache}")
                csvwriter.writerow([f'Operation {i + 1}', cache_size, 'N/A'])

            elif op_type == 'compute':
                # Simulate a CPU compute operation (no effect on cache in this example)
                print(f"Operation {i + 1}: Compute Task Executed")

            else:
                print(f"Operation {i + 1}: Unknown Operation")

    total_operations = len(cpu_operations)
    miss_rate = cache_misses / total_operations if total_operations > 0 else 0.0
    hit_rate = cache_hits / total_operations if total_operations > 0 else 0.0

    print("\nCache Simulation Metrics:")
    print(f"Total Hits: {cache_hits}")
    print(f"Total Misses: {cache_misses}")
    print(f"Miss Rate: {miss_rate * 100:.2f}%")
    print(f"Hit Rate: {hit_rate * 100:.2f}%")

    return cache_hits, cache_misses, miss_rate

def simulate_sequential_with_metrics(cpu_operations, cache_types, cache_capacity, output_filenames):
    total_hits = 0
    total_misses = 0

    start_time = time.time()

    for cache_type, output_filename in zip(cache_types, output_filenames):
        cache_hits, cache_misses, _ = simulate_with_metrics(cpu_operations, cache_type, cache_capacity, output_filename)
        total_hits += cache_hits
        total_misses += cache_misses

    end_time = time.time()
    total_execution_time = end_time - start_time

    print("\nTotal Metrics (Sequential):")
    print(f"Total Hits: {total_hits}")
    print(f"Total Misses: {total_misses}")
    total_operations = len(cpu_operations) * len(cache_types)
    miss_rate = total_misses / total_operations if total_operations > 0 else 0.0
    hit_rate = total_hits / total_operations if total_operations > 0 else 0.0
    print(f"Miss Rate: {miss_rate * 100:.2f}%")
    print(f"Hit Rate: {hit_rate * 100:.2f}%")
    print(f"Total Execution Time: {total_execution_time:.2f} seconds")

def simulate_parallel_with_metrics(cpu_operations, cache_types, cache_capacity, output_filenames):
    total_hits = 0
    total_misses = 0

    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(simulate_with_metrics, cpu_operations, cache_type, cache_capacity, output_filename)
                   for cache_type, output_filename in zip(cache_types, output_filenames)]
        concurrent.futures.wait(futures)

        for future in futures:
            cache_hits, cache_misses, _ = future.result()
            total_hits += cache_hits
            total_misses += cache_misses

    end_time = time.time()
    total_execution_time = end_time - start_time

    print("\nTotal Metrics (Parallel):")
    print(f"Total Hits: {total_hits}")
    print(f"Total Misses: {total_misses}")
    total_operations = len(cpu_operations) * len(cache_types)
    miss_rate = total_misses / total_operations if total_operations > 0 else 0.0
    hit_rate = total_hits / total_operations if total_operations > 0 else 0.0
    print(f"Miss Rate: {miss_rate * 100:.2f}%")
    print(f"Hit Rate: {hit_rate * 100:.2f}%")
    print(f"Total Execution Time: {total_execution_time:.2f} seconds")

# ... (existing code)

def main():
    # Read CPU operations from a text file
    with open("cpu_operations.txt", "r") as file:
        cpu_operations = [tuple(line.strip().split()) for line in file]

    # Set cache types and output filenames
    cache_types = ['LRU', 'LFU', 'FIFO']

    # Prompt user for cache size
    cache_capacity = int(input("Enter cache size: "))

    # Sequential execution with metrics
    output_filenames_sequential = [f'{cache_type}_sequential_results.csv' for cache_type in cache_types]
    simulate_sequential_with_metrics(cpu_operations, cache_types, cache_capacity, output_filenames_sequential)

    # Parallel execution with metrics
    output_filenames_parallel = [f'{cache_type}_parallel_results.csv' for cache_type in cache_types]
    simulate_parallel_with_metrics(cpu_operations, cache_types, cache_capacity, output_filenames_parallel)

if __name__ == "__main__":
    main()