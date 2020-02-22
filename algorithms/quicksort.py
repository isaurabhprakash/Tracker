# This function takes last element as pivot, places
# the pivot element at its correct position in sorted 
# array, and places all smaller (smaller than pivot) 
# to left of pivot and all greater elements to right 
# of pivot


def partition(arr, low, high):
    i = (low - 1)  # index of smaller element
    pivot = arr[high][0]  # pivot

    for j in range(low, high):

        # If current element is smaller than or 
        # equal to pivot 
        if arr[j][0] <= pivot:
            # increment index of smaller element
            i = i + 1
            arr[i][0], arr[j][0] = arr[j][0], arr[i][0]
            arr[i][1], arr[j][1] = arr[j][1], arr[i][1]

    arr[i + 1][0], arr[high][0] = arr[high][0], arr[i + 1][0]
    arr[i + 1][1], arr[high][1] = arr[high][1], arr[i + 1][1]

    return i + 1


# The main function that implements QuickSort
# arr[] --> Array to be sorted, 
# low  --> Starting index, 
# high  --> Ending index 

# Function to do Quick sort 
def quicksort(arr, low, high):
    if low < high:
        # pi is partitioning index, arr[p] is now
        # at right place 
        pi = partition(arr, low, high)

        # Separately sort elements before 
        # partition and after partition 
        quicksort(arr, low, pi - 1)
        quicksort(arr, pi + 1, high)

    return arr
