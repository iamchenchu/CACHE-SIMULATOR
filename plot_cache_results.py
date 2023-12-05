import csv
import matplotlib.pyplot as plt
import numpy as np  # Added import for NaN handling

def plot_cache_results(csv_filenames, labels, title):
    for i, csv_filename in enumerate(csv_filenames):
        with open(csv_filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip the header

            operations = []
            cache_sizes = []
            results = []

            for row in reader:
                operations.append(row[0])
                cache_sizes.append(int(row[1]))
                result_value = row[2] if row[2] != 'N/A' else None
                results.append(result_value)

            # Plot Cache Sizes
            plt.figure(figsize=(12, 6))
            plt.plot(operations, cache_sizes, marker='o', linestyle='-', label=labels[i])
            plt.title(f'Cache Sizes Over Operations ({title})', fontsize=16)
            plt.xlabel('Operation', fontsize=14)
            plt.ylabel('Cache Size', fontsize=14)
            plt.legend(fontsize=12)
            plt.grid(True)
            plt.tight_layout()
            plt.show()

            # Plot Results
            plt.figure(figsize=(12, 6))
            results = [np.nan if result is None else result for result in results]
            plt.plot(operations, results, marker='o', linestyle='-', label=labels[i])
            plt.title(f'Results Over Operations ({title})', fontsize=16)
            plt.xlabel('Operation', fontsize=14)
            plt.ylabel('Result', fontsize=14)
            plt.legend(fontsize=12)
            plt.grid(True)
            plt.tight_layout()
            plt.show()

# Example usage:
# For FIFO
fifo_csv_filenames = ['AdaptiveFIFO_parallel_results.csv', 'AdaptiveFIFO_sequential_results.csv']
fifo_labels = ['P_FIFO', 'S_FIFO']
plot_cache_results(fifo_csv_filenames, fifo_labels, 'FIFO')

# For LRU
lru_csv_filenames = ['AdaptiveLRU_parallel_results.csv', 'AdaptiveLRU_sequential_results.csv']
lru_labels = ['P_LRU', 'S_LRU']
plot_cache_results(lru_csv_filenames, lru_labels, 'LRU')

# For LFU
lfu_csv_filenames = ['AdaptiveLFU_parallel_results.csv', 'AdaptiveLFU_sequential_results.csv']
lfu_labels = ['P_LFU', 'S_LFU']
plot_cache_results(lfu_csv_filenames, lfu_labels, 'LFU')