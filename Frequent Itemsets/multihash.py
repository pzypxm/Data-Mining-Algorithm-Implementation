from sys import argv
from itertools import combinations

# For IDE debugging
# input_fd = open("/Users/patrickpeng/Workspace_Python/Assignment_2/input.txt")
# support = 4
# bucket = 5

input_fd = open(argv[1])
support = int(argv[2])
bucket = int(argv[3])


# Hash function 1
def hash_1(items):
    total = 0
    count = 0
    for i in items:
        count += 1
        total += ord(i) * count
    return total % bucket


# Hash function 2
def hash_2(items):
    total = 0
    count = 0
    for i in items:
        count += 1
        total += ord(i) ^ 2 * 3 * count
    return total % bucket

# Read baskets in
baskets = []
for line in input_fd:
    baskets.append(line.split("\n")[0])

# Get 1-size item count number
single_CNT = {}
for item in baskets:
    item = item.split(",")
    for key in item:
        single_CNT.setdefault(key, [])
        single_CNT[key].append(1)
for key in single_CNT:
    single_CNT[key] = len(single_CNT[key])

# Get size-1 items
all_single = sorted(single_CNT)

# Output size-1 frequent items
fre_single = []
for key in single_CNT:
    if single_CNT[key] >= support:
        fre_single.append(key)
fre_single = sorted(fre_single)
print fre_single
print " "

# Output hash table and n-size items (n >= 2)
can_itemsets = {}
fre_itemsets = [0]  # Initial frequent itemsets list
size = 2    # Record size of sets in current loop
hash_tab_1 = {}
hash_tab_2 = {}
while len(fre_itemsets) != 0:

    can_itemsets = {}
    fre_itemsets = []

    # Initialize hash table
    for i in range(0, bucket):
        hash_tab_1.setdefault(i, 0)
        hash_tab_2.setdefault(i, 0)

    flag_fre = 0
    # Generate every subset and count its times of appearance in baskets and construct hash table
    for subset in combinations(all_single, size):
        count = 0
        for bsk in baskets:
            flag = 0
            for item in bsk:
                for i in range(0, size):
                    if item == subset[i]:
                        flag += 1
            if flag == size:
                count += 1
        hash_tab_1[hash_1(subset) % bucket] += count
        hash_tab_2[hash_2(subset) % bucket] += count
        if count >= support:
            flag_fre = 1

    if flag_fre == 1:   # Output hash table if there is at least one frequent bucket
        print hash_tab_1
        print hash_tab_2

    # Construct bit map
    for key in hash_tab_1:
        if hash_tab_1[key] >= support:
            hash_tab_1[key] = 1
        else:
            hash_tab_1[key] = 0

    for key in hash_tab_2:
        if hash_tab_2[key] >= support:
            hash_tab_2[key] = 1
        else:
            hash_tab_2[key] = 0

    # Get candidate itemsets
    for subset in combinations(fre_single, size):
        if hash_tab_1[hash_1(subset)] == 1 and hash_tab_2[hash_2(subset) == 1]:     # Check bit map
            can_itemsets.setdefault(subset, 0)
            for bsk in baskets:
                flag = 0
                for item in bsk:
                    for i in range(0, size):
                        if item == subset[i]:
                            flag += 1
                if flag == size:
                    can_itemsets[subset] += 1

    # Get truly frequent itemsets
    for items in can_itemsets:
        if can_itemsets[items] >= support:
            tmp = []
            for char in items:
                tmp.append(char)
            fre_itemsets.append(tmp)

    if len(fre_itemsets) != 0:
        print sorted(fre_itemsets)
        print " "

    size += 1



















