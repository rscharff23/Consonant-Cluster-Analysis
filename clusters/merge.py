import pandas as pd

pd.set_option('display.float_format', '{:.10f}'.format)
n_pl = 15707 #n sentences in pl training data
n_en = 14150 #n sentences in en data ### CHANGE THESE IF SWITCHING DATASETS

df1 = pd.read_csv('clusters/clusters_pl.csv')
df2 = pd.read_csv('clusters/clusters_en.csv')

#merge datasets
new = pd.merge(df1,df2,on=['cluster','length'], how='outer').fillna(0)
new['occurences_pl'] = new['occurences_pl'].astype(int)
new['occurences_en'] = new['occurences_en'].astype(int) #change floats to ints
new['length'] = new['length'].astype(int)

#calculated fields
new['frequency_pl'] = new['occurences_pl'] / n_pl 
new['frequency_en'] = new['occurences_en'] / n_en
new['total_frequency'] = new['frequency_pl'] + new['frequency_en']
new['relative_frequency'] = new['frequency_pl'] / (new['frequency_pl'] + new['frequency_en'])

new = new.reindex(columns = ['cluster','length','occurences_pl','occurences_en',#reorder
                             'frequency_pl','frequency_en','total_frequency','relative_frequency'])

new.to_csv('merged_clusters.csv',float_format='%.6f',index=False)