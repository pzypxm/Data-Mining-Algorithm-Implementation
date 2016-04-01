from heapq import *
from sys import argv
from itertools import combinations
from math import sqrt


def get_dataset(fd):

    # Read in dataset
    tuples_list = []
    for line in fd:
        tuples_list.append(line.split("\n")[0].split(","))

    # Transfer value format
    for tup in tuples_list:
        for i in range(0, len(tup)-1):
            tup[i] = float(tup[i])

    # Assign new label name and tuple sequence number for classes, all are in String format
    num_label = {}
    for tup in tuples_list:
        num_label.setdefault(str(tup[len(tup)-1]), 1)
    seq = 1
    for label in num_label:
        num_label[label] = seq
        seq += 1
    num = 0
    for tup in tuples_list:
        tup[len(tup)-1] = str(num_label[tup[len(tup)-1]])
        tup.append(str(num))
        num += 1

    # Store list to dictionary
    tuples = {}
    for tup in tuples_list:
        tuples.setdefault(tup[len(tup)-1], tup[0:len(tup)-1])

    return tuples


def get_distance(name_list, clusters):

    # Calculate centroid for left side and right side
    left = name_list[0]
    right = name_list[1]

    first_time = True
    for name in left:
        if first_time:
            centroid_left = []
            for i in clusters[str(name)]:
                centroid_left.append(i)
            first_time = False
        else:
            for i in range(0, len(centroid_left)):
                centroid_left[i] = float(centroid_left[i]) + float(clusters[str(name)][i])
    for i in range(0, len(centroid_left)):
        centroid_left[i] = float(centroid_left[i]) / float(len(left))

    first_time = True
    for name in right:
        if first_time:
            centroid_right = []
            for i in clusters[str(name)]:
                centroid_right.append(i)
            first_time = False
        else:
            for i in range(0, len(centroid_right)):
                centroid_right[i] = float(centroid_right[i]) + float(clusters[str(name)][i])
    for i in range(0, len(centroid_right)):
        centroid_right[i] = float(centroid_right[i]) / float(len(right))

    # Construct merge record
    sum = 0
    for index in range(0, len(centroid_left)):
        sum += (float(centroid_left[index]) - float(centroid_right[index]))**2

    return [sqrt(sum), [left, right]]



def get_result(cluster, clusters):

    """
    Whole Process:
    1. Get combination of current clusters
    2. Calculate their distance and add them to heap
    3. Pop heap root
    4. Check if belonging to old cluster
    4. Record this new merge
    5. Update clusters set
    """
    for name in clusters:
        clusters[name].pop()  # Remove class label of each tuple

    heap = []   # Store the heap
    merge_record = []  # Record every clustering operation
    cluster_name = []   # Store current cluster
    times = 1

    # Get name of each cluster
    for tup in clusters:
        cluster_name.append([int(tup)])

    while times < len(clusters):

        # Calculate their distance and add them to heap
        if times == 1:
            for pair in combinations(cluster_name, 2):
                temp = [pair[0], pair[1]]
                heappush(heap, get_distance(temp, clusters))
        else:
            for i in range(0, len(cluster_name)-1):
                temp = [cluster_name[i], cluster_name[len(cluster_name)-1]]
                heappush(heap, get_distance(temp, clusters))

        # Check is root is for old cluster
        if times > 1:
            old = True
            while old:
                old = False
                for name in heap[0][1]:
                    if merge_record.count(name) != 0:
                        old = True
                if old:
                    heappop(heap)

        # Record this new merge
        temp = heappop(heap)[1]
        for name in temp:
            merge_record.append(name)

        # Update cluster name list
        length = len(merge_record)
        for i in range(length-2, length):   # Delete merged name
            cluster_name.remove(merge_record[i])
        cluster_name.append(merge_record[length-2]+merge_record[length-1])     # Add new merged name

        if times == len(clusters)-cluster:
            return cluster_name

        times += 1


def evaluation(clusters, cluster_name):
    # Get pairs for gold standard
    gold_std = {}
    for name in clusters:
        key = clusters[name].pop()
        gold_std.setdefault(key, [])
        gold_std[key].append(int(name))
    gold_pair = []
    for key in gold_std:
        for i in combinations(gold_std[key], 2):
            gold_pair.append(sorted(i))

    # Get pairs for gotten result
    result_pair = []
    for i in cluster_name:
        for j in combinations(i, 2):
            result_pair.append(sorted(j))

    # Calculate matched amount
    match = 0
    for i in gold_pair:
        for j in result_pair:
            if i == j:
                match += 1

    precision = float(match)/float(len(result_pair))
    recall = float(match)/float(len(gold_pair))

    return [precision, recall]

if __name__ == '__main__':

    # For IDE debugging
    fd = open("/Users/patrickpeng/Workspace_Python/Assignment_4/iris.dat")
    cluster = 3

    #fd = open(argv[1])
    #cluster = int(argv[2])

    clusters = get_dataset(fd)

    cluster_name = get_result(cluster, clusters)

    fd.seek(0)
    clusters = get_dataset(fd)
    for i in evaluation(clusters, cluster_name):
        print i

    for i in cluster_name:
        print sorted(i)


