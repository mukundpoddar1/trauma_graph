import json
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import json
import networkx as nx
import matplotlib.pyplot as plt
from node_finder import connected_nodes

app = dash.Dash('Trauma Dashboard')

def load_nodes():
    with open('adj_list.csv') as json_file:
        adj_list = json.load(json_file)
    nodes = []
    for k, v in adj_list.items():
        nodes.append(k)
        for vk, _ in v.items():
            nodes.append(vk)
    return nodes

def load_descriptions(nodes):
    descriptions = pd.read_csv('data/RDS_ICD10_DCODEDES.csv', encoding_errors='replace')
    descriptions['short_code'] = descriptions[descriptions['ICD10_DCODE'].apply(lambda code: type(code)==str and code!='-1' and code!='-2')]['ICD10_DCODE'].apply(lambda code: code[:5])
    def get_description(node):
        try:
            return descriptions[descriptions['short_code']==node]['ICD10_DCODEDES'].iloc[0]
        except IndexError:
            return 'Unknown'
    icd_desc = {node: get_description(node) for node in nodes}
    desc_icd = {v: k for k,v in icd_desc.items()}
    return icd_desc, desc_icd

injury_codes = load_nodes()
icd_desc, desc_icd = load_descriptions(injury_codes)

with open('adj_list.csv') as json_file:
    adj_list = json.load(json_file)
net = nx.Graph(adj_list)

app.layout = dbc.Container(
    fluid=True,
    children=[
        dbc.Row(html.H1('Trauma Dashboard'), align="center"),
        dbc.Form(
        [
            dbc.Label('Choose injuries:'),
            dcc.Dropdown( id='injuries',
                options=[{'label': desc, 'value': code} for code, desc in icd_desc.items()],
                multi=True)
            ]),
            dbc.Row(html.H3('Associated Injuries'), align="center"),
            dcc.Checklist(id='predicted', labelStyle = dict(display='block'))
        ]
    )

@app.callback(
    Output('predicted', 'options'), Input('injuries', 'value')
)
def get_predictions(input_injuries):
    results = connected_nodes(net, input_injuries[0], 2, 0, 0.0000001)
    return [{'label': icd_desc[node], 'value': node} for node in results]

if __name__ == '__main__':
    app.run_server(debug=True)
