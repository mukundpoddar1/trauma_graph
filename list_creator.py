# %%
import pandas as pd
import csv

# %%
data_loc = 'RDS_ICD10_DCODE.csv'
df = pd.read_csv(data_loc)
# keep the first 5 digits of the DCODE
# print out some descriptive statistics
df['ICD10_DCODE'] = df['ICD10_DCODE'].astype(str).apply(lambda x: x[:5])


# %%
df['INC_KEY'] = df['INC_KEY'].astype(str)
adj_list = df.groupby('INC_KEY')['ICD10_DCODE'].apply(list).reset_index(name='dcodes')


# %%
adj_list.sample(5)
# %%
def write_to_file(inc_dcode, fname='adj_list.csv'):
    to_ignore = ['[',']','"', '\'']
    inc_dcode.dcodes = inc_dcode.dcodes.astype(str)
    for char in to_ignore:
        inc_dcode.dcodes = inc_dcode.dcodes.apply(lambda x: x.replace(char, ''))
    inc_dcode.dcodes.to_csv(fname, quoting=csv.QUOTE_NONNUMERIC, header=False, index=False)

write_to_file(adj_list)
