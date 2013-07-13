gTrends 
=======

## Overview 
This is a Python-based program for executing queries against Google Trends, collecting the resulting time-series data and writing it to a local SQLite database file. 
The repository also includes some example R code for working with the resulting data. 

## Configuration 

There is a file `config.txt` for your gmail username and password: 

```
username:<scraper_guy>@gmail.com
password:XXXXXX
```

And a file containing your query terms, in `query_ars_lst.txt`: 
```
python,php
cat,mouse,dog
Django,Zend,Symfony
```

## How to run 
Once your files are set-up, run: 

`` $ python gTrends.py --conffile <conffile> --queryfile <queryfile> ``

This wille execute your query and return the results to `google_trends_db`. 
The raw CSV files are written to the folder `/csv_results`. 
Note: You can omit arguments and in this case default values are used.
  
## Data Structures in the SQLite database 

TBD.  

## Access your data with R 

```
library(RPostgreSQL)
library(RSQLite)
   
db <- dbConnect(SQLite(), dbname="google_trends_db")
df <- dbGetQuery(db, "select * from search_volume") 
```

