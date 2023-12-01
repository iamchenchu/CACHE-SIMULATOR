import csv
import concurrent.futures
from collections import OrderedDict

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

def main():
    # Example usage:

    # Define CPU operations with cache hits, misses, and cache updates
    cpu_operations = [
    ('get', 2),
    ('put', 4, 40),
    ('get', 1),
    ('get', 2),
    ('put', 5, 50),
    ('compute'),
    ('get', 3),
    ('put', 6, 60),
    ('get', 2),
    ('put', 7, 70),
    ('get', 4),
    ('get', 5),
    ('put', 8, 80),
    ('compute'),
    ('get', 1),
    ('put', 9, 90),
    ('get', 6),
    ('get', 2),
    ('put', 10, 100),
    ('get', 3),
    ('compute'),
    ('get', 7),
    ('put', 11, 110),
    ('put', 12, 120),
    ('get', 8),
    ('get', 9),
    ('put', 13, 130),
    ('compute'),
    ('get', 4),
    ('put', 14, 140),
    ('get', 10),
]

    # Set cache types, capacity, and output filenames
    cache_types = ['LRU', 'LFU', 'FIFO']
    cache_capacity = 3

    # Sequential execution
    for cache_type in cache_types:
        output_filename = f'{cache_type}_sequential_results.csv'
        simulate(cpu_operations, cache_type, cache_capacity, output_filename)

    # Parallel execution
    output_filenames_parallel = [f'{cache_type}_parallel_results.csv' for cache_type in cache_types]
    simulate_parallel(cpu_operations, cache_types, cache_capacity, output_filenames_parallel)

if __name__ == "__main__":
    main()
