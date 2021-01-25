from selenium import webdriver
from selenium.webdriver.common.by import By
from Naked.toolshed.shell import execute_js, muterun_js
from selenium.webdriver.firefox.options import Options
import subprocess
import time
import json
import sys
import tldextract

#url ='https://www.google.com'
#url ='https://www.w3schools.com/tags/tag_iframe.ASP'
#url ='https://tls.tc/yplbfsgn'

def interandextern( url, inter, exter,links):#files):

    #file1 = open(files, 'r')
    lines = links# file1.readlines()
    info = tldextract.extract(url)
    domainName=info.registered_domain #RDN

    for i in lines:
        if isinstance(i, str):                   #could be try
            dn=tldextract.extract(i)
        else:
            continue
        if dn.registered_domain == domainName:
            inter.append(i)
        else:
            exter.append(i)

def chainurl(chain,links):

    #file1 = open("file/slr.txt", 'r')
    lines = links#file1.readlines()
    for i in lines:
        chain.append(i)
    start = chain[0]
    land =  chain[-1]
    #print("\n\n\n\nstart:", start,"\n\n\n\nlanding",land,"\n\n\n\nchain",chain[1:-1])

def loaddata(data, filename):
    with open(filename, "r") as f:
        for line in f:
            data.extend(line.split())
def web_scrapping(url, driver):
    try:

        logged = []
        href = []
        img = []
        iframe = []
        _input = []
        title = []
        text = []
        chain = []
        flag = 0

       # script = """
       # var resources = window.performance.getEntriesByType(\"resource\");
       # resources.forEach(function (resource) {
       #     console.log(resource.name);
       # });
       # return resources[0].name;
       #     """
        resources = driver.execute_script("return window.performance.getEntriesByType(\"resource\")")
        #element = driver.find_element_by_name('resources')

        #result = execute_js('redirect.js',url)
        proc = subprocess.Popen(['node', 'redirect.js',url], stdout=subprocess.PIPE )#PIPE)
        output = proc.stdout.read().decode('utf-8')
        chain = output.splitlines()
        #print("redirect Links:")
        #print("Logged Links:")
        data = json.dumps(resources)
        final = json.loads(data)
        for i in final:
            if i['name'] is not None:
                logged.append(i['name'])
#                    f.write(i['name'])
#                    f.write("\n")

        lnks=driver.find_elements_by_tag_name("a")
        # traverse list
        for lnk in lnks:
           # get_attribute() to get all href
            if lnk.get_attribute("href") is not None:
                href.append(lnk.get_attribute("href"))
        lnks=driver.find_elements_by_tag_name("img")
        # traverse list
        for lnk in lnks:
           # get_attribute() to get all href
            if lnk.get_attribute("src") is not None:
                img.append(lnk.get_attribute("src"))
#                    f.write(lnk.get_attribute("src"))
#                    f.write("\n")

        lnks=driver.find_elements_by_tag_name("iframe")
        #print(lnks)
        # traverse list
        for lnk in lnks:
           # get_attribute() to get all href
            if lnk.get_attribute("src") is not None:
                iframe.append(lnk.get_attribute("src"))
        lnks=driver.find_elements_by_tag_name("input")
        # traverse list
        for lnk in lnks:
           # get_attribute() to get all href
            if lnk.get_attribute("type") is not None:
                _input.append(lnk.get_attribute("type"))
          # Getting current URL source code
        get_title = driver.title

        # Printing the title of this URL
        title.append(get_title)
        el = driver.find_element_by_tag_name('body')
        text.append(el.text)

        return chain, logged, href, img, iframe, _input, title, text, 1
    except Exception as e:
        print("webscrapping error")
        #print(e)
        trace_back = sys.exc_info()[2]
        line = trace_back.tb_lineno
        print(format(line),e)

    return chain, logged, href, img, iframe, _input, title, text, 0

