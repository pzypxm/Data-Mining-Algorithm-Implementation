from MapReduce import *
import sys
import re

"""
Count word frequency and document frequency
"""

mr = MapReduce()

def mapper(record):
    # key: words
    # value: [book names, 1]

    book_name = record[0]
    words = record[1].split()   # Split a value in list by space and construct a new list
    for w in words:
        if re.findall("\w*", w.lower())[0] != "":   # Obliterate punctuations
            mr.emit_intermediate(w.lower(), [book_name, 1])

def reducer(word, dict_value):
    df_tmp = {}
    df = []
    # Construct document frequency dictionary(key: document name; value: a count list that have many "1"
    for v in range(0, len(dict_value)):
        df_tmp.setdefault(dict_value[v][0], [])
        df_tmp[dict_value[v][0]].append(dict_value[v][1])
    for book_name in df_tmp:
        total = 0
        for value in df_tmp[book_name]:   # Calculate document frequency according to the count list
            total += 1
        df.append([book_name, total])
    mr.emit([word, len(df), df])


if __name__ == '__main__':
    #inputdata = open("books.json", "r+")    # Useful for IDE debugging
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)
