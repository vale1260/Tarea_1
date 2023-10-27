import matplotlib.pyplot as plt

def read_data_from_file(filename):
    data = []
    with open(filename, 'r') as f:
        for line in f:
            try:
                value = float(line.strip())
                data.append(value)
            except ValueError:
                # Skip lines that cannot be be converted to float
                continue
    return data

def plot_latency_and_throughput(latency_file, throughput_file, output_file):
    latency_data = read_data_from_file(latency_file)
    throughput_data = read_data_from_file(throughput_file)

    # Plot latency
    plt.figure(figsize=(10, 6))
    plt.subplot(2, 1, 1)
    plt.plot(latency_data, label='Latency')
    plt.title('Consumer Latency')
    plt.xlabel('Sample')
    plt.ylabel('Latency (ms)')
    plt.legend()

    # Plot throughput
    plt.subplot(2, 1, 2)
    plt.plot(throughput_data, label='Throughput')
    plt.title('Consumer Throughput')
    plt.xlabel('Sample')
    plt.ylabel('Throughput (messages/second)')
    plt.legend()

    plt.tight_layout()
    
    # Save the plot to a PNG file
    plt.savefig(output_file, format='png')

if __name__ == "__main__":
    consumer_latency_file = 'consumer_latency.txt'
    consumer_throughput_file = 'consumer_throughput.txt'
    output_file = 'consumer_plot.png'
    plot_latency_and_throughput(consumer_latency_file, consumer_throughput_file, output_file)

