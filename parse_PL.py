from conllu import parse_incr
from io import open
import csv

sentences = [] #contains full sentences after parsing 
clusters = {} #dict to contain each cluster and their number of occurences
consts = ['b','c','ć','d','f','g','h','j','k','l','ł','m','n','ń','p','q','r','s','ś','t','v','w','x','z','ź','ż', ' '] 
di_pl = ['cz','sz','rz','dż','dź','dz','ch','si','ci','zi']
#replace above arrays with one ipa list soon

#combine digraphs (rz,cz,sz,dż,dź,ch) to one character, to count sounds better
def combine_digraphs(s,digraphs):
    chars = list(s) #array of characters
    chars.append('.') #fixes bounding problem of some sentences not ending with period
    i = 0
    while i < len(chars)-1:
        if chars[i] + chars[i+1] in digraphs: #check if next two letters are a digraph
            if chars[i+1] + chars[i+2] == 'zi':
                chars[i] = 'dzi' #special case for dzi
                chars.pop(i+2)#and remove i
            else:           
                chars[i] = chars[i]+chars[i+1] #if so, combine them into one
            chars.pop(i+1) #and remove next
        i += 1
    return(chars)

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
def process_sentence(chars):
    char_min = 2 #change this to adjust minimum necessary sounds
    for i in range(len(chars)-1):
        if chars[i] not in [' ', 'j','ci','si','zi','dzi']: #starting at each consonant
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

#parse file to sentences
data_file = open("data_pl/pl_pdb-ud-train.conllu", "r", encoding="utf-8")
for tokenlist in parse_incr(data_file):
    sentences.append(tokenlist.metadata.get('text')) #convert conllu to normal sentences

#write sentences to text file for easier reading
with open ('sentences.txt', 'w', encoding="utf-8-sig") as txt:
    for i in sentences:
        txt.write(i + "\n")

#find clusters and write to db (dict)
for i in sentences:
    chars = combine_digraphs(i.lower(), di_pl)#make lowercase each sentence

    #TODO here - write function that turns letters into ipa

    remove_chars(chars, [' '])

    remove_vowels(chars, consts + di_pl) #update this to be ipa chars once that is changed

    process_sentence(chars) 

with open('clusters_pl.csv', 'w', newline='', encoding="utf-8-sig") as csvfile:
    writer = csv.writer(csvfile)
    for i in clusters.items():
        writer.writerow(i)