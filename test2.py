import lxml.html
from urllib.request import urlopen
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
import re
import sqlite3
from sqlite3 import Error
import time


l=[]
re1='.*?'   # Non-greedy match on filler
re2='(\\/www\\'+'\\.com)'  # Unix Path 1
re3='(^/)'   # Any Single Character 1
re4='/$'
re5='.html$'


rd = re.compile(re3,re.IGNORECASE|re.DOTALL)
rk=re.compile(re3+re5)
rf=re.compile(re3+re4)
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
    i=0
    connection = urlopen(txt)

    dom =  lxml.html.fromstring(connection.read())

    run.s=txt
    con = sql_connection()
    sql_table(con)
    for link in dom.xpath('//a/@href'): # select the url in href for all a tags(links)
        if(link not in l and txt +link not in l):
            if(rg.search(link)!=None ):
                l.append(link)
            if(rd.search(link)!=None ):
                l.append(txt +link)

    for i in range(len(l)):
        insert_data(con,i,l[i])
        i+=1
    x=print_data(con)
    return i,loop.c
run.s=''
def loop():
    loop.c+=1
    j=0
    con = sql_connection()
    if(loop.k>=len(l)):
        exit()
    while(loop.k<=len(l)):
        time.sleep(6)
        print("l[loop.k]={}".format(l[loop.k]))
        print("s={}".format(run.s))
        try:
            connection = urlopen(l[loop.k])

            dom =  lxml.html.fromstring(connection.read())
            for link in dom.xpath('//a/@href'): # select the url in href for all a tags(links)
                if(link not in l and run.s+link not in l):
                    if(rg.search(link)!=None ):
                        l.append(link)
                        print("link={}".format(link))
                        insert_data(con,len(l),link)
                        j+=1
                    if(rd.search(link)!=None ):
                        l.append(run.s +link)
                        insert_data(con,len(l),run.s+link)
                        print("s+link={}".format(run.s+link))
                        j+=1

            loop.k+=1
            q=print_data(con)
            return j,loop.c
        except urllib2.HTTPError as e:
            print("error [%s]: " % (l[loop.k]))
            loop.k+=1

loop.k=1
loop.c=0


def data(txt):
    z=run(txt)
    return z



