import requests
from bs4 import BeautifulSoup
import re
import json

dataArray = []
brandArray = []

i=1
url = 'https://www.auto-data.net/en/results?brand=0&model=0&power1=&power2=&fuel[]=6&page='
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'}
while(True):
    newUrl = url + str(i)
    resp = requests.get(newUrl, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')
    lst = soup.find_all("span", re.compile("title"))
    if(len(lst) == 0 ):
        break
    for index, item in enumerate(lst):
        data = '{1}'.format(index + 1, item.text.strip())
        data = re.sub(r" ?\([^)]+\)", "", data)
        if(not(data in dataArray)):
            dataArray.append(data)
        brand = data.split(' ', 1)[0]
        if(not(brand in brandArray)):
            brandArray.append(brand)
    i+=1;
dataArray.sort()
brandArray.sort()
with open('./data/CarNameData.txt', 'w') as outfile:  
    json.dump(dataArray, outfile)

with open('./data/BrandData.txt', 'w') as outfile:  
    json.dump(brandArray, outfile)
