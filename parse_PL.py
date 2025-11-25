from conllu import parse_incr
from io import open
import csv
import convert_ipa.pl_to_ipa as ipa

sentences = [] #contains full sentences after parsing 
clusters = {} #dict to contain each cluster and their number of occurences

consts = ['b','d','f','g','h','j','k','l','m','n','ŋ','ɲ','p','r','s','ɕ','ʂ','t','v','w','z',
          't͡s','d͡z','d͡ʐ','t͡ʂ','d͡ʑ','t͡ɕ','ʐ','ʑ','x'] #ipa consonants present in polish



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
        if chars[i] not in [' ', 'j','ci','si','zi','dzi']: #starting at each consonant
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



### PROCESSING

#parse file to sentences
data_file = open("data_pl/pl_pdb-ud-dev.conllu", "r", encoding="utf-8")
for tokenlist in parse_incr(data_file):
    #remove any sentences with abbreviations; cannot be accurately transcribed
    if not any(token.get('feats') and token.get('feats').get('Abbr') == 'Yes' for token in tokenlist):
        #remove acronyms; they are not pronounced
        if not any(str(token).isupper() and len(str(token)) > 1 for token in tokenlist):
            sentences.append(tokenlist.metadata.get('text')) #convert conllu to normal sentences

#write sentences to text file for easier reading
with open ('data_pl/sentences_pl.txt', 'w', encoding="utf-8-sig") as txt:
    for i in sentences:
        txt.write(i + "\n")

#find clusters and write to db (dict)
with open ('data_pl/ipa_sentences_pl.txt', 'w', encoding="utf-8-sig") as wtr:
    for i in sentences:
        chars = list(i.lower()) #make each sentence into a list of lowercase characters
        ipa.convert(chars) #convert polish to ipa for easier comparison

        wtr.write(''.join(chars) + '\n')#print sentences in ipa form for reference

        remove_chars(chars, [' ']) #remove spaces to allow clustering between words
        remove_vowels(chars, consts) #remove vowels to create clusters
        process_sentence(chars,clusters) #write to dict

#write dict to csv
with open('clusters_pl.csv', 'w', newline='', encoding="utf-8-sig") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['cluster','occurences'])
    for i in clusters.items():
        writer.writerow(i)