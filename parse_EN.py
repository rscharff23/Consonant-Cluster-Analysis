import pandas as pd
from parse_PL import combine_digraphs,remove_chars,remove_vowels
import csv

ipa_consts = ['b','d','f','g','h','j','k','l','m','n','ŋ','p','r','s','ʃ','t','v','w','z','θ','ð','ts','dz','dʒ','tʃ']
di_ipa = ['ts','dz','dʒ','tʃ'] #ipa sounds represented by two characters

df = pd.read_csv('data_en/sentences_en.csv')

clusters = {}#dict to hold clusters
for s in df['phonemes']:
    chars = combine_digraphs(s, di_ipa) #turn ipa sentences into list of ipa chars
    remove_chars(chars, [' ','ˈ'])
    remove_vowels(chars, ipa_consts)
    
    #change this to use the polish function once that is fixed, they should be the same
    char_min = 1
    for i in range(len(chars)-1):
        if chars[i] != ' ': #starting at each consonant
            count = 1 #cluster must have at least 2 sounds
            while chars[i+count] != ' ': #until we find a vowel/other symbol
                cl = ''
                for j in range(i,i+count+1):
                    cl += chars[j] #finally add chars back together
                if count+1 >= char_min: #check size of cluster and add if big enough
                    if cl not in clusters.keys(): #add new entry to dict
                        clusters.update({cl:1})
                    else: #increase cluster counter
                        clusters[cl] += 1
                count += 1 #check next char

with open('clusters_en.csv', 'w', newline='', encoding="utf-8-sig") as csvfile:
    writer = csv.writer(csvfile)
    for i in clusters.items():
        writer.writerow(i)
