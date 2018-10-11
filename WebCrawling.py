
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


ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


# In[3]:


conn = sqlite3.connect('search_engine.db')
cur = conn.cursor()

     
cur.execute('''CREATE TABLE IF NOT EXISTS Pages
    (url TEXT PRIMARY KEY)''')

cur.execute('''CREATE TABLE IF NOT EXISTS Indexing
   (keyword TEXT, url TEXT , PRIMARY KEY (keyword, url)  )''')

cur.execute('''CREATE TABLE IF NOT EXISTS Popularity
   (from_id TEXT, to_id TEXT , PRIMARY KEY (from_id, to_id)  )''')


# In[4]:


to_crawl=[]
crawled=[]
index=[]


# In[5]:


def change_to_crawled(cur):
    crawled =cur.fetchall()
    return [i[0] for i in crawled]
    


# In[6]:


def return_content(p):
    content=[]
    for i in p:
        var=i.text.split()
        for j in var:
            if not j.lower() in content:content.append(j.lower())
    return content


# In[9]:


seed="https://www.py4e.com/"
cur.execute('SELECT url FROM Pages')
crawled =change_to_crawled(cur)
if not seed in crawled:to_crawl.append(seed)


# In[10]:


'''This one'''
cur.execute("SELECT keyword, url  from Indexing")
index=cur.fetchall()
while to_crawl:
    url=to_crawl[0]
    del to_crawl[0]
    cur.execute('INSERT OR IGNORE INTO Pages (url) VALUES ( ? )', ( url, ) )
    conn.commit()
  

    
    print("going to :",url)
    try:
        document = urlopen(url, context=ctx)

        html = document.read()
        if document.getcode() != 200 :
            print("Error on page: ",document.getcode())
            cur.execute('DELETE FROM Pages WHERE url=?', ( url ,) )
            conn.commit()

        if 'text/html' != document.info().get_content_type() :
            print("Ignore non text/html page")
            cur.execute('DELETE FROM Pages WHERE url=?', ( url, ) )
            conn.commit()
            continue     
        
        soup = BeautifulSoup(html, "html.parser")

        a=soup.find_all('a')
        body=soup.find_all('body')
        
        content=" ".join(return_content(body))
        stop_words = set(stopwords.words('english'))
        
        table = str.maketrans('', '', string.punctuation)
        
        content = word_tokenize(content)
        content = [w.translate(table) for w in content]
        content= [w.lower().strip() for w in content if not w in stop_words]


        #print(content)      
        for word in content:
            if (word,url) not in index:
                index.append((word,url))
                cur.execute("INSERT OR IGNORE INTO Indexing (keyword, url) VALUES ( ?,? )", (word, url, ) )
                conn.commit()
            
        for i in a:
            cur.execute("INSERT OR IGNORE INTO Popularity (from_id, to_id) VALUES ( ?,? )", (url, i['href'], ) )
            conn.commit()
            cur.execute('SELECT url FROM Pages')
            crawled=change_to_crawled(cur)
            if i['href'] in to_crawl or i['href'] in crawled: continue
            to_crawl.append( i['href'] ) 
        
            
    except KeyboardInterrupt:
        print('')
        print('Program interrupted by user...')
        break
    except:
        print("Unable to retrieve or parse page")
        cur.execute('DELETE FROM Pages WHERE url=?', ( url, ) )
        conn.commit()
        cur.execute("DELETE FROM Popularity WHERE from_id=?", ( url, ) )
        conn.commit()
        cur.execute("DELETE FROM Popularity WHERE to_id=?", ( url, ) )
        conn.commit()
        continue

print("Crawling complete")

