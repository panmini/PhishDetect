from selenium import webdriver
from selenium.webdriver.common.by import By
from Naked.toolshed.shell import execute_js, muterun_js
from selenium.webdriver.firefox.options import Options
import time
import json
import sys
import tldextract

#url ='https://www.google.com'
#url ='https://www.w3schools.com/tags/tag_iframe.ASP'
url ='https://tls.tc/yplbfsgn'

def interandextern( url, inter, exter,files):

    file1 = open(files, 'r')
    lines = file1.readlines()
    info = tldextract.extract(url)
    domainName=info.registered_domain #RDN

    for i in lines:
        if isinstance(i, str):                   #could be try
            dn=tldextract.extract(i)
        else:
            continue
        #print(i)
        if dn.registered_domain == domainName:
            inter.append(i)
        else:
            exter.append(i)

    #print("\n\n\n\ninternal", inter,"\n\n\n\nexternal",exter)

# def chainurl(start, land, chain):
def chainurl(chain):

    file1 = open("file/slr.txt", 'r')
    lines = file1.readlines()
    for i in lines:
        chain.append(i)
    start = chain[0]
    land =  chain[-1]
    #print("\n\n\n\nstart:", start,"\n\n\n\nlanding",land,"\n\n\n\nchain",chain[1:-1])

def loaddata(data, filename):
    with open(filename, "r") as f:
        for line in f:
            data.extend(line.split())
    #print("\n\n\n\ntitle:", data)
def web_scrapping(url):
    original_stdout = sys.stdout # Save a reference to the original standard output

    with open('file/logged.txt', 'w') as f:
        sys.stdout = f # Change the standard output to the file we created.
        #driver = webdriver.Firefox(executable_path="/home/mo/.local/bin/geckodriver")
        options = Options()
        options.headless = True

        driver = webdriver.Firefox(options=options)
        driver.get(url)
       # script = """
       # var resources = window.performance.getEntriesByType(\"resource\");
       # resources.forEach(function (resource) {
       #     console.log(resource.name);
       # });
       # return resources[0].name;
       #     """
        resources = driver.execute_script("return window.performance.getEntriesByType(\"resource\")")
        #element = driver.find_element_by_name('resources')
        result = execute_js('redirect.js',url)
        #print("Logged Links:")
        data = json.dumps(resources)
        final = json.loads(data)
        for i in final:
            print(i['name'])
        sys.stdout = original_stdout # Reset the standard output to its original value

    with open('file/href.txt', 'w') as f:
        sys.stdout = f # Change the standard output to the file we created.
        #print("HREF Links:")
        lnks=driver.find_elements_by_tag_name("a")
        # traverse list
        for lnk in lnks:
           # get_attribute() to get all href
           print(lnk.get_attribute("href"))
        sys.stdout = original_stdout # Reset the standard output to its original value

    with open('file/img.txt', 'w') as f:
        sys.stdout = f # Change the standard output to the file we created.

        #print("HREF Links:")
        lnks=driver.find_elements_by_tag_name("img")
        # traverse list
        for lnk in lnks:
           # get_attribute() to get all href
           print(lnk.get_attribute("src"))
        sys.stdout = original_stdout # Reset the standard output to its original value

    with open('file/iframe.txt', 'w') as f:
        sys.stdout = f # Change the standard output to the file we created.

        #print("HREF Links:")
        lnks=driver.find_elements_by_tag_name("iframe")
        # traverse list
        for lnk in lnks:
           # get_attribute() to get all href
           print(lnk.get_attribute("src"))
        sys.stdout = original_stdout # Reset the standard output to its original value

    with open('file/input.txt', 'w') as f:
        sys.stdout = f # Change the standard output to the file we created.

        #print("HREF Links:")
        lnks=driver.find_elements_by_tag_name("input")
        # traverse list
        for lnk in lnks:
           # get_attribute() to get all href
           print(lnk.get_attribute("type"))
        sys.stdout = original_stdout # Reset the standard output to its original value

    with open('file/title.txt', 'w') as f:
        sys.stdout = f # Change the standard output to the file we created.
        #print("Title:")
          # Getting current URL source code
        get_title = driver.title

        # Printing the title of this URL
        print(get_title)
        sys.stdout = original_stdout # Reset the standard output to its original value

    with open('file/text.txt', 'w') as f:
        sys.stdout = f # Change the standard output to the file we created.
        el = driver.find_element_by_tag_name('body')
        print(el.text)
        driver.quit()
        sys.stdout = original_stdout # Reset the standard output to its original value

#url ='https://tls.tc/yplbfsgn'
#phish_main(url)

