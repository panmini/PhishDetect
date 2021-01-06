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
def print_wo(line,coma):
        print(line,coma,end = " ")

def f1_8feature(feature_1, URL):

    url = start_url(URL)
    info = parse_url(URL)
    feature_1.append(check_protocol(url['protocol']))
    #print_wo(check_protocol(url['protocol']),",")
    freeurl = str(info.subdomain) + str(url['path'] )+ str(url['query'])
    term = str(info.fqdn) + str(url['path'] )+ str(url['query'])
    dot_url = count(getfreeurl(URL), ".")
    feature_1.append(dot_url)
    feature_1.append(count_ld(url['host']))
    feature_1.append(len(info.domain))
    feature_1.append(len(info.fqdn))
    feature_1.append(len(info.registered_domain))
#    print_wo(dot_url,",")
#    print_wo(count_ld(url['host']),",")
#    print_wo(len(info.domain),",") #MLD LENGTH
#    print_wo(len(info.fqdn),",") #FQDN LENGTH
#    print_wo(len(info.registered_domain),",") #RDN LENGTH
#    print_wo(term_extract(term),",")
#    print_wo(term_extract(info.domain),",")

def mean_median_stdev(feature_1, data):
    feature_1.append(statistics.mean(data))
    feature_1.append(statistics.mean(data))
    feature_1.append(statistics.mean(data))
    #print_wo(statistics.mean(data),",")
    #print_wo(statistics.median(data),",")
    #print_wo(statistics.stdev(data),",")
    #return statistics.mean(data), statistics.median(data), statistics.stdev(data)


def f1_3_8feature(feature_1, links):

    list_dl             =[]
    list_len_mld        =[]
    list_len_fqdn       =[]
    list_rdn            =[]
#    list_c_url          =[]
#    list_c_mld          =[]
    for data in links:
        url = start_url(data)
        info = parse_url(data)
        term = str(info.fqdn) + str(url['path'] )+ str(url['query'])
        list_dl.append(count_ld(url['host']))
        list_len_mld.append(len(info.domain))
        list_len_fqdn.append(len(info.fqdn))
        list_rdn.append(len(info.registered_domain))
#        list_c_url.append(term_extract(term))
#        list_c_mld.append(term_extract(info.domain))

    mean_median_stdev(feature_1, list_dl)
    mean_median_stdev(feature_1, list_len_mld)
    mean_median_stdev(feature_1, list_len_fqdn)
    mean_median_stdev(feature_1, list_rdn)
#    mean_median_stdev(list_c_url)
#    mean_median_stdev(list_c_mld)

#original_stdout = sys.stdout # Save a reference to the original standard output
#with open('file/dataset.csv', 'w') as f:

#    sys.stdout = f # Change the standard output to the file we created.
def phish_extraction():
    result = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0, '9': 0, '10': 0, '11': 0, '12': 0, '13': 0, '14': 0, '15': 0, '16': 0, '17': 0, '18': 0, '19': 0, '20': 0, '21': 0, '22': 0, '23': 0, '24': 0, '25': 0, '26': 0, '27': 0, '28': 0, '29': 0, '30': 0, '31': 0, '32': 0, '33': 0, '34': 0, '35': 0, '36': 0, '37': 0, '38': 0, '39': 0, '40': 0, '1': 0, '42': 0, '43': 0, '44': 0, '45': 0, '46': 0, '47': 0, '48': 0, '49': 0, '50': 0, '51': 0, '52': 0, '53': 0, '54': 0, '55': 0, '56': 0, '57': 0, '58': 0, '59': 0, '60': 0, '61': 0, '62': 0, '63': 0, '64': 0, '65': 0, '66': 0, '67': 0, '68': 0, '69': 0, '70': 0, '71': 0, '72': 0, '73': 0, '74': 0, '75': 0, '76': 0, '77': 0, '78': 0, '79': 0, '80': 0, '81': 0, '82': 0, '83': 0, '84': 0, '85': 0, '86': 0, '87': 0, '88': 0, '89': 0, '90': 0, '91': 0, '92': 0, '93': 0, '94': 0, '95': 0, '96': 0, '97': 0, '98': 0, '99': 0, '100': 0, '101': 0, '102': 0, '103': 0, '104': 0, '105': 0, '106': 0, '107': 0, '108': 0, '109': 0, '110': 0, '111': 0, '112': 0, '113': 0, '114': 0, '115': 0, '116': 0, '117': 0, '118': 0, '119': 0, '120': 0, '121': 0, '122': 0, '123': 0, '124': 0, '125': 0, '126': 0, '127': 0, '128': 0, '129': 0, '130': 0, '131': 0, '132': 0, '133': 0, '134': 0, '135': 0, '136': 0, '137': 0, '138': 0, '139': 0, '140': 0, '141': 0, '142': 0, '143': 0, '144': 0, '145': 0, '146': 0, '147': 0, '148': 0, '149': 0, '150': 0, '151': 0, '152': 0, '153': 0, '154': 0, '155': 0, '156': 0, '157': 0, '158': 0, '159': 0, '160': 0, '161': 0, '162': 0, '163': 0, '164': 0, '165': 0, '166': 0, '167': 0, '168': 0, '169': 0, '170': 0, '171': 0, '172': 0, '173': 0, '174': 0, '175': 0, '176': 0, '177': 0  }
    interhref=[]
    exterhref=[]
    interlog=[]
    exterlog=[]
    chain=[]
    title=[]
    text=[]
    chainurl(chain)
    starturl=chain[0]
    landurl=chain[-1]
    interandextern(landurl,interhref,exterhref,"file/href.txt")
    interandextern(landurl,interlog,exterlog,"file/logged.txt")
    loaddata(title,'file/title.txt')
    loaddata(text,'file/text.txt')
    feature_1 = []
    f1_8feature(feature_1, starturl)
    f1_8feature(feature_1, landurl)

    f1_3_8feature(feature_1, interhref)
    f1_3_8feature(feature_1, interlog)
    f1_3_8feature(feature_1, exterhref)
    f1_3_8feature(feature_1, exterlog)

##
#   Feature 2 calculating
##
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

    #print_wo(binaryfeatures(intrdn,title),",")
    #print_wo(binaryfeatures(extrdn,title),",")
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
                #print_wo("1",",")
            else:
                feature_3n4.append(0)
                #print_wo("0",",")
    compare = [title,intlog,extlog,intlink,extlink]
    compare = " ".join(str(x) for x in compare)
    for i in range(2):
        for j in range(5):
            if compare[j] in mlds[i]:
                feature_3n4.append(1)
                #print_wo("1",",")
            else:
                feature_3n4.append(0)
                #print_wo("0",",")
    for m in range(2):
        for n in range(5):
            if compare[j] in rdns[i] and compare[j] not in mlds[i]:
                feature_3n4.append(1)
                #print_wo("1",",")
            else:
                feature_3n4.append(0)
                #print_wo("0",",")


    ##
    # f3 features calculeted
    ##

    ##
    # f4 features calculeting
    ##

    if getrdn(starturl) in getrdn(landurl):
        feature_3n4.append(1)
        #print_wo(1,",")
    else:
        feature_3n4.append(0)
        #print_wo(0,",")
    if len(chain) > 2:
        feature_3n4.append(len(chain)-2)
        #print_wo(len(chain)-2,",")
    else:
        feature_3n4.append(0)
        #print_wo(0,",")
    feature_3n4.append(len(interlog))
    feature_3n4.append(len(interhref))
    ##print_wo(len(interlog),",")
    ##print_wo(len(interhref),",")

    feature_3n4.append(len(exterlog))
    feature_3n4.append(len(exterhref))
    #print_wo(len(exterlog),",")
    #print_wo(len(exterhref),",")

    count = 0
    for comp in interlog:
        if getrdn(starturl) in getrdn(comp):
            count += 1
    feature_3n4.append(count)
    #print_wo(count,",")


    count = 0
    for comp in interhref:
        if getrdn(starturl) in getrdn(comp):
            count += 1
    feature_3n4.append(count)
    #print_wo(count,",")

    count = 0
    if len(chain) > 2 :
        for comp in chain[1:len(chain)-1] :#check later
            if getrdn(starturl) in getrdn(comp):
                count += 1
    feature_3n4.append(count)
    #print_wo(count,",")


    count = 0
    if len(chain) > 2 :
        for comp in chain[1:len(chain)-1] :#check later
            if getrdn(landurl) in getrdn(comp):
                count += 1
    feature_3n4.append(count)
    #print_wo(count,",")


    count = 0
    for comp in exterlog :#check later
        if getrdn(starturl) in getrdn(comp):
            count += 1
    feature_3n4.append(count)
    #print_wo(count,",")

    count = 0
    for comp in exterlog : #check later
        if getrdn(starturl) in getrdn(comp):
            count += 1
    feature_3n4.append(count)
    #print_wo(count,",")

    ##
    # f4 features calculed
    ##
    ##
    # f5 features calculation
    ##
    feature_5 = []
    file = open('file/input.txt',"r")
    data = file.read()
    word = data.split()

    feature_5.append(len(word))
    #print_wo(len(word),",")

    file = open('file/img.txt',"r")
    data = file.read()
    word = data.split()
    feature_5.append(len(word))

    #print_wo(len(word),",")

    file = open('file/iframe.txt',"r")
    data = file.read()
    word = data.split()
    feature_5.append(len(word))

    #print_wo(len(word),",")

    file = open('file/text.txt',"r")
    data = file.read()
    word = data.split()
    feature_5.append(len(word))

    #print_wo(len(word),",")

    file = open('file/title.txt',"r")
    data = file.read()
    word = data.split()
    feature_5.append(len(word))

    #print(len(word))

    #sys.stdout = original_stdout # Reset the standard output to its original value
    res = feature_1 + feature_2 + feature_3n4 + feature_5

    for i in range(len(res)):
        result[str(i)] = res[i]

    return result
#phish_extraction()
