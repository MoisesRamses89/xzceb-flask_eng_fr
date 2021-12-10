from collections import defaultdict
import re
import string
from string import *
from itertools import product
from contextlib import closing
#import codecs
#import shelve
import math
import json

def make_listoflist(file):
    max_length = 0
    eng_sen = list(open(file, "r", encoding='utf-8').readlines())
    sen_list = []
    temp = []
    for idx, sen in enumerate(eng_sen):
        temp = [x.strip(string.punctuation) for x in sen.split()]
        # sen = sen.translate(None, string.punctuation)
        # #print sen
        # temp = sen.split()
        if (len(temp)>max_length):
            max_length = len(temp)
        sen_list.append(temp)
        print (temp)
        if(idx == 1000):
            break;
    return sen_list,max_length

#########################################

#l = max length of english sen; m = max length of foreign sen, j - index of english word, i-of foreign word
def init_q(q_dist,l,m):
    for a in range(l):
        for b in range(m):
            for c in range(0,a):#j in video
                for d in range(0,b):#i in video
                    q_dist[repr((c+1,d+1,a+1,b+1))] = 0.25#randomly assign some value
    return q_dist

#update q_dist

def update_q(q_dist,l,m,c_dist,count_denom):
    for a in range(l):
        for b in range(m):
            for c in range(0,a):#j in vide0
                for d in range(0,b):
                    if (count_denom[(d+1,a+1,b+1)]!=0):
                        q_dist[repr((c+1,d+1,a+1,b+1))] = c_dist[(c+1,d+1,a+1,b+1)]*1.0 / count_denom[(d+1,a+1,b+1)]
    return q_dist

#l = len of eng sen, m-len of foreign sen
# def set_count(c_dist,l,m):#c[j/i,l,m]
#     for a in range(l):
#         for b in range(m):
#             for c in range(0, a):
#                 for d in range(0, b):
#                     c_dist[(c + 1, d + 1, a + 1, b + 1)] = 0  # randomly assign some value
#     return c_dist

# def set_count_denom(count_denom,l,m):    #c[i,l,m]
#     for a in range(m):
#         for b in range(l):
#             for c in range(0,a):#i in video
#                 count_denom[(c+1,l+1,m+1)] = 0
#     return count_denom
#########################################################################

def tokenize_normalize_eng(lis):
    return lis

def tokenize_normalize_french(lis):
    return lis

#stop_words_eng = set(stopwords.words('english'))
#stop_words_french = set(stopwords.words('french'))
# eng_count = {}
l,m = 0,0
# eng_lis = []
# french_lis = []
# eng_lis,l = make_listoflist('english.txt')        #english.txt to be stored in the same folder as this file
# french_lis,m = make_listoflist('french.txt')
# terms_eng = []          #same as eng_lis as there is no normalization 
# terms_french = []

# for lis in eng_lis:
#     terms_eng.append(tokenize_normalize_eng(lis))   #returns the same lis - there is no normalization
# for lis in french_lis:
#     terms_french.append(tokenize_normalize_french(lis))

# eng_words = []                  # contain list of all terms in english
# for terms in terms_eng:
#     for term in terms:
#         eng_words.append(term)

# french_words = []               # contains list of all terms in French
# for terms in terms_french:
#     for term in terms:
#         french_words.append(term)

#     #list of unique words
# eng_words = list(set(eng_words))
# french_words = list(set(french_words))

# sen_num = len(terms_eng)            #store number of sentences in parallel corpora
# eng_words_num =  len(eng_words)
# french_words_num = len(french_words)
# count_ef = {}   # stores count : count(e|f) - used for f->e
# count_fe = {}   # stores count : count(f|e) used for e-> f
# total_f = {}    # for f->e
# total_e = {}    # for e->f



#set initial translation parameter french to english
#Sep 1: will store p(e|f) intial parameter setting for each e-f or f-e word pair

def init_tp_fe(eng_words_num):

    # for e_term in eng_words:
    #     for f_term in french_words:
    #         #print ("Considering french word")
    #         tp_init_fe[repr((e_term,f_term))] = 1 / float(eng_words_num)

    return defaultdict(lambda: (1/float(eng_words_num)))

def init_tp_ef(french_words_num):
    
    # for f_term in french_words:
    #     for e_term in eng_words:
    #         tp_init_ef[repr((f_term,e_term))] = 1 / float(french_words_num)

    return defaultdict(lambda: (1/float(french_words_num)))

##    IBM Model 1 and 2 Training     ##


def makedict(tp_init_fe, tp_init_ef, q_dist, terms_eng, terms_french, eng_words, french_words):

    sen_num = len(terms_eng)            #store number of sentences in parallel corpora
    eng_words_num =  len(eng_words)
    french_words_num = len(french_words)
    # print ("Initialising tp_init_fe")
    # tp_init_fe = init_tp_fe(eng_words_num)
    # print ("Initialising tp_init_ef")
    # tp_init_ef = init_tp_ef(french_words_num)


    # #printing some data for debugging purpose
    # print (tp_init_ef[repr(('the', 'la'))])
    # print (terms_eng)
    # print (terms_french)
    # print (eng_words)
    # print (french_words)
        
    # count_ef = {}; count_fe = {}; total_f = {}; total_e = {}
    num = 0
    while num<10:
        count_ef = defaultdict(int)
        count_fe = defaultdict(int)
        total_f = defaultdict(int)
        total_e = defaultdict(int)

        ##################################           Distortion parameter needed in Model 2
        c_dist = defaultdict(int)
        count_denom = defaultdict(int)
        #q_dist = init_q(q_dist,l,m)
        #q_dist = defaultdict(float)
        ###################################

        for sen in range(sen_num):

            print ("Considering sentence #", sen)
            frenchwords = len(terms_french[sen])
            engwords = len(terms_eng[sen])
            #print "Engwords  = ", engwords, "Frenchwords = ", frenchwords
            A = terms_eng[sen]
            B = terms_french[sen]
        
            s_total = []    
            s_total1 = [0] * len(french_words) # for e->f
            for i in range(engwords):
                s_total.append(0)
                for j in range(frenchwords):
                    z = tp_init_fe[repr((A[i],B[j]))]
                    s_total[i] = s_total[i] + z

            for i in range(frenchwords):
                for j in range(engwords):
                    z = tp_init_ef[repr((B[i],A[j]))]
                    s_total1[i] += z

        #collect counts for f->e
            for i in range(engwords): 
                for j in range(frenchwords):
                    count_ef[(A[i],B[j])] =  count_ef[(A[i],B[j])] + tp_init_fe[repr((A[i],B[j]))]*1.0 / s_total[i]*1.0
                    total_f[B[j]] = total_f[B[j]] + tp_init_fe[repr((A[i],B[j]))]*1.0 / s_total[i]*1.0
                    delta = tp_init_fe[repr((A[i],B[j]))]*1.0 / s_total[i]*1.0
                    count_ef[(A[i],B[j])] =  count_ef[(A[i],B[j])] + delta
                    total_f[B[j]] = total_f[B[j]] + delta
                    ################################################here delta is stored
                    c_dist[(i,j,engwords,frenchwords)] = c_dist[(i,j,engwords,frenchwords)] + delta
                    count_denom[(j,engwords,frenchwords)] = count_denom[(j,engwords,frenchwords)] + delta
                    ####################

            #collect counts for e->f
            for i in range(frenchwords):
                for j in range(engwords):
                    count_fe[(B[i], A[j])] = count_fe[(B[i], A[j])] + tp_init_ef[repr((B[i],A[j]))]*1.0 / s_total1[i]*1.0;
                    total_e[A[j]] += (tp_init_ef[repr((B[i],A[j]))]*1.0) / s_total1[i]*1.0

    #end for loop for sentence pair
    #estimate probabilities for f->e
        print ("Now going to estimate the probabilities", num)

        for (f_word,e_word) in product(french_words,eng_words):
            tp_init_fe[repr((e_word,f_word))] = count_ef[(e_word,f_word)]*1.0 #/ total_f[f_word]*1.0
            tp_init_fe[repr((e_word,f_word))] /= total_f[f_word]
            if tp_init_fe[repr((e_word,f_word))] > 0.5:
                print (e_word,f_word)
 
            # if tp_init_fe[repr((e_word,f_word))] > 0.01 and tp_init_fe[repr((e_word,f_word))] < 0.99:
            #     flag = 1

        print ("going to tp_ef")

        for (e_word,f_word) in product(eng_words,french_words):
            tp_init_ef[repr((f_word,e_word))] = count_fe[(f_word,e_word)]*1.0
            tp_init_ef[repr((f_word,e_word))] /= total_e[e_word]

            # if tp_init_ef[repr((f_word,e_word))] > 0.01 and tp_init_ef[repr((f_word,e_word))] < 0.99:
            #     flag1 = 1

        #############
        #q_dist = update_q(q_dist,l,m,c_dist,count_denom)
        ############

        num += 1
        # if (flag == 0 and flag1 == 0):             #Max 10 iterations of the training model
        #     break


def main():
    
    #stop_words_eng.update(['.', ',', '"', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}', '<', '>', '-'])
    #stop_words_french.update(['.', ',', '"', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}', '<', '>', '-'])
    eng_count = {}
    eng_lis = []
    french_lis = []
    eng_lis,l = make_listoflist('../Documents/english.txt')        #english.txt to be stored in the same folder as this file
    french_lis,m = make_listoflist('../Documents/french.txt')
    terms_eng = []          #same as eng_lis as there is no normalization 
    terms_french = []

    for lis in eng_lis:
        terms_eng.append(tokenize_normalize_eng(lis))   #returns the same lis - there is no normalization
    for lis in french_lis:
        terms_french.append(tokenize_normalize_french(lis))

    eng_words = []                  # contain list of all terms in english
    for terms in terms_eng:
        for term in terms:
            eng_words.append(term)

    french_words = []               # contains list of all terms in French
    for terms in terms_french:
        for term in terms:
            french_words.append(term)

        #list of unique words
    eng_words = list(set(eng_words))
    french_words = list(set(french_words))

    print ("The training code for Model 1 and Model 2\n")

    #printing associated metadata
    print ("Number of unique terms ========")
    print (len(eng_words), len(french_words))
    print ("Number of sentences ===========")
    print (len(terms_eng),len(terms_french))

    #using shelve to store the dicts in secondary storage to avoid memory overflow and for persistence
    # shelf1 = shelve.open('shelf_fe.shelf', 'n')##, writeback = 'True')
    # shelf2 = shelve.open('shelf_ef.shelf', 'n')#, writeback = 'True')
    # shelf3 = shelve.open('shelf_q.shelf', 'n')#, writeback = 'True')
    # shelf4 = shelve.open('shelf_countef.shelf', 'c', writeback = 'True')
    # shelf5 = shelve.open('shelf_countfe.shelf', 'c', writeback = 'True')
    # shelf6 = shelve.open('shelf_totalf.shelf', 'c', writeback = 'True')
    # shelf7 = shelve.open('shelf_totale.shelf', 'c', writeback = 'True')
    eng_words_num = len(eng_words)
    french_words_num =  len(french_words)
    tp_init_ef = defaultdict(lambda: (1/float(french_words_num)))
    tp_init_fe = defaultdict(lambda: (1/float(eng_words_num)))
    q_dist = defaultdict(float)

    makedict(tp_init_fe, tp_init_ef, q_dist, terms_eng, terms_french, eng_words, french_words)

    with open('dict_fe.json', 'w') as fe:
        json.dump(tp_init_fe, fe)
    with open('dict_ef.json', 'w') as ef:
        json.dump(tp_init_ef, ef)
    # with open('dict_q.json', 'w') as q1:
    #     json.dump(q_dist, q1) 
    
    # try:
    #     makedict(shelf1, shelf2, shelf3, terms_eng, terms_french, eng_words, french_words)
    # finally:
    #     shelf1.close()
    #     shelf2.close()
    #     shelf3.close()
        # shelf4.close()
        # shelf5.close()
        # shelf6.close()
        # shelf7.close()


    print ("The parameters of the model are")

    print ("For F->E")
    my_dict = {}
    # with closing(shelve.open('shelf_fe.shelf')) as d:
    #     #print (d.keys())
    #     for fword in french_words:
    #         for eword in eng_words:
    #             if (d[repr((eword,fword))]>0.8):
    #                 print (d[repr((eword,fword))])
    #                 print (eword,fword)
    with open('dict_fe.json') as fe:
        my_dict = json.load(fe)
    for fword in french_words:
        for eword in eng_words:
            if(my_dict[repr((eword,fword))] > 0.5):
                print (my_dict[repr((eword,fword))])
                print (eword,fword) 
        # for setstr in d.keys():
        #     if(d[setstr] > 0.5):       #printing only those pairs for which t(e/f) > 0.8
        #         print (d[setstr])
        #         print (eval(setstr))

    print ("For E->F")

    #with closing(shelve.open('shelf_ef.shelf')) as d:
        #print (len(d))
    with open('dict_ef.json') as ef:
        my_dict = json.load(ef)
    for (fword,eword) in product(french_words,eng_words):
        if (my_dict[repr((fword,eword))]>0.5):
            print (my_dict[repr((fword,eword))])
            print (fword,eword)
# For n = 100
# For F->E
# 259740
# 0.896450846067
# ('not', 'pas')
# 0.866547799617
# ('since', 'depuis')
# 0.852980207488
# ('which', 'sur')
# 0.806638447926
# ('and', 'et')
# 0.815380063442
# ('case', 'cas')
# 0.952513323071
# ('I', 'je')
# 0.84478030879
# ('Thursday', 'jeudi')
# For E->F
# 259740
# 0.806823021333
# ('les', 'requested')
# 0.806996010033
# ('cas', 'case')
# 0.910554164145
# ('nous', 'we')
# 0.889608982127
# ('et', 'and')
# 0.836539925525
# ('je', 'I')

if __name__ == '__main__':
    main()
