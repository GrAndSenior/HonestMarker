import pandas as pd
import lxml

def make_K(row):
    print(row[0])    
    return row.iloc[0]


k_count, p_count = 20, 4
Codes = pd.read_csv('d:/DM/100ok.csv', sep='\t', encoding='utf-8', names=['gs1dm'])
KCodes = pd.read_csv('d:/DM/k.csv', sep='\t', encoding='utf-8', names=['K'])
PCodes = pd.read_csv('d:/DM/p.csv', sep='\t', encoding='utf-8', names=['P'])


KCodes['idx'] = KCodes.index
PCodes['idx'] = PCodes.index

Codes['idx'] = Codes.index // k_count
Codes = Codes.merge(KCodes, how='left', on='idx', suffixes=('', '1'))
Codes['K'] = Codes['K'].fillna('-')
Codes['idx'] = Codes.index // p_count
Codes = Codes.merge(PCodes, how='left', on='idx', suffixes=('', '1'))
Codes['P'] = Codes['P'].fillna('-')

#Codes.to_xml('d:/DM/test.xml', encoding='utf-8', root_name='unit_pack')

#Codes = Codes.groupby(['P','K','gs1dm']).count()
#Codes.reset_index()

#Codes = Codes.drop(['idx'], axis=True)
P = Codes['P'].value_counts().index.tolist()
K = Codes['K'].value_counts().index.tolist()
print(Codes)
for i in P:
    print(i)
    for j in K:
        print('   ',j)
        C = Codes[Codes['K']==j]['gs1dm'].tolist()
        print('        ', C)



#print(Codes)
print(P)




