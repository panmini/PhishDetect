import json
from urllib.request import urlopen
weather = urlopen('http://data.phishtank.com/data/online-valid.json')
#f = open('data.json',)
wjson = weather.read()
wjdata = json.loads(wjson)

f = open("dp"+str(len(wjdata))+".txt","w")
for i in range(len(wjdata)):
        if wjdata[i]['online'] == 'yes' and wjdata[i]['verified'] == 'yes':
            f.write(wjdata[i]['url']+'\n')



