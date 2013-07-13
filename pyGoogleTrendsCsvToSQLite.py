import re, sys, getopt
import csv
import sqlite3 as lite
import datetime
from pyGoogleTrendsCsvDownloader import pyGoogleTrendsCsvDownloader

def read_ConfInfo(config_file):
    '''
    Read login and password to be used to connect to Google Trends
    default file name: config.txt
    '''
    username = ""
    password = ""
    print "Reading login and password to be used to connect to Google Trends from '" + config_file + "'..."
    try:
        ins = open(config_file, 'r')
        for line in ins:
            p = re.compile(r'^username:(?P<param>.*)')
            m = p.search( line.rstrip() )
            if m is not None and m.group('param') is not None:
                strtmp = m.group('param')
                username = strtmp.strip()
                continue

            p = re.compile(r'^password:(?P<param>.*)')
            m = p.search( line.rstrip() )
            if m is not None and m.group('param') is not None:
                strtmp = m.group('param')
                password = strtmp.strip()
                continue
    except:
        print "Could not open '" + config_file + "' file."
        sys.exit()
        pass

    return {'username':username, 'password':password}

def read_QueriesInfo(queries_file):
    '''
    Read queries (a tuple of search terms that will be comma separated in the search box)
    default file name: query_args_lst.txt
    '''
    queries_lst = []
    print "Reading queries (a tuple of search terms that will be comma separated in the search box) from '" + queries_file + "'..."
    try:
        ins = open(queries_file, 'r')
        for line in ins:
            strtmp = line.strip()
            if len(strtmp) > 0:
                queries_lst.append(strtmp)
    except:
        print "Could not open '" + queries_file + "' file."
        sys.exit()
        pass

    return queries_lst

def parseCsvAndExportToSQLite(query_id, query_str, csvfilename, url_str, dbfilename):
    '''
    Parse CSV file and export into SQLite
    '''
    print 'Parsing "' + csvfilename + '" ...'
    ifile  = open(csvfilename, "rb")
    reader = csv.reader(ifile)

    #Interest over time
    #Week,python,php
    rownum = 0
    beforeInterestOverTime = 0
    headerCols = []
    IntOverTimeData = []
    for row in reader:
        colnum = 0
        if beforeInterestOverTime == 2:
            #now read data lines
            #print headerCols
            if len(row) == len(headerCols):
                IntOverTimeData.append(row)
            else:
                #end of data lines
                beforeInterestOverTime = 3
                continue

        isHeaderLine = False
        for col in row:
            if beforeInterestOverTime == 0:
                #loop until finding "Interest over time" in the first col
                if colnum == 0:
                    str1 = "Interest over time"
                    str2 = col.strip()
                    if str1.upper() == str2.upper():
                        #found
                        beforeInterestOverTime = 1
                        break #next line
            elif beforeInterestOverTime == 1:
                #now read header
                #Week,python,php
                headerCols.append(col.strip())
                isHeaderLine = True
            else:
                pass

            #print col
            colnum += 1
        if beforeInterestOverTime == 1 and isHeaderLine == True:
            beforeInterestOverTime = 2

        rownum += 1

    ifile.close()

    #Now export IntOverTimeData into SQLite db
    #print IntOverTimeData

    con = lite.connect(dbfilename)
    with con:
        cur = con.cursor()
        #INSERT INTO search_term_groups ('id','term') VALUES('1','python')
        for hcol in headerCols[1:]:
            sql = "INSERT INTO search_term_groups ('id','term') VALUES('%d','%s')" % (query_id,hcol)
            cur.execute(sql)

        #INSERT INTO search_volume ('group_id','term','time_period_start','time_period_end','volume') VALUES('%d','%s','%s','%s','%d')" % (,,,)
        for item in IntOverTimeData:
            if len(item[0].strip()) == 23 and len(item) == len(headerCols):
                time_period_start = item[0][:10]
                time_period_end = item[0][13:]
                hcolnum = 1
                for hcol in headerCols[1:]:
                    volume_str = item[hcolnum].strip()
                    if len(volume_str) > 0 and volume_str.isdigit() == True:
                        volume = int(volume_str)
                        sql = "INSERT INTO search_volume ('group_id','term','time_period_start','time_period_end','volume') VALUES('%d','%s','%s','%s','%d')" % \
                              (query_id,hcol,time_period_start,time_period_end,volume)
                        cur.execute(sql)
                    hcolnum += 1

                #INSERT INTO meta_data ('group_id','query_string','launched','url') VALUES('%d','%s','%s','%s')" % (,,,)
                launched = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                sql = "INSERT INTO meta_data ('group_id','query_string','launched','url') VALUES('%d','%s','%s','%s')" % (query_id,query_str,launched,url_str)
                cur.execute(sql)
    return

def main(argv):
    '''
    Main Logic
     1 - Read Config filesq
     2 - Read queries list
     3 - Grab google trends results into csv file
     4 - Parse csv file and export into sqlite db
    '''
    dbfile = "google_trends_db"
    print "SQLite db file: ", dbfile
    config_file = "config.txt"
    queries_file = "query_args_lst.txt"
    thisfile = 'pyGoogleTrendsCsvToSQLite.py'
    #parsing input args
    try:
        opts, args = getopt.getopt(argv,"hc:q:",["conffile=","queryfile="])
    except getopt.GetoptError:
        print thisfile + ' -c <conffile> -q <queryfile>'
        print thisfile + ' --conffile <conffile> --queryfile <queryfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print thisfile + ' -c <conffile> -q <queryfile>'
            print thisfile + ' --conffile <conffile> --queryfile <queryfile>'
            sys.exit()
        elif opt in ("-c", "--conffile"):
            config_file = arg
        elif opt in ("-q", "--queryfile"):
            queries_file = arg
    print 'conffile file is "' + config_file + '"'
    print 'queryfile file is "' + queries_file + '"'

    # 1 - Read Config file
    username = ""
    password = ""
    rtn_confinfo = read_ConfInfo(config_file)
    username = rtn_confinfo['username']
    password = rtn_confinfo['password']
    print "\t", "username : " + username
    #print "password : " + password

    # 2 - Read queries list
    queries_lst = read_QueriesInfo(queries_file)
    print "\t",queries_lst

    # 3 - Grab google trends results into csv file
    #parseCsvAndExportToSQLite(1,
    #                          "python,php",
    #                          "trends_q-python,php.csv",
    #                          "http://www.google.com/trends/explore?q=python%2Cphp#q=python&cmpt=q",
    #                          dbfile)
    #sys.exit()

    r = pyGoogleTrendsCsvDownloader(username, password)
    query_id = 1
    for query in queries_lst:
        rtn = r.get_csv(q=query)
        #parse csv file
        parseCsvAndExportToSQLite(query_id, query, rtn['csvfilename'], rtn['url'], dbfile)
        query_id += 1

if __name__ == "__main__":
    #is being run directly
   main(sys.argv[1:])



#read_ConfInfo(g_config_file)


#r = pyGoogleTrendsCsvDownloader(username, password)
#r.get_csv(cat='0-958', geo='US-ME-500')
#r.get_csv(q='python,php')
#r.get_csv(q='cat,mouse,dog')



