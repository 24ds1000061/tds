import json
import os

def compress_json(input_file, output_file):
    # Read input data
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    if not data:
        print("Empty data.")
        return

    # Extract columns from the first object
    columns = list(data[0].keys())

    # Convert each object to array of values
    rows = [[obj[col] for col in columns] for obj in data]

    result = {'columns': columns, 'rows': rows}

    # Save refactored data
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)
    
    # Print statistics
    orig_size = os.path.getsize(input_file)
    new_size = os.path.getsize(output_file)
    reduction = (1 - new_size / orig_size) * 100
    
    print(f"Original size: {orig_size} bytes")
    print(f"Refactored size: {new_size} bytes")
    print(f"Reduction: {reduction:.2f}%")

if __name__ == "__main__":
    compress_json('data.json', 'refactored.json')
