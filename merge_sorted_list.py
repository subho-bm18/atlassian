def merge_sort_list(list1, list2):
    merged_list = []
    i,j = 0,0 
    while i< len(list1) and j< len(list2):
        if list1[i] <= list2[j]:
            merged_list.append(list1[i])
            i+=1
        else:
            merged_list.append(list2[j])
            j+=1
    while i < len(list1):
        merged_list.append(list1[i])
        i+=1
    while j < len(list2):
        merged_list.append(list2[j])
        j+=1

    return merged_list

a = [1,3,5,7,9]
b = [2,4,6,8,10]
op = merge_sort_list(a,b)
print (op)
        
