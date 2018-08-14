
# coding: utf-8

# In[90]:


import pandas
i7 = pandas.read_csv('CZB_TruSeq_12BP_i7.csv')
i5 = pandas.read_csv('CZB_TruSeq_12BP_i5.csv')


# In[91]:


i7.head()
i5.head()


# In[92]:


#function that will give you direct complement of a nucleotide. Character input!
def complement (nucleotide):
    if nucleotide=='A':
        comp='T'
    elif nucleotide=='T':
        comp='A'
    elif nucleotide=='C':
        comp='G'
    elif nucleotide=='G':
        comp='C'
    else:
        comp='N'
    return comp;


# In[93]:


#function that will reverse a sequence of characters. String input!
def reverse (sequence):
    count=0
    reverseseq=''
    nucleotides=list(sequence)
    for nucleotide in sequence:
        reverseseq+=nucleotides[len(nucleotides)-count-1]
        count = count+1
    return reverseseq;


# In[94]:


i7["Forward index"].head()


# In[95]:


i7["RevComp Index"] = str(i7["RevComp Index"])
i5["RevComp Index"] = str(i5["RevComp Index"])


# In[96]:


count=0
for forindex in i7["Forward index"]:
    i7.set_value(count, "Comp Index", "".join([complement(y) for y in forindex]))
    i7.set_value(count, "RevComp Index", reverse(i7.iloc[count]["Comp Index"]))
    count = count+1
i7=i7.drop(["Comp Index"], axis=1)


# In[97]:


count=0
for forindex in i5["Forward index"]:
    i5.set_value(count, "Comp Index", "".join([complement(y) for y in forindex]))
    i5.set_value(count, "RevComp Index", reverse(i5.iloc[count]["Comp Index"]))
    count = count+1
i5=i5.drop(["Comp Index"], axis=1)


# In[98]:


i5.head()


# In[89]:


i7.to_csv("CZB_TruSeq_12BP_i7.csv")


# In[99]:


i5.to_csv("CZB_TruSeq_12BP_i5.csv")

