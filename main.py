import numpy as np

def calculate_median(x):
    """
    Computes the median of a 1D numpy array x.
    
    Parameters:
        x (numpy.ndarray): 1D array of numeric values.
    
    Returns:
        float: The median value of the array.
    """
    # Ensure input is a 1D NumPy array
    x = np.asarray(x).flatten()
    
    # Sort the array
    sorted_x = np.sort(x)
    
    # Find the number of elements
    n = len(sorted_x)
    
    # If n is odd, return the middle element
    if n % 2 == 1:
        return sorted_x[n // 2]
    # If n is even, return the average of the two middle elements
    else:
        mid1, mid2 = sorted_x[n // 2 - 1], sorted_x[n // 2]
        return (mid1 + mid2) / 2

arr = np.array([7, 1, 3, 9, 5])
print(calculate_median(arr))