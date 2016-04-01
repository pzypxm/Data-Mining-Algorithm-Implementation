from MapReduce import *
import sys

"""
Compute square of matrix (One phase version)
"""

mr = MapReduce()

def mapper(record):
    # key: the position info in matrix C
    # value: the sposition and value info

    nums = record
    nums[0] += 1
    nums[1] += 1
    v = nums[2]
    # For elements in A, create key-value pair
    i = nums[0]
    j = nums[1]
    for L in range(1, 6):
        mr.emit_intermediate(str(str(i)+" "+str(L)), ["A", i, j, v])
    # For elements in B, create key-value pair
    j = nums[0]
    k = nums[1]
    for N in range(1, 6):
        mr.emit_intermediate(str(str(N)+" "+str(k)), ["B", j, k, v])

def reducer(key, list_of_values):
    total = 0
    # Rearrange pairs from A,B to different list
    A = []
    B = []
    for i in list_of_values:
        if i[0] == "A":
            A.append(i)
        if i[0] == "B":
            B.append(i)
    # Calculate value in C
    for a in A:
        for b in B:
            if a[2] == b[1]:
                total += a[3] * b[3]
    mr.emit([int(key.split()[0])-1, int(key.split()[1])-1, total])

if __name__ == '__main__':
    #inputdata = open("matrix.json", "r+")   # Useful for IDE debugging
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)
