from contextlib import closing
from collections import defaultdict
import json
import math
#from assign24 import eng_words,french_words,eng_lis,french_lis
from assign24 import make_listoflist, tokenize_normalize_eng, tokenize_normalize_french

def cosineScore(doc1, doc2, dict, listofLists):     #dict = eng_words for english

    #update dict to include terms in doc2
    dict += doc2
    dict = list(set(dict))

    n = len(dict);
    vector1 = [0] * n
    vector2 = [0] * n

    result = 0
    for i in range(n):
        df1 = df(dict[i], listofLists)
        if df1 == 0:
            df1 = 1
        vector1[i] = math.log((1 + termFrequency(dict[i], doc1)), 10) * math.log(float(len(listofLists))/df1, 10)   #does not handle the case when docFrequency is 0
        vector2[i] = math.log((1 + termFrequency(dict[i], doc2)), 10) * math.log(float(len(listofLists))/df1, 10)

        result = result + vector1[i] * vector2[i]
    result = float(result)/(vectorLength(vector1) * vectorLength(vector2))
    return result

def termFrequency(word, doc):
    count = 0
    for i in range(len(doc)):
        if doc[i] == word:
            count += 1
    return count

def df(word, listOfLists):
    count = 0
    for i in range(len(listOfLists)):
        if word in listOfLists[i]:
            count += 1

    return count

def vectorLength(vector):
    sum = 0
    for i in range(len(vector)):
        sum = sum + vector[i]**2
    return math.sqrt(sum)

def jaccardCoeff(wdoc1, wdoc2):    #taking 2 docs as list of words 

    wdoc1_set = set(wdoc1)
    wdoc2_set = set(wdoc2)

    num = (wdoc1_set.intersection(wdoc2_set)).__len__()   #less expensive than len()
    den = (wdoc1_set.union(wdoc2_set)).__len__()

    return float(num)/den

def findEnglish(fword, d, eng_words):
    max = 0; englishwd = ""
    #with closing(shelve.open('shelf_fe.shelf')) as d:
    for eword in eng_words:
        if (repr((fword,eword)) in d.keys()):
            if(d[repr((eword,fword))] > max):
                max = d[repr((eword,fword))]
                englishwd = eword
    return englishwd

def findFrench(eword, d, french_words):
    max = 0; frenchwd = ""
    for fword in french_words:
        if (repr((fword,eword)) in d.keys()):
            if(d[repr((fword,eword))] > max):
                max = d[repr((fword,eword))]
                frenchwd = fword
    return frenchwd

def main():

    #print (eng_words)
    #print (french_words)
    #print (eng_lis)
    eng_lis = []
    french_lis = []
    eng_words = []                  # contain list of all terms in english
    french_words = [] 
    eng_lis,l = make_listoflist('C:/Users/Sameer96/Desktop/english.txt')        #english.txt to be stored in the same folder as this file
    french_lis,m = make_listoflist('C:/Users/Sameer96/Desktop/french.txt')
    terms_eng = []          #same as eng_lis as there is no normalization 
    terms_french = []

    for lis in eng_lis:
        terms_eng.append(tokenize_normalize_eng(lis))   #returns the same lis - there is no normalization
    for lis in french_lis:
        terms_french.append(tokenize_normalize_french(lis))

    for terms in terms_eng:
        for term in terms:
            eng_words.append(term)

    for terms in terms_french:
        for term in terms:
            french_words.append(term)

        #list of unique words
    eng_words = list(set(eng_words))
    french_words = list(set(french_words))
    
    # fe = defaultdict(float)
    # ef = defaultdict(float)

    with open('dict_fe.json') as d:
        fe = json.load(d)           #dict having prob for foreign to english

    with open('dict_ef.json') as d1:
        ef = json.load(d1)          #dict hving prob for eng to french

    n = int(input("Enter number of documents to be translated\n"))
    doclist = [""] * n
    qtlis = [0] * n
    print ("Enter 1 for English to French ; 2 for French to English for each document")
    print ("Enter the path of each doc along with the translation number (1 or 2)\n")
    for i in range(0,n):
        doclist[i] = input()
        qtlis[i] = int(input())
    #print(type(doclist[0]))
    transDoc = []   #list in which each element is a list of words of the translated document produced by model
    for i in range(0,n):
        transDoci = [] #holding the translation of the ith document
        senlist, rdm = make_listoflist(doclist[i])
        #print(type(senlist))

        for sentence in senlist:
            #print(type(sentence))
            for word in sentence:
                if (qtlis[i]==1):
                #enlish doc has to be converted to french
                #for each english word, find the most suitable french word from tp_init_ef
                    fw = findFrench(word, ef, french_words)
                    transDoci.append(fw)
                    print (fw,)
                else:
                #french doc has to be translated to english
                #for each french word, find the most suitable french word from tp_init_fe
                    ew = findEnglish(word, fe, eng_words)
                    transDoci.append(ew)
                    print (ew,)
        transDoc.append(transDoci)      #inserting the translated document (as a list of words)
        print ("\n")

    print ("Enter the paths of the translated versions of the earlier documents")
    translist = [""] * n
    for i in range(0,n):
        translist[i] = input()

    transDocAct = []
    for i in range(0,n):
        transDocActi = []
        senlist, rdm2 = make_listoflist(translist[i])
        for sentence in senlist:
            for word in sentence:
                transDocActi.append(word)
        transDocAct.append(transDocActi)

    jc_sum, cs_sum = 0.0, 0.0
    #compute similarity between the translated doc produced and the actual translated doc
    for i in range(0,n):
        print ("Jaccard Coefficient of the 2 docs is ",)
        jc = jaccardCoeff(transDoc[i], transDocAct[i])
        print (jc)

        print ("Cosine score of the 2 docs is ",)
        if (qtlis[i] == 1):     #translated docs are in French so send the french index
            dict1, listOfList = french_words, french_lis
        else:
            dict1, listOfList = eng_words, eng_lis
        cs = cosineScore(transDoc[i], transDocAct[i], dict1, listOfList)
        print (cs)

        jc_sum += jc
        cs_sum += cs

    print ("Average Jaccard Coefficient = ", jc_sum/n)
    print ("Average Cosine Similarity = ", cs_sum/n)


if __name__ == '__main__':
    main()

