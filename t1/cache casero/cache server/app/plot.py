import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend for non-interactive plots
import matplotlib.pyplot as plt

# Initialize empty lists to store data
search_numbers = []
elapsed_times = []

# Read the data from the text file
with open("search_data.txt", "r") as file:
    next(file)  # Skip the header line
    for line in file:
        parts = line.strip().split(',')
        search_number = int(parts[0])
        time_elapsed = float(parts[1])
        search_numbers.append(search_number)
        elapsed_times.append(time_elapsed)

# Create a plot
plt.figure(figsize=(10, 6))
plt.plot(search_numbers, elapsed_times, label='Elapsed Time (s)')
plt.xlabel('Search Number')
plt.ylabel('Elapsed Time (s)')
plt.title('Search Time Over Time')
plt.legend()
plt.grid(True)

# Save the plot as an image file (e.g., PNG)
plt.savefig("search_plot.png")

# Close the plot to release resources
plt.close()

print("Plot saved as search_plot.png")