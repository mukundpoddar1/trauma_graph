import pandas as pd

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