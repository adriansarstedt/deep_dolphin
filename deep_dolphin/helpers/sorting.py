# arr[] --> Array to be sorted,
# mirror[] --> Array reordered in same order as arr[]
def quick_sort(arr, mirror=None):
    iterate_quick_sort(arr, 0, len(arr)-1, mirror)

# low  --> Starting index
# high  --> Ending index
def iterate_quick_sort(arr, low, high, mirror):
    if low < high:
        # pi is partitioning index, arr[p] is now
        # at right place
        pi = partition(arr,low,high,mirror)

        # Separately sort elements before
        # partition and after partition
        iterate_quick_sort(arr, low, pi-1, mirror)
        iterate_quick_sort(arr, pi+1, high, mirror)

# This function takes last element as pivot, places
# the pivot element at its correct position in sorted
# array, and places all smaller (smaller than pivot)
# to left of pivot and all greater elements to right
# of pivot
def partition(arr,low,high,mirror):
    i = ( low-1 )         # index of smaller element
    pivot = arr[high]     # pivot

    for j in range(low , high):

        # If current element is smaller than or
        # equal to pivot
        if   arr[j] <= pivot:

            # increment index of smaller element
            i = i+1
            arr[i],arr[j] = arr[j],arr[i]
            if (mirror != None):
                mirror[i],mirror[j] = mirror[j],mirror[i]

    arr[i+1],arr[high] = arr[high],arr[i+1]
    if (mirror != None):
        mirror[i+1],mirror[high] = mirror[high],mirror[i+1]

    return ( i+1 )
