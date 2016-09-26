from bs4 import BeautifulSoup
import urllib2
import re
try:
    import simplejson as json
except:
    import json

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import pymongo

# Connection to Mongo DB
try:
    conn=pymongo.MongoClient()
    print "Connected successfully!!!"
except pymongo.errors.ConnectionFailure, e:
   print "Could not connect to MongoDB: %s" % e 

db = conn.bibleDict

bdictlist = db.bdictlist


def get_links():
    all_links = []
    try:
        url = "http://eastonsbibledictionary.org/index.php"
        content = urllib2.urlopen(url).read()
        soup = BeautifulSoup(content, "html.parser")
        links = soup.select("li.IndexLevel2 a")
        for link in links:
            all_links.append('http://eastonsbibledictionary.org/' + link['href'])
    except:
        print 'ERROR Fetching Links'
    return all_links

def get_info():
    link_list = get_links()
    for indexx in range(len(link_list)):
        data_dump = {}
        url = str(link_list[indexx])
        content = urllib2.urlopen(url).read()
        soup = BeautifulSoup(content, "html.parser")
        title = soup.select("div #bookcontent h2")
        paragraphs = soup.select("div #bookcontent p")
        # remove html tags with regex
        title = re.sub(r'(<script(\s|\S)*?<\/script>)|(<style(\s|\S)*?<\/style>)|(<!--(\s|\S)*?-->)|(<\/?(\s|\S)*?>)', '', str(title[0]))
        print title, '\n '
        paragraphs_clean = []
        for index in range(len(paragraphs)):
        # remove html tags with regex
            regex = re.sub(r'(<script(\s|\S)*?<\/script>)|(<style(\s|\S)*?<\/style>)|(<!--(\s|\S)*?-->)|(<\/?(\s|\S)*?>)', '', str(paragraphs[index]))
            print regex
            if regex != ' ':
                paragraphs_clean.append(str(regex))
        data_dump['title'] = title
        data_dump['info'] = paragraphs_clean
        bdictlist.insert(data_dump)

if __name__ == '__main__':
    get_info()
