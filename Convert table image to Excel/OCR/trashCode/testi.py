def group_close_numbers(lst, threshold=4):
    if not lst: return []
    lst.sort()
    groups = [[lst[0]]]
    for x in lst[1:]:
        if abs(x - groups[-1][-1]) < threshold:
            groups[-1].append(x)
        else:
            groups.append([x])
    return groups

def average_groups(groups):
    averages = []
    for group in groups:
        avg = sum(group) // len(group)
        averages.append(avg)
    return averages

numbers = [0, 1, 17, 18, 19, 21, 67, 68, 70, 71, 97, 98, 99]
print(average_groups(group_close_numbers(numbers)))