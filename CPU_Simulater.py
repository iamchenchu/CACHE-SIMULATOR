import csv
from collections import OrderedDict
from heapq import heappush, heappop


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


def run_cache_simulation(cache, operations, filename):
    results = []
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Operation', 'Cache Size', 'Result'])
        for i, op in enumerate(operations):
            if op[0] == 'put':
                cache.put(op[1], op[2])
            elif op[0] == 'get':
                result = cache.get(op[1])
                results.append(result)
                cache_size = len(cache.cache)
                print(f"Operation {i + 1}: Cache Size: {cache_size}, Result: {result}")
                csvwriter.writerow([f'Operation {i + 1}', cache_size, result])
    return results


# Example usage:

# LRU Cache
lru_cache = LRUCache(3)
lru_operations = [('put', 1, 1), ('put', 2, 2), ('put', 3, 3), ('get', 2), ('put', 4, 4), ('get', 1)]
lru_results = run_cache_simulation(lru_cache, lru_operations, 'lru_results.csv')

# LFU Cache
lfu_cache = LFUCache(2)
lfu_operations = [('put', 1, 1), ('put', 2, 2), ('get', 1), ('put', 3, 3), ('get', 2)]
lfu_results = run_cache_simulation(lfu_cache, lfu_operations, 'lfu_results.csv')

# FIFO Cache
fifo_cache = FIFOCache(2)
fifo_operations = [('put', 1, 1), ('put', 2, 2), ('get', 1), ('put', 3, 3), ('get', 2)]
fifo_results = run_cache_simulation(fifo_cache, fifo_operations, 'fifo_results.csv')
