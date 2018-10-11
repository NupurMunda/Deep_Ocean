# Mini_Search_Engine
It is a mini search engine using Python

The project contain 4 python programs
1.WebCrawling.py
    -1st and the slowest step
2.Ranking.py
    -to rank the pages
3.Preset.py
    -to reset the rank=1 incase we repeat the 1st step for new page
4.SearchMe.py
    -last step the return list of url of given query
    
Database created"search_engine.db"
tables: 1. Pages
            -contains the list of urls 
        2. Indexing
            -contains the urls and keywords 
        3. Ranking
            -contain the urls and their ranking
        4. Popularity
            -contains the link of from_url to_url
