import pandas as pd
from node_finder import connected_nodes
from numpy.random import choice
import networkx as nx
import json
from sklearn.metrics import jaccard_score

test_file = 'test.csv'
test_visits = pd.read_csv('test.csv')
# convert dcodes str representation back to list
test_visits['dcodes'] = test_visits.dcodes.apply(lambda x: x[1:-1].replace('\'', '').split(','))

test_visits['input'] = test_visits.dcodes.map(lambda codes: choice(codes, size=1, replace=False)[0])

with open('adj_list.csv') as json_file:
    adj_list = json.load(json_file)
net = nx.Graph(adj_list)

def get_pred_list(input):
    input = input.strip(' \'')
    predictions = connected_nodes(net, input, 2, 0, 0.0000001)
    predictions.append(input)
    return predictions

test_visits['predictions'] = test_visits.input.apply(get_pred_list)
