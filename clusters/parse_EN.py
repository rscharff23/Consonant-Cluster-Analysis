import pandas as pd
from parse_PL import remove_chars,remove_vowels, process_sentence, lng
from convert_ipa.pl_to_ipa_dev import combine_digraphs
import csv

ipa_consts = ['b','d','f','g','h','j','k','l','m','n','ŋ','p','r','s','ʃ','t','v','w','z','θ','ð','t͡s','d͡z','t͡ʃ','d͡ʒ','ʒ']

df = pd.read_csv('clusters/data_en/sentences_en.csv')

clusters = {}#dict to hold clusters
with open('clusters/data_en/ipa_sentences_en.txt','w', encoding="utf-8-sig") as ipa:
    for s in df['phonemes']:
        s = s.replace('ts','t͡s').replace('dz','d͡z').replace('tʃ','t͡ʃ').replace('dʒ','d͡ʒ')
        chars = list(s)
        combine_digraphs(chars, []) #turn ipa sentences into list of ipa chars
        remove_chars(chars, [' ','ˈ']) #remove spaces and emphasis markers to create clusters

        ipa.write(''.join(chars) + '\n')#make file of ipa sentences - maybe figure out spaces later
        
        remove_vowels(chars, ipa_consts) #isolate clusters by removing everything left
        process_sentence(chars,clusters) #update dict with clusters and prevalence

data = {#reformat to dataframe
    'cluster': clusters.keys(),
    'occurences_en': clusters.values(),
    'length': lng(clusters.keys()) #get length of each cluster
}
df = pd.DataFrame(data)

#write to csv
df.to_csv('clusters/clusters_en.csv',index=False)