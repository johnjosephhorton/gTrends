johnjosephhorton
================

Python Scraping(johnjosephhorton)

1) There are several files.

- 2 python files
  pyGoogleTrendsCsvDownloader.py - google trends scraber python module
  pyGoogleTrendsCsvToSQLite.py   - Parse csv file and export into sqlite db

- 2 configuration files
  config.txt         - read login and password to be used to connect to Google Trends
    # config.txt
    username:grytsenko.bamboo@gmail.com
    password:XXXXXX

  query_args_lst.txt -  read queries (a tuple of search terms that will be comma separated in the search box)
    #query_args_lst.txt
    python,php
    cat,mouse,dog
    Django,Zend,Symfony
- 1 SQLite db file
  google_trends_db - sqlite db file

- When this scraper running, CSV files are generated in the same folder path.


2) How to run this scraper.

- Run on console.

  >> pyGoogleTrendsCsvToSQLite.py
  >> pyGoogleTrendsCsvToSQLite.py -c <conffile> -q <queryfile>
  >> pyGoogleTrendsCsvToSQLite.py --conffile <conffile> --queryfile <queryfile>

  for ex)
  >> pyGoogleTrendsCsvToSQLite.py
  >> pyGoogleTrendsCsvToSQLite.py -c config.txt -q query_args_lst.txt
  >> pyGoogleTrendsCsvToSQLite.py --conffile config.txt --queryfile query_args_lst.txt


  Note: You can omit arguments and in this case default values are used.
        <conffile> - config.txt
        <queryfile> - query_args_lst.txt

