#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re
from pattern.en import lexeme
from nltk.stem import WordNetLemmatizer

def counting_words(words):
    word_count = {}
    for word in words:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    return word_count

def prob_cal(word_count_dict):
    probs = {}
    m = sum(word_count_dict.values())
    for key in word_count_dict.keys():
        probs[key] = word_count_dict[key] / m
    return probs

def LemmWord(word):
    return list(lexeme(word))[0]

def colab_1(word, allow_switches=True):
    colab_1 = set()
    colab_1.update(DeleteLetter(word))
    if allow_switches:
        colab_1.update(Switch_(word))
    colab_1.update(Replace_(word))
    colab_1.update(insert_(word))
    return colab_1

def colab_2(word, allow_switches=True):
    colab_2 = set()
    edit_one = colab_1(word, allow_switches=allow_switches)
    for w in edit_one:
        if w:
            edit_two = colab_1(w, allow_switches=allow_switches)
            colab_2.update(edit_two)
    return colab_2

def get_corrections(word, probs, vocab, n=2):
    suggested_word = []
    best_suggestion = []
    suggested_word = list(
        (word in vocab and word) or colab_1(word).intersection(vocab)
        or colab_2(word).intersection(vocab))

    best_suggestion = [[s, probs[s]] for s in list(reversed(suggested_word))]
    return best_suggestion

def DeleteLetter(word):
    delete_list = []
    split_list = []

    for i in range(len(word)):
        split_list.append((word[0:i], word[i:]))

    for a, b in split_list:
        delete_list.append(a + b[1:])
    return delete_list

def Switch_(word):
    split_list = []
    switch_l = []

    for i in range(len(word)):
        split_list.append((word[0:i], word[i:]))
    
    switch_l = [a + b[1] + b[0] + b[2:] for a, b in split_list if len(b) >= 2]
    return switch_l

def Replace_(word):
    split_l = []
    replace_list = []

    for i in range(len(word)):
        split_l.append((word[0:i], word[i:]))
    alphs = 'abcdefghijklmnopqrstuvwxyz'
    replace_list = [a + l + (b[1:] if len(b) > 1 else '')
                    for a, b in split_l if b for l in alphs]
    return replace_list

def insert_(word):
    split_l = []
    insert_list = []

    for i in range(len(word) + 1):
        split_l.append((word[0:i], word[i:]))

    alphs = 'abcdefghijklmnopqrstuvwxyz'
    insert_list = [a + l + b for a, b in split_l for l in alphs]
    return insert_list

w = []
with open('final.txt', 'r', encoding="utf8") as f:
    file_name_data = f.read()
    file_name_data = file_name_data.lower()
    w = re.findall('\w+', file_name_data)

main_set = set(w)

my_word = input("Enter any word:")
word_count = counting_words(main_set)
probs = prob_cal(word_count)

tmp_corrections = get_corrections(my_word, probs, main_set, 2)
for i, word_prob in enumerate(tmp_corrections):
    if(i < 3):
        print(word_prob[0])
    else:
        break


# In[ ]:




