from bs4 import BeautifulSoup
import requests
import datetime
import csv
import time

timeStarted = datetime.datetime.today()
latest = '2016'
first = 'year unknown' #the query string will be 1900
going = False
firstPageLinks = []

url = 'http://aviation-safety.net/database/'
urlHeaders = {"User-Agent": "Jason Thomas, journalist, SBS News, https://github.com/JasonThomasData/WebWatcher, jason.thomas(at)sbs.com.au", "Referer": "www.sbs.com.au/news"}
r = requests.get(url, headers=urlHeaders, timeout=None)

soup = BeautifulSoup(r.content)
mianContent = soup.find('div', {'class': 'innertube'})
allLinks = mianContent.findAll('a')

trInTable = []
year = 1920

for i, link in enumerate(allLinks):
    if first in link:
        going = True
    if latest in link:
        going = False
        firstPageLinks.append(link)
    if (going):
        firstPageLinks.append(link)

for j, link in enumerate(firstPageLinks):
    secondUrl = url + str(link.get('href'))
    secondContent = requests.get(secondUrl, headers=urlHeaders, timeout=None)
    secondSoup = BeautifulSoup(secondContent.content)
    secondContent = secondSoup.find('div', {'class': 'pagenumbers'})
    pagesNumber = len(secondContent) / 2
    for m in range(0, pagesNumber):
        time.sleep(3)
        thirdUrl = url + str(link.get('href')) + '&lang=&page=' + str(m + 1)
        print thirdUrl
        thirdContent = requests.get(thirdUrl, headers=urlHeaders, timeout=None)
        thirdSoup = BeautifulSoup(thirdContent.content)
        thirdContent = thirdSoup.find('div', {'class': 'innertube'})
        getTable = thirdContent.find('table')
        getTr = getTable.findAll('tr')
        #print getTr[0].findAll('th').get_text
        for k in range(1, len(getTr)): #Can't start at 0, because the first tr is a heading, so there won't be any td data!
            getTd = getTr[k].findAll('td')
            tdInRow = []
            for l in range(0, len(getTd)):
                tdInRow.append(getTd[l].get_text().encode('utf-8')) #encode turns unicode into a normal str
            trInTable.append(tdInRow)
    time.sleep(1)

with open('airSafetyNet.csv', 'wb') as csvFile:
    csvWriter = csv.writer(csvFile, delimiter = ',')
    for n in range(0, len(trInTable)):
        csvWriter.writerow(trInTable[n])

timeFinished = datetime.datetime.today()
print "TIME timeFinished ~ " + str(timeFinished)
print "TIME taken ~ " + str(timeFinished - timeStarted)