import csv
import matplotlib.pyplot as plt
import numpy as np  # Added import for NaN handling

def plot_cache_results(csv_filename):
    with open(csv_filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header

        operations = []
        cache_sizes = []
        results = []

        for row in reader:
            operations.append(row[0])
            cache_sizes.append(int(row[1]))
            result_value = row[2] if row[2] != 'N/A' else None  # Replace 'N/A' with None
            results.append(result_value)

    # Plot Cache Sizes
    plt.figure(figsize=(10, 5))
    plt.subplot(2, 1, 1)
    plt.plot(operations, cache_sizes, marker='o', linestyle='-', color='b')
    plt.title('Cache Sizes Over Operations')
    plt.xlabel('Operation')
    plt.ylabel('Cache Size')
    plt.grid(True)

    # Plot Results (handle NaN)
    plt.subplot(2, 1, 2)
    results = [np.nan if result is None else result for result in results]
    plt.plot(operations, results, marker='o', linestyle='-', color='r')
    plt.title('Results Over Operations')
    plt.xlabel('Operation')
    plt.ylabel('Result')
    plt.grid(True)

    plt.tight_layout()
    plt.show()

# Example usage:
plot_cache_results('lru_results.csv')
