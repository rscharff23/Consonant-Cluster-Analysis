from conllu import parse_incr
from io import open
import csv

sentences = [] #contains full sentences after parsing 
clusters = {} #dict to contain each cluster and their number of occurences
consts = ['b','c','ć','d','f','g','h','j','k','l','ł','m','n','ń','p','q','r','s','ś','t','v','w','x','z','ź','ż'] 
#TODO - adjust for special cases like ci/si, (vowel)-j, etc.

#remove spaces, allowing for clusters across words, then apply translation
def remove_spaces(s):
    s = s.replace(" ","")
    return "".join(ch if ch in consts else " " for ch in s)#remove all chars except consonants

#parse file to sentences
data_file = open("pl_pdb-ud-dev.conllu", "r", encoding="utf-8")
for tokenlist in parse_incr(data_file):
    sentences.append(tokenlist.metadata.get('text').lower()) #convert conllu to normal (LC) sentences

with open ('sentences.txt', 'w', encoding="utf-8-sig") as txt:
    for i in sentences:
        txt.write(i + "\n")

for i in sentences:
    remvd = remove_spaces(i) 
    for word in remvd.split():
        if len(word) > 1:#not a cluster otherwise
            if word not in clusters.keys(): #add new entry to dict
                clusters.update({word:1})
            else: #increase counter
                clusters[word] += 1

with open('clusters.csv', 'w', newline='', encoding="utf-8-sig") as csvfile:
    writer = csv.writer(csvfile)
    for i in clusters.items():
        writer.writerow(i)
#export to csv
#fix so numbers and other chars are not included