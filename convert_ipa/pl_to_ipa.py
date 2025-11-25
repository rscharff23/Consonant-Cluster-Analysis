import csv

di_pl = ['cz','sz','rz','dż','dź','dz','ch','si','ci','zi'] #polish 
vw_pl = ['a','ą','e','ę','i','o','ó','u','y']

#read in dict with pl -> ipa matchings
pl_ipa_dict = {}
with open('convert_ipa/pl_ipa_pairs.csv', 'r', encoding="utf-8-sig") as ipa:
    wr = csv.DictReader(ipa)
    for row in wr:
        pl_ipa_dict[row['pl']] = row['ipa']



#combine digraphs (rz,cz,sz,dż,dź,ch,si,ci,dzi,zi) to one character
def combine_digraphs(chars,digraphs):
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

#turns polish (consonant) chars individually into ipa equivalent, resulting sentence is NOT ipa equivalent
#due to voicing and other small quirks which are fixed in a separate function
def convert(chars):
    combine_digraphs(chars,di_pl)
    count = 0
    while count < len(chars):#go through each char
        curr = chars[count]
        if curr in pl_ipa_dict.keys(): #if is changed 1:1 in ipa
            if curr.endswith('i') and chars[count + 1] not in (vw_pl): 
                chars.insert(count+1,'i') #if is ci,si,dzi,zi and no other vowel, insert i afterwards
            chars[count] = pl_ipa_dict.get(curr, curr) #replace with ipa equivalent
            
        elif curr in ['ą','ę']:#phonetic sound depends on next character
            if curr == 'ą':
                chars[count] = 'ɔ'
            else:
                chars[count] = 'ɛ'
            match (chars[count + 1]): #pattern is the same other than for EOW
                case 'k'|'g' :
                    chars.insert(count+1,'ŋ')
                case 't'|'d'|'c'|'dz'|'cz'|'dż':
                    chars.insert(count+1,'n')
                case 'p'|'b':
                    chars.insert(count+1,'m')
                case 'ś'|'ź'|'ć'|'dź'|'si'|'zi'|'ci'|'dzi':
                    chars.insert(count+1,'ɲ')
                case 'f'|'w'|'s'|'z'|'sz'|'ż'|'rz'|'ch'|'h':
                    if curr == 'ą':
                        chars[count] = 'ɔw̃'
                    else:
                        chars[count] = 'ɛw̃'
                case 'l'|'ł': 
                    continue
                case _: #end of word case
                    if curr == 'ą':
                        chars[count] = 'ɔw̃'
            
        count += 1
    
    chars.pop() #remove added final char