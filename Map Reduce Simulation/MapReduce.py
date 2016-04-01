import json

class MapReduce:
    def __init__(self):
        # initialize dictionary for intermediate values from Map task
        self.intermediate = {}
        # initialize list for results of Reduce task
        self.result = []

    def emit_intermediate(self, key, value):
        # "setdefault": If key is in the dictionary, do nothing. Otherwise insert key with an empty list
        self.intermediate.setdefault(key, [])
        # append value to list associated with key
        self.intermediate[key].append(value)

    def emit(self, value):
        # append value to list of results
        self.result.append(value) 

    def execute(self, data, mapper, reducer):
        # read each line from input file, then call Map function on each record
        for line in data:
            record = json.loads(line)
            mapper(record)
        
        # for each key-value list in intermediate dictionary, call Reduce task
        for key in self.intermediate:   # Loop in the dictionary by keys
            reducer(key, self.intermediate[key])

        jenc = json.JSONEncoder()   # Create an JSON Encoder instance
        # print each result in result list
        for item in self.result:
            print jenc.encode(item)





