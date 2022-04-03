#!/usr/bin/env python
# coding: utf-8

# In[7]:


import pandas as pd

df = pd.read_csv("Pātimokkha Word by Word.csv", sep="\t", dtype= str)
df.fillna("", inplace=True)


# In[8]:


# filter all SBS words
test1 = df['meaning'] != ""
test2 = df['sentence'] != ""
test3 = df['#'] == "1"
filter = test2 & test1 & test3
df = df.loc[filter]


# In[9]:


# change tamil
test1 = df['meaning'] != ""
filter = test1
df.loc[filter, ['tamil']] = ""


# In[ ]:


# choosing order of columns

df = df[['bhikkhupātimokkhapāḷi', 'pos', 'grammar', '+case', 'tamil', 
        'meaning', 'lit. meaning', 'root', 'rt gp', 'sign', 'base', 
        'construction', 'compound type', 'compound construction', 'abbrev', 
        'source', 'sentence', 'aṭṭhakathā']]


# In[10]:


# save csv
df.to_csv("Pātimokkha Word by Word.csv", sep="\t", index=None)

