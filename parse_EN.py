import pandas as pd
from parse_PL import combine_digraphs,remove_chars,remove_vowels

ipa_consts = ['b','d','f','g','h','j','k','l','m','n','ŋ','p','r','s','ʃ','t','v','w','z','θ','ð','ts','dz','dʒ','tʃ']
di_ipa = ['ts','dz','dʒ','tʃ']

df = pd.read_csv('data_en/sentences_en.csv')

for s in df['phonemes']:
    chars = combine_digraphs(s, di_ipa) #turn ipa sentences into list of ipa chars
    remove_chars(chars, [' ','ˈ'])
    remove_vowels(chars, ipa_consts)
    #now combine clusters and write to list/file
