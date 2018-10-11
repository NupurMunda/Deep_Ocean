
# coding: utf-8

# In[1]:


import sqlite3
import urllib.error
import ssl
from urllib.parse import urljoin
from urllib.parse import urlparse
from urllib.request import urlopen
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string


# In[2]:


conn = sqlite3.connect('search_engine.db')
cur = conn.cursor()

     
cur.execute('''CREATE TABLE IF NOT EXISTS Pages
    (url TEXT PRIMARY KEY, rank INTEGER DEFAULT 1)''')

cur.execute('''CREATE TABLE IF NOT EXISTS Indexing
   (keyword TEXT, url TEXT , PRIMARY KEY (keyword, url)  )''')

cur.execute('''CREATE TABLE IF NOT EXISTS Popularity
   (from_id TEXT, to_id TEXT , PRIMARY KEY (from_id, to_id)  )''')
cur.execute('''CREATE TABLE IF NOT EXISTS Ranking
   (url TEXT PRIMARY KEY, rank INTEGER DEFAULT 1 )''')


# In[3]:


cur.execute("select from_id, to_id from Popularity")
pop=cur.fetchall()


# In[4]:


graph={}


# In[5]:


for (i,j) in pop:
    cur.execute ("select to_id from Popularity where from_id=?",(i,))
    to=cur.fetchall()
    to=[i[0] for i in to]
    graph[i]=to


# In[6]:


def compute_ranks(graph):
    d = 0.8 # damping factor
    numloops = 10
    
    ranks = {}
    npages = len(graph)
    for page in graph:
        ranks[page] = 1.0 / npages
    
    for i in range(0, numloops):
        newranks = {}
        for page in graph:
            newrank = (1 - d) / npages
            
            #Insert Code Here
            for node in graph:
                if page in graph[node]:
                    newrank=newrank + d*(ranks[node]/len(graph[node]))
            newranks[page] = newrank
            
        ranks = newranks
        
    return ranks


# In[7]:


new=compute_ranks(graph)


# In[8]:


for k in new:
    cur.execute("INSERT OR IGNORE INTO Ranking (url, rank) VALUES ( ?,? )", (k, new[k], ) )
    conn.commit()

