
# coding: utf-8

# In[2]:


import sqlite3
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string


# In[3]:


conn = sqlite3.connect('search_engine.db')
cur = conn.cursor()

     
cur.execute('''CREATE TABLE IF NOT EXISTS Ranking
    (url TEXT PRIMARY KEY, rank INTEGER DEFAULT 1)''')


cur.execute('''CREATE TABLE IF NOT EXISTS Popularity
   (from_id TEXT, to_id TEXT , PRIMARY KEY (from_id, to_id)  )''')


# In[5]:


cur.execute("SELECT keyword, Indexing.url,rank from Indexing INNER JOIN Ranking on Indexing.url=Ranking.url")
index=cur.fetchall()


# In[9]:


Query=input("What you want to search??")


# In[10]:


stop_words = set(stopwords.words('english'))
table = str.maketrans('', '', string.punctuation)
Query = word_tokenize(Query)
Query = [w.translate(table) for w in Query]
Query= [w.lower().strip() for w in Query if not w in stop_words]


# In[16]:


result=[]
for word in Query:
    for row in index:
        roww=[]
        if word in row[0]:
            roww.append(row[1])
            roww.append(row[2])
            result.append(roww)

            


# In[19]:


x=sorted(result,key=lambda l:l[1], reverse=True)


# In[25]:


print("Searched results are:")
for i in x:
    print(i[0])

