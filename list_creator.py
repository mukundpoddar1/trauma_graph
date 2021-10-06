# %%
import pandas as pd
import csv
import json

# %%
data_loc = 'RDS_ICD10_DCODE.csv'
df = pd.read_csv(data_loc)
# keep the first 5 digits of the DCODE
df['ICD10_DCODE'] = df['ICD10_DCODE'].astype(str).apply(lambda x: x[:5])


# %%
df['INC_KEY'] = df['INC_KEY'].astype(str)
diagnoses = df.groupby('INC_KEY')['ICD10_DCODE'].apply(list).reset_index(name='dcodes')
diagnoses = diagnoses.dcodes

# %%
diagnoses.sample(5)
# %%
def write_to_file(adj_list, fname='adj_list.csv'):
    with open(fname, 'w') as file:
        json.dump(adj_list, file)

def convert_to_dict(diagnoses):
    adj_list = {}
    def add_diagnoses_to_list(row):
        source = row[0]
        for dest in row[1:]:
            if source in adj_list:
                if dest in adj_list[source]:
                    adj_list[source][dest]["weight"] = adj_list[source][dest]["weight"]+1
                else:
                    adj_list[source]={dest:{"weight": 1}}
            elif dest in adj_list:
                if source in adj_list[dest]:
                    adj_list[dest][source]["weight"] = adj_list[dest][source]["weight"]+1
                else:
                    adj_list[dest]={source:{"weight": 1}}
            else:
                adj_list[source]={dest:{"weight": 1}}
    diagnoses.map(add_diagnoses_to_list)
    return adj_list

adj_list = convert_to_dict(diagnoses.sample(500))
write_to_file(adj_list)

#%%
