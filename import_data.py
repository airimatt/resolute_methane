import numpy as np

def import_values(filename):
    """
    Purpose: Imports values from a file and returns them as a numpy array
    Arguments: Filename to read from
    """
    try:
        with open(filename, 'r') as f:
            line = f.readline().strip()  # Read the line and remove leading/trailing whitespace
            values_str = line.split() # Split the string by spaces
            values = [float(x) if '.' in x else int(x) for x in values_str] # Convert to int or float
            return np.array(values)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    except ValueError:
        print(f"Error: Could not convert values in '{filename}' to numbers.")
        return None