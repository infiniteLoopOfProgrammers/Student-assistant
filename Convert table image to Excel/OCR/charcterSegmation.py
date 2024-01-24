import cv2
import numpy as np

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


def char(name,image,min_w):
    column_sums = np.sum(image, axis=0)
    # column_sumsx = np.sum(image, axis=1)
    # mean_column_max = np.max(column_sumsx)
    # selected_y_coordinates = np.where(column_sumsx >= mean_column_max)[0]
    # Calculate the mean of the column sums
    mean_column_sum = np.mean(column_sums)
    mean_column_min = np.min(column_sums)
    selected_x_coordinates = np.where(column_sums < mean_column_sum)[0]

    grouped = group_close_numbers(selected_x_coordinates.tolist())
    # grouped.insert(0,[0])
    # grouped.append([image.shape[1]])
    # yy = selected_y_coordinates[0]
    # hh = (selected_y_coordinates[-1]+5)-yy
    # place = image[yy:yy+hh,:]
    # cv2.imwrite(f'all_letters_in_img4/0.png', place) # @@@@@
    # column_sums_place = np.sum(place, axis=0)
    # mean_column_sum_place = np.mean(column_sums_place)
    # selected_x_coordinates_place  = np.where(column_sums_place < 0.8*mean_column_sum_place)[0]
    print("group_close_numbers:", grouped)
    selected_x_coordinates2 = average_groups(grouped)
    selected_x_coordinates3 = selected_x_coordinates2.copy()
    for i,item in enumerate(selected_x_coordinates3):
        if item < min_w or item > image.shape[1] - min_w or len(grouped[i]) < 5:
            selected_x_coordinates2.remove(item)
    print("X-coordinates less than half the mean:", selected_x_coordinates2)
    # list11 = []
    # for x in selected_x_coordinates2:
    #     list11.append(column_sums[x])
    
    # deleted = []   
    # for item in selected_x_coordinates2:
    #     # group = grouped[selected_x_coordinates3.index(item)]
    #     # group.remove(group[0])
    #     # # group.remove(group[1])
    #     # # group.remove(group[-2])
    #     # group.remove(group[-1])
    #     column_sums_group = [int(column_sums[(item-2)+i]) for i in range(3)]
    #     # column_sums_group = [int(column_sums[x]) for x in group]
    #     avarege = sum(column_sums_group) / len(column_sums_group)
    #     variance = sum((x - avarege) ** 2 for x in column_sums_group) / len(column_sums_group)
    #     if(variance > 15000):
    #         deleted.append(item)
    #     # if abs(int(column_sums[item]) - int(avarege)) > abs(int(column_sums[item]) - int(column_sums[item-1]))*10:
    #     #     deleted.append(item)
            
    # for item in deleted:
    #     selected_x_coordinates2.remove(item)
            
    img_with_lines = image.copy()
    for x in selected_x_coordinates2:
        cv2.line(img_with_lines, (x , 0),
                    (x,img_with_lines.shape[0]), (255, 0, 0), 1)
    cv2.imwrite(f'all_letters_in_img4/{name}.png', img_with_lines) # @@@@@
    pass
