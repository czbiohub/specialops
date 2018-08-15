
# coding: utf-8
# In[1]: import pandas and read txt file from wrapper script into dataframe
import pandas as pd
df=pd.read_csv('DASHH_test.txt',delimiter='\s',encoding='utf-8', engine ='python', header=None)

# In[3]:

rows=list(range(len(df)))
rows_to_drop=[2*x+1 for x in rows]
rows_to_drop= [x for x in rows_to_drop if x<(len(df)+1)]


# In[4]:


df=df.drop(df.index[rows_to_drop])




# In[5]:


df = df[[3,5,7,9]]



# In[6]:


df=df.reset_index(drop=True)



# In[7]:


df=df.rename(index=int, columns={3 : "Guide Library", 5 : "Filename",7 : "Reads DASHed",9 : "Percent DASHed"})


# In[8]:


guidelibrary = df['Guide Library'].str.split('/',expand=True)



# In[9]:


df['Guide Library'] = guidelibrary[guidelibrary.columns[-1]]



# In[10]:


df['Percent DASHed']=df['Percent DASHed'].str.strip('%')




# In[12]:


reads = df['Reads DASHed'].str.split('/',expand=True)



# In[14]:


reads= reads.rename(index=int, columns={ 0 : "total reads DASHed", 1 : "total reads"})





# In[16]:


df=pd.concat([df, reads],axis=1)




# In[18]:


df=df.drop('Reads DASHed',axis=1)



# In[23]:


df.to_csv("DASH_output.csv")
