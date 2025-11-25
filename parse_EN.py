import pandas as pd
from parse_PL import remove_chars,remove_vowels, process_sentence
from convert_ipa.pl_to_ipa import combine_digraphs
import csv

ipa_consts = ['b','d','f','g','h','j','k','l','m','n','ŋ','p','r','s','ʃ','t','v','w','z','θ','ð','ts','dz','dʒ','tʃ','ʒ']
di_ipa = ['ts','dz','dʒ','tʃ'] #ipa sounds represented by two characters

df = pd.read_csv('data_en/sentences_en.csv')

clusters = {}#dict to hold clusters
with open('data_en/ipa_sentences_en.txt','w', encoding="utf-8-sig") as ipa:
    for s in df['phonemes']:
        chars = list(s)
        combine_digraphs(chars, di_ipa) #turn ipa sentences into list of ipa chars
        remove_chars(chars, [' ','ˈ']) #remove spaces and emphasis markers to create clusters

        ipa.write(''.join(chars) + '\n')#make file of ipa sentences - maybe figure out spaces later
        
        remove_vowels(chars, ipa_consts) #isolate clusters by removing everything left
        process_sentence(chars,clusters) #update dict with clusters and prevalence

#write dict to csv file
with open('clusters_en.csv', 'w', newline='', encoding="utf-8-sig") as csvfile:
    writer = csv.writer(csvfile)
    for i in clusters.items():
        writer.writerow(i)
