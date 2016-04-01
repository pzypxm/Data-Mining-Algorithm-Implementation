from sys import argv
from itertools import combinations
from random import sample

# For IDE debugging
# input_fd = open("/Users/patrickpeng/Workspace_Python/Assignment_2/input1.txt")
# support = 20

input_fd = open(argv[1])
support = int(argv[2])

fraction = 0.4
iterate = 1     # Iteration count
if_neg = 1  # False negative indicator

while if_neg != 0:

    if_neg = 0
    p1_fre_itemsets = []
    neg_border = []

    # Read 60% baskets in
    line_count = 0
    input_fd.seek(0)
    for line in input_fd:   # Count the number of lines in file
        line_count += 1

    random_line = []    # Get a randomly sampled line number
    for i in range(0, line_count):
        random_line.append(i)
    random_line = sorted(sample(random_line, int(line_count*fraction)))

    sample_baskets = []    # Get sampled baskets
    count_line = 0
    count_random = 0
    input_fd.seek(0)    # Renew FD by redirecting pointer to first line
    for line in input_fd:
        if count_random == len(random_line):
            break
        if count_line == random_line[count_random]:     # Fetch lines according to random number list
            sample_baskets.append(line.split("\n")[0])
            count_random += 1
        count_line += 1
    for i in range(0, len(sample_baskets)):
        sample_baskets[i] = sample_baskets[i].split(",")

    # Get size-1 frequent items
    single_CNT = {}
    for item in sample_baskets:
        for key in item:
            single_CNT.setdefault(key, 0)
            single_CNT[key] += 1

    fre_single = []
    for key in single_CNT:
        if single_CNT[key] >= support*fraction*0.9:
            fre_single.append(key)
            p1_fre_itemsets.append([key])
        else:
            neg_border.append([key])

    fre_single = sorted(fre_single)

    # Output n-size items (n >= 2)
    can_itemsets = {}
    fre_itemsets = [0]  # Initial frequent itemsets list
    size = 2    # Record size of sets in current loop

    while len(fre_itemsets) != 0:

        can_itemsets = {}
        fre_itemsets = []

        # Generate every subset and count its times of appearance in baskets
        for subset in combinations(fre_single, size):
            count = 0
            for bsk in sample_baskets:
                flag = 0
                for item in bsk:
                    for i in range(0, size):
                        if item == subset[i]:
                            flag += 1
                if flag == size:
                    count += 1
            can_itemsets[subset] = count

        # Get frequent size-n itemsets
        for items in can_itemsets:
            tmp = []
            for char in items:
                tmp.append(char)

            if can_itemsets[items] >= support*fraction*0.9:
                fre_itemsets.append(tmp)
                p1_fre_itemsets.append(tmp)
            elif size == 2:     # Get size-2 negative border
                flag = 0
                for i in tmp:
                    for sin in fre_single:
                        if i == sin:
                            flag +=1
                if flag == len(tmp):
                    neg_border.append(tmp)


        # Construct negative border
        for subset_1 in combinations(fre_single, size+1):
            tmp_1 = []
            for char in subset_1:
                tmp_1.append(char)

            count = 0
            for bsk in sample_baskets:      # Check if candidate negative border is frequent in sample itemsets
                flag = 0
                for item in bsk:
                    for i in range(0, len(tmp_1)):
                        if item == tmp_1[i]:
                            flag += 1
                if flag == len(tmp_1):
                    count += 1

            if count >= support*fraction*0.9:
                continue

            equal_CNT = 0   # Check if candidate negative border's immediate subsets are all frequent
            count = 0
            for subset_2 in combinations(tmp_1, size):
                tmp_2 = []
                for i in subset_2:
                    tmp_2.append(i)

                for items in fre_itemsets:
                    if items == tmp_2:
                        equal_CNT += 1
                        break
                count += 1
            if count == equal_CNT:
                neg_border.append(tmp_1)

        size += 1

    # Read all baskets (Pass 2 begin)
    input_fd.seek(0)
    basket = []
    temp = []
    for line in input_fd:
        basket.append(line.split("\n")[0])
    for bsk in basket:
        bsk = bsk.split(",")
        temp.append(bsk)
    basket = temp

    # Check if candidate negative border is frequent in sample itemsets
    for neg in neg_border:
        count = 0
        for bsk in basket:
            flag = 0
            for item in bsk:
                for i in range(0, len(neg)):
                    if item == neg[i]:
                        flag += 1
            if flag == len(neg):
                count += 1
        if count >= support:
            if_neg = 1
            iterate += 1
            break

    # If there is not any false negative, check and output truly frequent itemsets
    result = []
    if if_neg == 0:
        for item in p1_fre_itemsets:
            count = 0
            for bsk in basket:
                flag = 0
                for items in bsk:
                    for i in range(0, len(item)):
                        if items == item[i]:
                            flag += 1
                if flag == len(item):
                    count += 1
            if count >= support:
                result.append(item)

        # Output results
        print iterate
        print fraction

        result = sorted(result)
        maxlen = 0
        for i in range(0, len(result)):
            if len(result[i]) > maxlen:
                maxlen = len(result[i])
        for i in range(1, maxlen+1):
            tmp = []
            for item in result:
                if len(item) == i:
                    tmp.append(item)
            print tmp
            print " "
