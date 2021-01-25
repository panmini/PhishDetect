import json
from urllib.request import urlopen
#weather = urlopen('http://data.phishtank.com/data/online-valid.json')
#wjson = weather.read()
fa = open('features.txt',)
wjdata = json.loads(fa.read())

f = open("dp"+str(len(wjdata))+".txt","w")
for i in range(len(wjdata)):
    f.write(wjdata[i]['info']['url']+'\n')

