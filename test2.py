import lxml.html
from urllib.request import urlopen
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
import re
import sqlite3
from sqlite3 import Error



l=[]
re1='.*?'   # Non-greedy match on filler
re2='(\\/www\\'+'\\.com)'  # Unix Path 1
re3='(^/)'   # Any Single Character 1

rd = re.compile(re3,re.IGNORECASE|re.DOTALL)

rg = re.compile(re1+re2,re.IGNORECASE|re.DOTALL)

def sql_connection():
 
    try:
 
        con = sqlite3.connect('mydatabase.db')
 
        return con
 
    except Error:
 
        print(Error)



'''for i in l:
    c = urlopen(i)

    d=  lxml.html.fromstring(c.read())

    for j in d.xpath('//a/@href'): # select the url in href for all a tags(links)
        if(rg.search(j)!=None):
            l.append(j)
            print(j)
        if(rd.search(j)!=None):
            l.append('https://www.nytimes.com' +j)
            print('https://www.nytimes.com' +j)'''


 
def sql_table(con):
 
    cursorObj = con.cursor()
 
    cursorObj.execute("CREATE TABLE  if not exists url(id integer , url text)")
 
    con.commit()
 
 
def insert_data(con,i,url):
    cursorObj = con.cursor()
    data = [(i,url)]
    cursorObj.executemany("INSERT INTO url VALUES(?, ?)", data)
    con.commit()

def print_data(con):
    d=[]
    cursorObj=con.cursor()
    cursorObj.execute('SELECT * FROM url ')
    c=cursorObj.fetchall()
    for j in c:
        d.append(j)
    return d

def row_count(con):
    cursorObj = con.cursor()
    rows = cursorObj.fetchall()
    return len(rows)
    

def run(txt):


    connection = urlopen(txt)

    dom =  lxml.html.fromstring(connection.read())


    con = sql_connection()
    sql_table(con)
    for link in dom.xpath('//a/@href'): # select the url in href for all a tags(links)
        if(rg.search(link)!=None):
            l.append(link)
        if(rd.search(link)!=None):
            l.append(txt +link)

    for i in range(len(l)):
        insert_data(con,i,l[i])

    x=print_data(con)
    return x

def loop():
    con = sql_connection()
    while(loop.k<=len(l)):
        print(l[loop.k])
        try:
            connection = urlopen(l[loop.k])

            dom =  lxml.html.fromstring(connection.read())
            for link in dom.xpath('//a/@href'): # select the url in href for all a tags(links)
                if(rg.search(link)!=None):
                    l.append(link)
                    insert_data(con,len(l),link)
                if(rd.search(link)!=None):
                    l.append(l[loop.k] +link)
                    insert_data(con,len(l),l[loop.k]+link)
            
            loop.k+=1
            q=print_data(con)
            return q
        except urllib2.HTTPError as e:
            print("error [%s]: " % (l[loop.k]))
            loop.k+=1


loop.k=1

 
def data(txt):
    z=run(txt)
    return z


