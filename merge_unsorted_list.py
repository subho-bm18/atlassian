def merge_unsorted_list(list1, list2):
    merged_list = list1 + list2
    return merge_list(merged_list)

def merge_list(arr_merge):
    if len(arr_merge) <=1:
        return arr_merge
    
    mid = len (arr_merge) //2
    left = merge_list(arr_merge[mid:])
    right = merge_list(arr_merge[mid:])

    return merge(left, right)

def merge (left, right):
    merged = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    while i < len(left):
        merged.append(left[i])
        i += 1

    while j < len(right):
        merged.append(right[j])
        j += 1

    return merged


a = [5, 3, 1, 4, 2]
b = [100, 34, 56, 78, 90]
op = merge_unsorted_list(a, b)
print(op)