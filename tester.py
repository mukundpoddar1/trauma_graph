#%%
import pandas as pd
from node_finder import connected_nodes, get_community
from numpy.random import choice
import networkx as nx
import json
from sklearn.metrics import jaccard_score
from utilities import load_descriptions

# %%
test_file = 'test.csv'
test_visits = pd.read_csv(test_file)
# convert dcodes str representation back to list
test_visits['dcodes'] = test_visits.dcodes.apply(lambda x: x[1:-1].replace('\'', '').split(','))

def divide_input(dcodes):
    dcodes['input'] = dcodes.dcodes.map(lambda codes: choice(codes, size=1, replace=False)[0])
    dcodes['output'] = dcodes.apply(lambda codes: list(set(codes['dcodes'])-set(codes['input'])), axis=1)
    return dcodes

test_visits = divide_input(test_visits)

with open('adj_list.csv') as json_file:
    adj_list = json.load(json_file)
net = nx.Graph(adj_list)

#%%
def get_pred_list(input):
    input = input.strip(' \'')
    return get_community(net, input)#, 2, 0, 0.0000001)

test_visits['predictions'] = test_visits.input.apply(get_pred_list)

# %%
def evaluate(results):
    def get_diff(true, pred):
        intersection = [x for x in true if x in pred]
        return len(intersection)/(len(true)+len(pred)-len(intersection))
    return results.apply(lambda row: get_diff(row['output'], row['predictions']), axis=1)
# %%
results = evaluate(test_visits)
results.plot.hist(bins=15, logy=True)