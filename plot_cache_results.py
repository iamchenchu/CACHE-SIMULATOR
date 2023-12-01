import csv
import matplotlib.pyplot as plt
import numpy as np  # Added import for NaN handling

def plot_cache_results(csv_filenames, labels):
    plt.figure(figsize=(15, 8))

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
            plt.subplot(2, 3, i + 1)
            plt.plot(operations, cache_sizes, marker='o', linestyle='-', label=labels[i])
            plt.title(f'Cache Sizes Over Operations ({labels[i]})')
            plt.xlabel('Operation')
            plt.ylabel('Cache Size')
            plt.legend()
            plt.grid(True)

            # Plot Results
            plt.subplot(2, 3, i + 4)
            results = [np.nan if result is None else result for result in results]
            plt.plot(operations, results, marker='o', linestyle='-', label=labels[i])
            plt.title(f'Results Over Operations ({labels[i]})')
            plt.xlabel('Operation')
            plt.ylabel('Result')
            plt.legend()
            plt.grid(True)

    plt.tight_layout()
    plt.show()

# Example usage:
csv_filenames = ['LRU_parallel_results.csv', 'LFU_parallel_results.csv', 'FIFO_parallel_results.csv']
labels = ['P_LRU', 'P_LFU', 'P_FIFO']
plot_cache_results(csv_filenames, labels)

csv_filenames = ['LRU_sequential_results.csv', 'LFU_sequential_results.csv', 'FIFO_sequential_results.csv']
labels = ['S_LRU', 'S_LFU', 'S_FIFO']
plot_cache_results(csv_filenames, labels)
