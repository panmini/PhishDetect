from gensim.corpora import Dictionary
from itertools import combinations

from function import *
from webscrapper import *


import statistics

def binaryfeatures(rdn,title):
    for word in rdn:
        if word in title:
            return 1
        else:
            return 0
def term_extraction( URL):
    from url_rules import url_rules

    parser = domain_parser()
    line = URL.strip().replace('"', "").replace("'",'')
    extracted_domain = tldextract.extract(line)
    tmp = line[line.find(extracted_domain.suffix):len(line)]  # tld sonraki ilk / e gore parse --> path
    pth = tmp.partition("/")

    words_raw = parser.words_raw_extraction(extracted_domain.domain, extracted_domain.subdomain, pth[2])
    nlp = url_rules()

    result_nlp = nlp.nlp_features(words_raw)
    return result_nlp

def print_wo(line,coma):
        print(line,coma,end = " ")

def f1_8feature(feature_1, URL):

    url = start_url(URL)
    info = parse_url(URL)
    feature_1.append(check_protocol(url['protocol']))
    freeurl = str(info.subdomain) + str(url['path'] )+ str(url['query'])
    term = str(info.fqdn) + str(url['path'] )+ str(url['query'])
    dot_url = count(getfreeurl(URL), ".")
    feature_1.append(dot_url)
    feature_1.append(count_ld(url['host']))
    feature_1.append(len(info.domain))
    feature_1.append(len(info.fqdn))
    feature_1.append(len(info.registered_domain))

def mean_median_stdev(feature_1, data):
    if len(data) > 0:
        feature_1.append(statistics.mean(data))
        feature_1.append(statistics.median(data))
        if len(data)>1:
            feature_1.append(statistics.stdev(data))
    else:
        feature_1.append(0)
        feature_1.append(0)
        feature_1.append(0)

def f1_3_8feature(feature_1, links):

    list_dl             =[]
    list_len_mld        =[]
    list_len_fqdn       =[]
    list_rdn            =[]
    list_nlp            =[]
#    list_c_url          =[]
#    list_c_mld          =[]
    for data in links:
        rules = term_extraction(data)['features']
        url = start_url(data)
        info = parse_url(data)
        term = str(info.fqdn) + str(url['path'] )+ str(url['query'])
        list_dl.append(count_ld(url['host']))
        list_len_mld.append(len(info.domain))
        list_len_fqdn.append(len(info.fqdn))
        list_rdn.append(len(info.registered_domain))

        #print(len(url_rules_o.term_extraction(URL)['features']))
        nlp = []
        for i in rules:
            nlp.append(rules[i])
        list_nlp.append(nlp)
#        list_c_url.append(term_extract(term))
#        list_c_mld.append(term_extract(info.domain))
    mean_median_stdev(feature_1, list_dl)
    mean_median_stdev(feature_1, list_len_mld)
    mean_median_stdev(feature_1, list_len_fqdn)
    mean_median_stdev(feature_1, list_rdn)
    if list_nlp:
        for i in range(len(list_nlp[0])):
            calc = []
            for j in list_nlp:
                calc.append(j[0])
            mean_median_stdev(feature_1, calc)
    else:
        mean_median_stdev(feature_1, [0,0])



def phish_extraction(url, driver):

    try:
        result = {}
        interhref=[]
        exterhref=[]
        interlog=[]
        exterlog=[]
        #chain=[]
        title=[]
        text=[]
        chain, logged, href, img, iframe, _input, title, text, flag = web_scrapping(url, driver)
        #print(chain, logged, href, img, iframe, _input, title, text, flag)
        if type(chain) is list and len(chain) > 0:
            starturl=chain[0]
            landurl=chain[-1]
        else:
            starturl=chain
            landurl=chain



        if flag == 0:
            return False
        interandextern(landurl,interhref,exterhref,href)
        interandextern(landurl,interlog,exterlog,logged)

        feature_1 = []
        f1_8feature(feature_1, starturl)
        f1_8feature(feature_1, landurl)
        f1_3_8feature(feature_1, interhref)
        f1_3_8feature(feature_1, interlog)
        f1_3_8feature(feature_1, exterlog)
        f1_3_8feature(feature_1, exterhref)
     #
        #Feature 2 calculating
     #
        start=list(getfreeurl(starturl))
        land=list(getfreeurl(landurl))
        startrdn=list(getrdn(starturl))
        landrdn=list(getrdn(landurl))
        intlog=[]
        intlink=[]
        intrdn=[]
        extrdn=[]
        extlog=[]
        extlink=[]

        for var in interhref:
           intlink.append(getfreeurl(var))
           intrdn.append(getrdn(var))

        for var in interlog:
           intlog.append(getfreeurl(var))
           intrdn.append(getrdn(var))

        for var in exterhref:
           extlink.append(getfreeurl(var))

        for var in exterlog:
           extlog.append(getfreeurl(var))
           extrdn.append(getrdn(var))

        # you can use any corpus, this is just illustratory
        texts = [
            text,title,start,land,startrdn,landrdn,intlog,intlink,intrdn,extrdn,extlog,extlink
        ]
        dictionary = Dictionary(texts)
        corpus = [dictionary.doc2bow(text) for text in texts]
        import numpy
        numpy.random.seed(1) # setting random seed to get the same results each time.

        from gensim.models import ldamodel
        model = ldamodel.LdaModel(corpus, id2word=dictionary, num_topics=2)#, minimum_probability=1e-8)
        model.show_topics()
        #print_wo("\n")

        from gensim.matutils import hellinger
        feature_2 = []
        for combo in combinations(texts, 2):  # 2 for pairs, 3 for triplets, etc
        ## we can now get the LDA topic distributions for these
            bow0 = model.id2word.doc2bow(combo[0])
            bow1 = model.id2word.doc2bow(combo[1])

            lda_bow0 = model[bow0]
            lda_bow1 = model[bow1]

            #print_wo("Distance #",count,":",hellinger(lda_bow0,lda_bow1))
            feature_2.append(hellinger(lda_bow0,lda_bow1))
            #print_wo(hellinger(lda_bow0,lda_bow1),",")
        #for i in range(16):
        #    print_wo(i,":",dictionary.get(i))
        # now let's make these into a bag of words format
        #

        feature_2.append(binaryfeatures(intrdn,title))
        feature_2.append(binaryfeatures(extrdn,title))

               ##
        # f3 features calculeting
        ##
        feature_3n4 = []
        startmld = getmld(starturl)
        landmld = getmld(landurl)

        mlds = [startmld,landmld]

        startrdn = getrdn(starturl)
        landrdn = getrdn(landurl)

        rdns = [startmld,landmld]

        compare = [text,title,intlog,extlog,intlink,extlink]

        for i in range(2):
            for j in range(6):
                if mlds[i] in compare[j]:
                    feature_3n4.append(1)
                else:
                    feature_3n4.append(0)
        compare = [title,intlog,extlog,intlink,extlink]
        compare = " ".join(str(x) for x in compare)
        for i in range(2):
            for j in range(5):
                if compare[j] in mlds[i]:
                    feature_3n4.append(1)
                else:
                    feature_3n4.append(0)
        for m in range(2):
            for n in range(5):
                if compare[j] in rdns[i] and compare[j] not in mlds[i]:
                    feature_3n4.append(1)
                else:
                    feature_3n4.append(0)


        ##
        # f3 features calculeted
        ##

        ##
        # f4 features calculeting
        ##

        if getrdn(starturl) in getrdn(landurl):
            feature_3n4.append(1)
        else:
            feature_3n4.append(0)
        if len(chain) > 2:
            feature_3n4.append(len(chain)-2)
        else:
            feature_3n4.append(0)
        feature_3n4.append(len(interlog))
        feature_3n4.append(len(interhref))

        feature_3n4.append(len(exterlog))
        feature_3n4.append(len(exterhref))

        count = 0
        for comp in interlog:
            if getrdn(starturl) in getrdn(comp):
                count += 1
        feature_3n4.append(count)


        count = 0
        for comp in interhref:
            if getrdn(starturl) in getrdn(comp):
                count += 1
        feature_3n4.append(count)

        count = 0
        if len(chain) > 2 :
            for comp in chain[1:len(chain)-1] :#check later
                if getrdn(starturl) in getrdn(comp):
                    count += 1
        feature_3n4.append(count)


        count = 0
        if len(chain) > 2 :
            for comp in chain[1:len(chain)-1] :#check later
                if getrdn(landurl) in getrdn(comp):
                    count += 1
        feature_3n4.append(count)


        count = 0
        for comp in exterlog :#check later
            if getrdn(starturl) in getrdn(comp):
                count += 1
        feature_3n4.append(count)

        count = 0
        for comp in exterlog : #check later
            if getrdn(starturl) in getrdn(comp):
                count += 1
        feature_3n4.append(count)

        ##
        # f4 features calculed
        ##
        ##
        # f5 features calculation
        ##
        feature_5 = []
        data = _input#file.read()

        feature_5.append(len(data))

        data = img# file.read()
        feature_5.append(len(data))


        data = iframe# file.read()
        feature_5.append(len(data))


        data = text#file.read()
        feature_5.append(len(data))


        data = title# file.read()
        feature_5.append(len(data))
        res = feature_1 + feature_2 + feature_3n4 + feature_5

        if flag == 1:
            for i in range(len(res)) :
                if res[i] is not None:
                    result[str(i)] = res[i]
                else:
                    result[str(i)] = 0
        else:
            return False
    except Exception as e:
        #print("extraction error",e)
        trace_back = sys.exc_info()[2]
        line = trace_back.tb_lineno
        print(format(line),e)

        if flag == 1:
            return False
        else:
            return False
    return result
#url ='http://itaacesslinkregulari-com.umbler.net/'
##url = 'http://apple-iforget.com'
#options = Options()
#options.headless = True
#driver = webdriver.Firefox(options=options)# Firefox(options=options)
#web_scrapping(url,driver)
#driver.get(url)
#print(phish_extraction(url,driver))
##url = 'https://www.google.com'
##driver.get(url)
#driver.quit()
