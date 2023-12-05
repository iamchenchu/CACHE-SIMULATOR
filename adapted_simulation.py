import csv
import concurrent.futures
from collections import OrderedDict
import time

class AdaptiveFIFOCache:
    def __init__(self, capacity, decay_factor=0.5):
        self.capacity = capacity
        self.cache = OrderedDict()
        self.frequency = {}
        self.decay_factor = decay_factor

    def get(self, key):
        return self.cache.get(key, -1)

    def put(self, key, value):
        if self.capacity > 0:
            if key in self.cache:
                # Update value and decay frequencies
                self.cache[key] = value
                self.decay_frequencies(key)
            else:
                # Check and remove the least frequently used item if at capacity
                if len(self.cache) >= self.capacity:
                    min_key = min(self.frequency, key=lambda k: (self.frequency[k], k))
                    del self.cache[min_key]
                    del self.frequency[min_key]
                # Add new item and set initial frequency to 1
                self.cache[key] = value
                self.frequency[key] = 1

    def decay_frequencies(self, current_key):
        # Decay frequencies of all items except the current key
        for key in self.frequency:
            if key != current_key:
                self.frequency[key] *= self.decay_factor

class AdaptiveLRUCache:
    def __init__(self, capacity, decay_factor=0.5):
        self.capacity = capacity
        self.cache = OrderedDict()
        self.frequency = {}
        self.decay_factor = decay_factor

    def get(self, key):
        if key in self.cache:
            # Increment frequency and move the accessed key to the end
            self.frequency[key] += 1
            self.cache.move_to_end(key)
            return self.cache[key]
        return -1

    def put(self, key, value):
        if self.capacity > 0:
            if key in self.cache:
                # Update value, increment frequency, and decay frequencies
                self.cache[key] = value
                self.frequency[key] += 1
                self.cache.move_to_end(key)
                self.decay_frequencies(key)
            else:
                # Check and remove the least frequently used item if at capacity
                if len(self.cache) >= self.capacity:
                    min_key = min(self.frequency, key=lambda k: (self.frequency[k], k))
                    del self.cache[min_key]
                    del self.frequency[min_key]
                # Add new item and set initial frequency to 1
                self.cache[key] = value
                self.frequency[key] = 1

    def decay_frequencies(self, current_key):
        # Decay frequencies of all items except the current key
        for key in self.frequency:
            if key != current_key:
                self.frequency[key] *= self.decay_factor

class AdaptiveLFUCache:
    def __init__(self, capacity, decay_factor=0.5):
        self.capacity = capacity
        self.cache = OrderedDict()
        self.frequency = {}
        self.decay_factor = decay_factor

    def get(self, key):
        if key in self.cache:
            # Increment frequency and move the accessed key to the end
            self.frequency[key] += 1
            self.cache.move_to_end(key)
            return self.cache[key]
        return -1

    def put(self, key, value):
        if self.capacity > 0:
            if key in self.cache:
                # Update value, increment frequency, and decay frequencies
                self.cache[key] = value
                self.frequency[key] += 1
                self.cache.move_to_end(key)
                self.decay_frequencies(key)
            else:
                # Check and remove the least frequently used item if at capacity
                if len(self.cache) >= self.capacity:
                    min_key = min(self.frequency, key=lambda k: (self.frequency[k], k))
                    del self.cache[min_key]
                    del self.frequency[min_key]
                # Add new item and set initial frequency to 1
                self.cache[key] = value
                self.frequency[key] = 1

    def decay_frequencies(self, current_key):
        # Decay frequencies of all items except the current key
        for key in self.frequency:
            if key != current_key:
                self.frequency[key] *= self.decay_factor

def simulate(cpu_operations, cache_type, cache_capacity, output_filename):
    if cache_type == 'AdaptiveFIFO':
        cache = AdaptiveFIFOCache(cache_capacity, decay_factor=0.5)
    elif cache_type == 'AdaptiveLRU':
        cache = AdaptiveLRUCache(cache_capacity, decay_factor=0.5)
    elif cache_type == 'AdaptiveLFU':
        cache = AdaptiveLFUCache(cache_capacity, decay_factor=0.5)
    else:
        raise ValueError("Invalid cache type. Choose from 'AdaptiveFIFO', 'AdaptiveLRU', or 'AdaptiveLFU'.")

    results = []

    start_time = time.time()

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

    end_time = time.time()
    total_execution_time = end_time - start_time

    print("\nCache Simulation Metrics:")
    print(f"Total Execution Time: {total_execution_time:.2f} seconds")

    return results

def simulate_sequential(cpu_operations, cache_types, cache_capacity, output_filenames):
    for cache_type, output_filename in zip(cache_types, output_filenames):
        simulate(cpu_operations, cache_type, cache_capacity, output_filename)

def simulate_parallel(cpu_operations, cache_types, cache_capacity, output_filenames):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(simulate, cpu_operations, cache_type, cache_capacity, output_filename)
                   for cache_type, output_filename in zip(cache_types, output_filenames)]
        concurrent.futures.wait(futures)

def simulate_with_metrics(cpu_operations, cache_type, cache_capacity, output_filename):
    cache_hits = 0
    cache_misses = 0

    if cache_type == 'AdaptiveFIFO':
        cache = AdaptiveFIFOCache(cache_capacity, decay_factor=0.5)
    elif cache_type == 'AdaptiveLRU':
        cache = AdaptiveLRUCache(cache_capacity, decay_factor=0.5)
    elif cache_type == 'AdaptiveLFU':
        cache = AdaptiveLFUCache(cache_capacity, decay_factor=0.5)
    else:
        raise ValueError("Invalid cache type. Choose from 'AdaptiveFIFO', 'AdaptiveLRU', or 'AdaptiveLFU'.")

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

def main():
    with open("cpu_operations.txt", "r") as file:
        cpu_operations = [tuple(line.strip().split()) for line in file]

    cache_types = ['AdaptiveFIFO', 'AdaptiveLRU', 'AdaptiveLFU']
    cache_capacity = int(input("Enter cache size: "))

    output_filenames_sequential = [f'{cache_type}_sequential_results.csv' for cache_type in cache_types]
    simulate_sequential_with_metrics(cpu_operations, cache_types, cache_capacity, output_filenames_sequential)

    output_filenames_parallel = [f'{cache_type}_parallel_results.csv' for cache_type in cache_types]
    simulate_parallel_with_metrics(cpu_operations, cache_types, cache_capacity, output_filenames_parallel)

if __name__ == "__main__":
    main()
