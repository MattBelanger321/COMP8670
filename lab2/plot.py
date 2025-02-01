import os
import pandas as pd
import matplotlib.pyplot as plt
import argparse


def plot_tcp_tahoe(csv_file):
    # Load CSV data
    df = pd.read_csv(csv_file)

    # Plot CWND over time
    plt.figure(figsize=(10, 5))
    plt.plot(df["Packet"], df["CWND"],
             label="Congestion Window (CWND)", marker='o')
    plt.plot(df["Packet"], df["SSTHRESH"],
             label="Slow Start Threshold (SSTHRESH)", linestyle='--')

    # Labels and title
    plt.xlabel("Packet Number")
    plt.ylabel("Window Size")
    plt.title("TCP Tahoe Congestion Control")
    plt.legend()
    plt.grid()

    # Save the plot with the same name as the CSV file
    file_name, _ = os.path.splitext(csv_file)
    plot_file_name = f"{file_name}.png"
    plt.savefig(plot_file_name)

    # Show plot
    plt.show()


def plot_all_csv_in_dir(directory):
    # Iterate over all CSV files in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            csv_file = os.path.join(directory, filename)
            plot_tcp_tahoe(csv_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Plot TCP Tahoe using CSV files from a directory.")
    parser.add_argument("dir_path", type=str,
                        help="The path to the directory containing the CSV files.")

    args = parser.parse_args()
    plot_all_csv_in_dir(args.dir_path)
