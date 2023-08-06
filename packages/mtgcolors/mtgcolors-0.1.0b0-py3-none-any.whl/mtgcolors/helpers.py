def isContained(list1, list2):
    small, large = (list1, list2) if len(list1) < len(list2) else (list2, list1)
    return set(small) <= set(large)
