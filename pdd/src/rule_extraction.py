#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tqdm import tqdm
import sys
from traceback import format_exc
import threading
from ns_log import NsLog
from url_rules import url_rules
from active_rules import active_rules
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
#from selenium.webdriver.chrome.options import Options
from joblib import Parallel, delayed



class rule_extraction:

    def __init__(self):
        self.logger = NsLog("log")
        self.url_rules_o = url_rules()
        self.active_rules_o = active_rules()
        self.path_phish = "phish/lib/"

    def thread_extraction(self, line, domain_features):
        try:
            options = Options()
            options.headless = True

            #chrome_options = Options()
    #chrome_options.add_argument("--disable-extensions")
    #chrome_options.add_argument("--disable-gpu")
    #chrome_options.add_argument("--no-sandbox") # linux only
            #chrome_options.add_argument("--headless")

            #driver_path = # geckodriver'ın path'i girilebilir
            driver = webdriver.Firefox(options=options)#, executable_path=driver_path)
            #driver = webdriver.Chrome(options=chrome_options)#,executable_path=driver_path)# Firefox(options=options)
#            if "https://" in line['url']:
#                driver.get(line['url'])
#            elif "http://" in line['url']:
#                driver.get(line['url'])
#            else:
#                driver.get("http://"+ line['url'])
            driver.get(line['url'])


            info = line

     #  info['mail'] = 'whoisden cekilecek'
     #nlp_info, url_features = self.url_rules_o.rules_main(info['domain'],
            nlp_info, url_features = self.url_rules_o.phish_rules_main(info['domain'],
                                                                 info['tld'],
                                                                 info['subdomain'],
                                                                 info['path'],
                                                                 info['words_raw'],
                                                                 info['url'],
                                                                 driver)  # url kurallarin calistigi yer

            info['nlp_info'] = nlp_info
            info['nlp_info']['words_raw'] = info['words_raw']
            info.pop("words_raw", None)
            #print(url_features)
            outputDict = {}

    #        info['dns_records'] = domain_info

            outputDict['info'] = info
            outputDict['url_features'] = url_features


    #        outputDict['dns_features'] = dns_features

            domain_features.append(outputDict)
            driver.quit()
            #driver.close()
            return domain_features
        except Exception as e:

            #        sys.stdout = original_stdout # Reset the standard output to its original value
            #print(e)
            driver.quit()
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            print(format(line),e)
            return False



    def extraction(self, parsed_domains):

        #options = Options()
        #options.headless = True

        #driver = webdriver.Firefox(options=options)# Firefox(options=options)

        self.logger.info("rule_extraction.extraction() is running")

        domain_features = []
        try:
            #_iter = iter(tqdm(parsed_domains))
            for line in tqdm(parsed_domains):# tqdm(parsed_domains):  # self.bar(parsed_domains)
            #Parallel(n_jobs=-1)(delayed(self.thread_extraction(line, domain_features))(line) for line in tqdm(parsed_domains))
                flag = self.thread_extraction(line, domain_features)
                if flag is False:
                    continue
#                info = line
#
#               #  info['mail'] = 'whoisden cekilecek'
#               #nlp_info, url_features = self.url_rules_o.rules_main(info['domain'],
#                nlp_info, url_features = self.url_rules_o.phish_rules_main(info['domain'],
#                                                                     info['tld'],
#                                                                     info['subdomain'],
#                                                                     info['path'],
#                                                                     info['words_raw'],
#                                                                     info['url'],
#                                                                     driver)  # url kurallarin calistigi yer
#
#                info['nlp_info'] = nlp_info
#                info['nlp_info']['words_raw'] = info['words_raw']
#                info.pop("words_raw", None)
#                #print(url_features)
#                outputDict = {}
#
#              #  info['dns_records'] = domain_info
#
#                outputDict['info'] = info
#                outputDict['url_features'] = url_features
#
#              #  outputDict['dns_features'] = dns_features
#
#                domain_features.append(outputDict)

            #domain_features = self.active_rules_o.goog_safe_browsing(domain_features)  # active kuralların calıtıı yer
        except:
            self.logger.error("Error : {0}".format(format_exc()))
        #driver.quit()
        return domain_features
