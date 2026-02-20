"""
Server Log Analysis

Process server logs to calculate response time statistics

This script processes server requests and calculates statistics
for values above a certain threshold.

Use GitHub Copilot or another AI coding agent to help debug this code!
"""

import utils

def main():
    # Load data
    data = utils.load_data()
    threshold = 119

    print(f"Analyzing {len(data)} server requests...")
    print(f"Threshold: {threshold}")
    print()

    # Process data using utility function
    result = utils.process_above_threshold(data, threshold)

    # Display results
    print(f"Items above threshold: {result['count']}")
    print(f"Total value: {result['total']}")
    print(f"Average value: {result['average']}")
    print()

    # Generate output hash for verification
    output = f"{result['count']},{result['total']},{result['average']}"
    print(f"OUTPUT: {output}")

if __name__ == "__main__":
    main()
