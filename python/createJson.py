import requests
import re
import httplib2
from bs4 import BeautifulSoup, SoupStrainer
import html5lib
from html5lib import sanitizer
from html5lib import treebuilders
import urllib
import time
import json
import sys
import random


cisco_url="http://www.cisco.com/web/about/ac50/ac207/crc_new/university/publications.html"

cisco_request= requests.get(cisco_url)

urls_ieee_download=[]
urls_download=[]
url_to_ieee=[]
url_to_acm=[]
list_href=[]
list_json_to_solr=[]
articles_in_html=[]

soup = BeautifulSoup(cisco_request.text, "html5lib")

for tag in soup.findAll('a', href=True):
    list_href.append(tag['href'])


'''Create two lists of URLs for IEEE and ACM papers'''

for lis in list_href:
    match=re.search("ieeexplore.ieee.org/xpl/articleDetails.jsp", lis)
    match_acm=re.search("http://dl.acm.org/citation.cfm", lis)
    if match:
        url_to_ieee.append(lis)
    if match_acm:
        url_to_acm.append(lis)


'''Creates ans saves json file for ACM papers'''

for url in url_to_acm:
    time.sleep(15)
    request=requests.get(url)
    soup_acm=BeautifulSoup(request.text,"html5lib")
    acm_authors=soup_acm.find('meta', {"name":"citation_authors"})['content']
    acm_date=soup_acm.find('meta', {"name":"citation_date"})['content']
    acm_title=soup_acm.find('meta', {"name":"citation_title"})['content']
    acm_id=soup_acm.find('meta', {"name":"citation_isbn"})
    acm_publisher=soup_acm.find('meta', {"name":"citation_publisher"})['content']
    acm_keywords=soup_acm.find('meta', {"name":"citation_keywords"})
    if acm_keywords is None:
        acm_keywords=''
    else:
        acm_keywords=acm_keywords['content']

    '''Set unique ID for the paper to be found by Solr'''

    if acm_id is None:
        acm_id=soup_acm.find('meta', {"name":"citation_issn"})
        if acm_id is None:
            acm_id=str(random.randint(0, 1000000))
        else:
            acm_id=acm_id['content']
    else:
        acm_id=acm_id['content']
    paper_dict={"id":acm_id,
                "name":acm_title,
                "series_t":acm_date,
                "author":acm_authors,
                "inStock":url,
                "genre_s":acm_publisher,
                "pages_i":acm_keywords}
    list_json_to_solr.append(paper_dict)
    print paper_dict

outfile="acm_papers.json"

with open(outfile, 'w') as outfile:
  json.dump(list_json_to_solr, outfile)

'''Creates ans saves json file for IEEE papers'''

for url in url_to_ieee:
    request=requests.get(url)
    soup_ieee=BeautifulSoup(request.text,"html5lib")
    ieee_keywords=soup_ieee.find('meta', {"name":"citation_keywords"})
    if ieee_keywords is None:
        ieee_keywords=''
    else:
        ieee_keywords=ieee_keywords['content']
    ieee_content=soup_ieee.find("div",{"class":"article"}).get_text()
    ieee_authors=soup_ieee.findAll('meta', {"name":"citation_author"})
    author=''
    for ieee_author in ieee_authors:
        author=author+ieee_author['content']
    ieee_publisher=soup_ieee.find('meta',{"name":"citation_publisher"})['content']
    ieee_date=soup_ieee.find('meta', {"name":"citation_date"})['content']
    ieee_title=soup_ieee.find('meta', {"name":"citation_title"})['content']
    ieee_id=soup_ieee.find('meta', {"name":"citation_isbn"})
    if ieee_id is None:
        ieee_id=soup_ieee.find('meta', {"name":"citation_issn"})
        if ieee_id is None:
            ieee_id=str(random.randint(0, 1000000))
        else:
            ieee_id=ieee_id['content']
    else:
        ieee_id=ieee_id['content']
    paper_dict={"id":ieee_id,
                "name":ieee_title,
                "cat":ieee_content,
                "series_t":ieee_date,
                "author":author,
                "manu":url,
                "genre_s":ieee_publisher,
                "features":ieee_keywords}
    list_json_to_solr.append(paper_dict)
    print paper_dict
print list_json_to_solr




#outfile="ieee_papers.json"
outfile='other_ieee.json'
with open(outfile, 'w') as outfile:
  json.dump(list_json_to_solr, outfile)

    	






