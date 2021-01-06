from urllib import parse
from dns import resolver, reversename
from datetime import datetime
from bs4 import BeautifulSoup
from rblwatch import RBLSearch
from random import choice
import string
import tldextract
import re
import ipaddress
import requests
import statistics
import os

FPATH = 'lib/file/'
FPATH = 'file/'
def start_url(url):
    """Split URL into: protocol, host, path, params, query and fragment."""
    #if not parse.urlparse(url.strip()).scheme:
     #   url = 'http://' + url
    protocol, host, path, params, query, fragment = parse.urlparse(url.strip())

    result = {
        'url': host + path + params + query + fragment,
        'protocol': protocol,
        'host': host,
        'path': path,
        'params': params,
        'query': query,
        'fragment': fragment
    }
    return result

def count(text, character):
    """Return the amount of certain character in the text."""
    return text.count(character)

def length(text):
    """Return the length of a string."""
    return len(text)


def count_tld(text):
    """Return amount of Top-Level Domains (TLD) present in the URL."""
    file = open(FPATH + 'tlds.txt', 'r')
    count = 0
    pattern = re.compile("[a-zA-Z0-9.]")
    for line in file:
        i = (text.lower().strip()).find(line.strip())
        while i > -1:
            if ((i + len(line) - 1) >= len(text)) or not pattern.match(text[i + len(line) - 1]):
                count += 1
                #print(pattern.match(text[i + len(line) - 1]))
            i = text.find(line.strip(), i + 1)
    file.close()
    return count

def count_ld(text):
    result = len(text.split("."))
    if result > 3:
        return 3
    return result

def split_dot_count(text):
    result = len(text.split("."))
    return result
def count_redirects(url):
    """Return the number of redirects in a URL."""
    try:
        response = requests.get(url, timeout=3)
        if response.history:
            return len(response.history)
        else:
            return 0
    except Exception:
        return '?'

def read_file(archive):
    """Read the file with the URLs."""
    with open(archive, 'r') as f:
        urls = ([line.rstrip() for line in f])
        return urls
def check_protocol(url):
    if "https" in url:
        return 1
    elif "http" in url:
        return 1
    return 0

def parse_url(fqdn):
    return tldextract.extract(fqdn)

def term_extract(text):

    dictionary = set(open(FPATH + 'word/all_tr','r').read().lower().split())
    max_len = max(map(len, dictionary)) #longest word in the set of words
    #text += '-'+text[::-1] #append the reverse of the text to itself

    words_found = [] #set of words found, starts empty
    size = 0
    for i in range(len(text)): #for each possible starting position in the corpus
        chunk = text[i:i+max_len+1] #chunk that is the size of the longest word
        for j in range(1,len(chunk)+1): #loop to check each possible subchunk
            word = chunk[:j] #subchunk
            #print(word)
            if word in dictionary  : #constant time hash lookup if it's in dictionary
                words_found.append(word) # add to set of words
                words_found.sort
                size = len(words_found)
                if size > 1 and words_found[size-2] in word:
                    words_found.pop(size-2)
                    size = len(words_found)
                if size > 1 and  word in words_found[size-2] :
                    words_found.pop(size-1)

#    print(words_found)
    return len(words_found)

def getfreeurl(URL):
    url = start_url(URL)
    info = parse_url(URL)
    freeurl = str(info.subdomain) + str(url['path'] )+ str(url['query'])
    return freeurl

def getrdn(url):
    info = parse_url(url)
    rdn = info.registered_domain
    return rdn

def getmld(url):
    info = parse_url(url)
    mld = info.domain
    return mld



def main(URL):
    url = start_url(URL)
    #print(url)
    #print("length of URL", len(url['url']))
    info = parse_url(URL)
    #print(info.registered_domain)
    #print(info.domain)
    #print(info.subdomain)
    #print("length of URL:", len(URL))    #URL
    #dot_url = str(count(info.subdomain + info._fields, '.'))
    #print(dot_url)
    #print(split_dot_count(info.suffix))
    #print(info._fields)

    print("http:",check_protocol(url['protocol']))
    freeurl = str(info.subdomain) + str(url['path'] )+ str(url['query'])
    term = str(info.fqdn) + str(url['path'] )+ str(url['query'])
    dot_url = count(getfreeurl(URL), ".")
    print("count of dot in freeurl:",dot_url)
    print("domain level:",count_ld(url['host']))
    print("length of MLD:",len(info.domain)) #MLD LENGTH
    print("length of FQDN:",len(info.fqdn)) #FQDN LENGTH
    print("length of RDN:",len(info.registered_domain)) #RDN LENGTH
    print("count of term:", term_extract(term))
    print("count of term:", term_extract(info.domain))
#main(URL)
