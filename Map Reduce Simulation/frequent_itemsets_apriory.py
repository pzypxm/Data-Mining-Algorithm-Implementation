from MapReduce import *
import sys
import json

"""
Find all frequent 2-itemsets with support threshold 100
"""

mr = MapReduce()

def mapper(record):
    # key: each pair
    # value: 1

    for i in range(0, len(record)):     # Get all the possible pairs according to items in baskets
        for j in range(i+1, len(record)):
            mr.emit_intermediate(str(str(i)+" "+str(j)), 1)     # Convert list to string in order to set it as key

def reducer(key, list_of_values):
    total = 0
    pair = [int(key.split()[0]), int(key.split()[1])]   # Revert list string
    #inputdata = open("transactions.json", "r+")
    inputdata = open(sys.argv[1])
    # Check every basket if current pair is frequent
    for line in inputdata:
        record = json.loads(line)
        flag_i = 0
        flag_j = 0
        for num in range(0, len(record)):   # Flag checks if every element in the pair is in a single basket
            if pair[0] == record[num]:
                flag_i = 1
            if pair[1] == record[num]:
                flag_j = 1
        if flag_i == 1 and flag_j == 1:
            total += 1

    if total >= 100:    # Output if frequent
        mr.emit(pair)

if __name__ == '__main__':
    #inputdata = open("transactions.json", "r+")     # Useful for IDE debugging
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)
