import pandas as pd

filename = 'd:\\DM\\output\\Интербир-1\\итог 1 (1).csv'
df = pd.read_csv(filename, sep='\t', encoding='utf-8', names=['gs1dm'])
def remove_lead_gs(row):
    return str(row['gs1dm'][1:])

def insert_gs(row):
    pass

df2 = df.apply(remove_lead_gs, axis=1)
df2.to_csv(filename.replace('.csv', '_.csv'), header=False, index=False)
print(df2.head(20))