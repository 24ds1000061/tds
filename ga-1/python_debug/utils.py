"""
Utility functions for data processing
"""

def load_data():
    """Load the server requests data"""
    return [148,292,49,140,108,284,284,65,127,181,33,170,4,149,40,241,96,134,286,249]

def process_above_threshold(items, threshold):
    """
    Process items that are above the given threshold.

    Args:
        items: List of numeric values
        threshold: Minimum value to include

    Returns:
        Dictionary with count, total, and average
    """
    count = 0
    total = 0

    for item in items:
        if item > threshold:
            count += 1
            total += item

    average = round(total / count, 2) if count > 0 else 0.0

    return {
        'count': count,
        'total': total,
        'average': f"{average:.2f}"
    }
