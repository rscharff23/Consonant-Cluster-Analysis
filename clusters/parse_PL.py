from conllu import parse_incr
from io import open
import csv
from convert_ipa.pl_ipa import ipa_polish 
import pandas as pd

sentences = [] #contains full sentences after parsing 
clusters = {} #dict to contain each cluster and their number of occurences

#ipa consonants present in polish
consts = ['b','d','f','g','h','j','k','l','m','n','ŋ','ɲ','p','r','s','ɕ','ʂ','t','v','w','z',
          't͡s','d͡z','d͡ʐ','t͡ʂ','d͡ʑ','t͡ɕ','ʐ','ʑ','x','ɣ','d͡ʒ','t͡ʃ','ʒ','ʃ','ʧ','ʤ','ʦ','ʣ'] 

simplified = {'d͡ʐ':'ʤ','t͡ʂ':'ʧ','d͡ʑ':'ʤ','t͡ɕ':'ʧ','ɕ':'ʃ','ʂ':'ʃ','ʐ':'ʒ','ʑ':'ʒ','t͡s':'ʦ','d͡z':'ʣ'}



### FUNCTIONS

#remove spaces (or other dividing chars), allowing for clusters across words
def remove_chars(chars, rem):
    for i in rem: #allow for multiple chars to be removed from string
        while 1<2: #go until we get value error from no more spaces
            try:
                chars.remove(i)
            except (ValueError):
                break

#remove vowels to isolate clusters
def remove_vowels(chars, cons):
    for i in range(len(chars)):
        if chars[i] not in (cons):
            chars[i] = ' '#set vowels and other chars to spaces, keeping clusters separate



#the following approach adds all clusters of size >= char_min to the db, and within each cluster
#includes any subclusters of sufficient size; eg. adds not only ftb but also ft and fb
def process_sentence(chars, cl_dict):
    char_min = 2 #change this to adjust minimum necessary sounds
    for i in range(len(chars)-1):
        if chars[i] not in [' ', 'j']: #starting at each consonant, j not consonant at start of cluster
            count = 1 #cluster must have at least 2 sounds
            while chars[i+count] != ' ': #until we find a vowel/other symbol
                cl = ''
                for j in range(i,i+count+1):
                    cl += chars[j] #finally add chars back together
                if count+1 >= char_min: #check size of cluster and add if big enough
                    if cl not in cl_dict.keys(): #add new entry to dict
                        cl_dict.update({cl:1})
                    else: #increase cluster counter
                        cl_dict[cl] += 1
                count += 1 #check next char

def lng(clust):
    arr = []
    for i in clust:
        arr.append(len(i))
    return arr

#combine digraphs (rz,cz,sz,dż,dź,ch,si,ci,dzi,zi) to one character
def combine_digraphs(chars,digraphs):
    chars.append('.') #fixes bounding problem of some sentences not ending with period
    i = 0
    while i < len(chars)-1:
        if chars[i] + chars[i+1] in digraphs or chars[i+1] == '͡': #check if next two letters are a digraph
            if chars[i+1] == '͡':
                chars[i] = chars[i]+chars[i+1]+chars[i+2]
                chars.pop(i+2)
            else:
                if chars[i+1] + chars[i+2] == 'zi':
                    chars[i] = 'dzi' #special case for dzi
                    chars.pop(i+2)#and remove i
                else:           
                    chars[i] = chars[i]+chars[i+1] #if so, combine them into one
            chars.pop(i+1) #and remove next
        i += 1


### PROCESSING

#parse file to sentences
data_file = open("clusters/data_pl/pl_pdb-ud-train.conllu", "r", encoding="utf-8")
for tokenlist in parse_incr(data_file):
    #remove any sentences with abbreviations; cannot be accurately transcribed
    if not any(token.get('feats') and token.get('feats').get('Abbr') == 'Yes' for token in tokenlist):
        #remove acronyms; they are not pronounced
        if not any(str(token).isupper() and len(str(token)) > 1 for token in tokenlist):
            sentences.append(tokenlist.metadata.get('text')) #convert conllu to normal sentences

#write sentences to text file for easier reading
with open ('clusters/data_pl/sentences_pl.txt', 'w', encoding="utf-8-sig") as txt:
    for i in sentences:
        txt.write(i + "\n")

#find clusters and write to db (dict)
with open ('clusters/data_pl/ipa_sentences_pl.txt', 'w', encoding="utf-8-sig") as wtr:
    for i in sentences:

        sent = ipa_polish(i.lower()) #convert polish to ipa for easier comparison
        wtr.write(sent + '\n')#print sentences in ipa form for reference

        chars = list(sent) #reformat sentence to list of chars for ease
        combine_digraphs(chars, []) #combine ipa digraphs to one char slot

        #the following modification is made solely for the purposes of comparison with the english
        #language, when analyzing polish alone, remove it
        chars = [simplified.get(i,i) for i in chars] # changes ɕ,ʂ,ʐ,ʑ to match simplified english ipa


        remove_chars(chars, [' ']) #remove spaces to allow clustering between words
        remove_vowels(chars, consts) #remove vowels to create clusters
        process_sentence(chars,clusters) #write to dict

data = {#reformat to dataframe
    'cluster': clusters.keys(),
    'occurences_pl': clusters.values(),
    'length': lng(clusters.keys()) #get length of each cluster
}
df = pd.DataFrame(data)

#write to csv
df.to_csv('clusters/clusters_pl.csv',index=False)