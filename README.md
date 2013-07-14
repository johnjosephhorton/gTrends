gTrends 
=======

This is a Python-based program for executing queries against Google Trends, collecting the resulting time-series data and writing it to a local SQLite database file. 
The repository also includes some example R code for working with the resulting data. 

![Image](http://dl.dropboxusercontent.com/u/420874/permanent/example_search_results.png)


## Dependencies

Python2.6+

## Installation for users

Install python modules such as lxml3.0.1 using pip.

```
pip install -r requirements.txt
```

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

There is a SQL backup file called `google_trends_db_schema.sql`.
```
BEGIN TRANSACTION;
CREATE TABLE meta_data (group_id NUMERIC, launched TEXT, pk_id INTEGER PRIMARY KEY, query_string TEXT, url TEXT);
...
COMMIT;
```

## How to run 
Once your files are set-up, run: 

`` $ python gTrends.py  --conffile <conffile> --queryfile <queryfile> --csvsubfolder <csvsubfolder> ``

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

