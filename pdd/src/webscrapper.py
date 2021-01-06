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
        #print(i)
        if dn.registered_domain == domainName:
            inter.append(i)
        else:
            exter.append(i)

    #print("\n\n\n\ninternal", inter,"\n\n\n\nexternal",exter)

# def chainurl(start, land, chain):
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
    #print("\n\n\n\ntitle:", data)
def web_scrapping(url, driver):
    try:
        #original_stdout = sys.stdout # Save a reference to the original standard output

        logged = []
        href = []
        img = []
        iframe = []
        _input = []
        title = []
        text = []
        chain = []
        flag = 0

 #       options = Options()
  #      options.headless = True

   #     driver = webdriver.Firefox(options=options)# Firefox(options=options)
        #time.sleep(0.8)
        #print("passed")
        #driver.get(url)
#        print(url)

#        with open('file/logged.txt', 'w') as f:
        #sys.stdout = f # Change the standard output to the file we created.
        #driver = webdriver.Firefox(executable_path="/home/mo/.local/bin/geckodriver")

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

            #print(i['name'])
        #sys.stdout = original_stdout # Reset the standard output to its original value
#        with open('file/href.txt', 'w') as f:
        #sys.stdout = f # Change the standard output to the file we created.
        #print("HREF Links:")
        lnks=driver.find_elements_by_tag_name("a")
        # traverse list
        for lnk in lnks:
           # get_attribute() to get all href
            if lnk.get_attribute("href") is not None:
                href.append(lnk.get_attribute("href"))
#                   f.write(lnk.get_attribute("href"))
#                  f.write("\n")

           #print(lnk.get_attribute("href"))
#            print("href Links:")
        #sys.stdout = original_stdout # Reset the standard output to its original value

#        with open('file/img.txt', 'w') as f:
       # sys.stdout = f # Change the standard output to the file we created.

        #print("HREF Links:")
        lnks=driver.find_elements_by_tag_name("img")
        # traverse list
        for lnk in lnks:
           # get_attribute() to get all href
            if lnk.get_attribute("src") is not None:
                img.append(lnk.get_attribute("src"))
#                    f.write(lnk.get_attribute("src"))
#                    f.write("\n")

#           print("img Links:")
           #print(lnk.get_attribute("src"))
      #  sys.stdout = original_stdout # Reset the standard output to its original value

#        with open('file/iframe.txt', 'w') as f:
     #   sys.stdout = f # Change the standard output to the file we created.

        #print("HREF Links:")
        lnks=driver.find_elements_by_tag_name("iframe")
        #print(lnks)
        # traverse list
        for lnk in lnks:
           # get_attribute() to get all href
            if lnk.get_attribute("src") is not None:
                iframe.append(lnk.get_attribute("src"))
#                    f.write(lnk.get_attribute("src"))
#                    f.write("\n")
#          print("iframe Links:")

           #print(lnk.get_attribute("src"))
    #    sys.stdout = original_stdout # Reset the standard output to its original value

#        with open('file/input.txt', 'w') as f:
   #     sys.stdout = f # Change the standard output to the file we created.

        #print("HREF Links:")
        lnks=driver.find_elements_by_tag_name("input")
        # traverse list
        for lnk in lnks:
           # get_attribute() to get all href
            if lnk.get_attribute("type") is not None:
                _input.append(lnk.get_attribute("type"))
#                    f.write(lnk.get_attribute("type"))
#                    f.write("\n")
#         print("input Links:")

           #print(lnk.get_attribute("type"))
  #      sys.stdout = original_stdout # Reset the standard output to its original value

#        with open('file/title.txt', 'w') as f:
 #       sys.stdout = f # Change the standard output to the file we created.
        #print("Title:")
          # Getting current URL source code
        get_title = driver.title

        # Printing the title of this URL
        title.append(get_title)
#            f.write(get_title)
        #f.write("\n")
#        print("title Links:")

        #print(get_title)
 #       sys.stdout = original_stdout # Reset the standard output to its original value

#        with open('file/text.txt', 'w') as f:
        #sys.stdout = f # Change the standard output to the file we created.
        el = driver.find_element_by_tag_name('body')
        text.append(el.text)
    #    driver.quit()
#            f.write(el.text)
        #print(el.text)
        #print("text Links:")
#            driver.quit()

        return chain, logged, href, img, iframe, _input, title, text, 1
    except Exception as e:
#        sys.stdout = original_stdout # Reset the standard output to its original value
        print("webscrapping error")
        #print(e)
        trace_back = sys.exc_info()[2]
        line = trace_back.tb_lineno
        print(format(line),e)
    #    driver.quit()

#    sys.stdout = original_stdout # Reset the standard output to its original value
#    driver.quit()
   # driver.quit()
    return chain, logged, href, img, iframe, _input, title, text, 0




#url ='https://tls.tc/yplbfsgn'
#url = 'http://apple-iforget.com'
#options = Options()
#options.headless = True
#driver = webdriver.Firefox(options=options)# Firefox(options=options)
#web_scrapping(url,driver)
#driver.get(url)
#url = 'https://www.google.com'
#driver.get(url)
#driver.quit()
