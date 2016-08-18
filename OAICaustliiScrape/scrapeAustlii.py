#!/usr/bin/env python
import csv, requests, time, datetime
from contextlib import closing
from bs4 import BeautifulSoup

url = 'http://www5.austlii.edu.au/au/cases/cth/AICmr'
years = ['2011','2012','2013','2014','2015']
targetLinksNumber = []
resultsList = []
rowNumber = 0

def scrape(url,year, extender):
    time.sleep(2) #Making sure our requests aren't a burden on their surver
    urlHeaders = {"User-Agent": "Jason Thomas, journalist, SBS News, https://github.com/JasonThomasData/WebWatcher, jason.thomas(at)sbs.com.au", "Referer": "www.sbs.com.au/news"}
    requestURL = '%s/%s/%s' %(url,year,extender)
    page_source = requests.get(requestURL, headers=urlHeaders, timeout=None)
    return page_source.content

# use firefox to get page with javascript generated content
#This also works for static web pages, which don't work with Requests
'''
def scrape(url,year, extender):
    with closing(Firefox()) as browser:
        request = '%s/%s/%s' %(url,year,extender)
        browser.get(request)
        WebDriverWait(browser, timeout=None)#.until(
            #lambda x: x.find_element_by_class_name('wrapper'))
            #lambda x: x.find_element_by_id('dcCatalogBox'))
        page_source = browser.page_source
        return page_source
        #I've turned bboth lambda fuunctions and the wait off, as there's no element to wait for
'''

#Jason, why did you make this function so massive? Consider cleaning this up at some point.
def appendRow(table, summary, num, requestURL):
#Function runs for each page
    def stripCharacters(elemToChange):
    #Seek and destroy \n, which will put data on new lines in CSV - bad mojo
        elemToChange = elemToChange.getText() 
        elemToChange = elemToChange.replace('\n', ' ')
        elemToChange = elemToChange.encode('ascii', 'ignore')
        return elemToChange

    tr = table.findAll('tr')
    newLine = [' '] * 5 #As far as I know, I'll only ever want five objects from the table.
    for n in range(0, len(tr)): #-1 because I don't want the last one
        tableCell = tr[n].findAll('td')
        if len(tableCell) == 0:
            tableCell = tr[n].findAll('th')
        newLabel = stripCharacters(tableCell[0]) #the table column of row names
        newCell = stripCharacters(tableCell[1])
        #This maps the data to the correct array elements, in order
        if 'Applicant' in newLabel or 'Complainant' in newLabel:
            newLine[0] = newCell
        elif 'Respondent' in newLabel:
            newLine[1] = newCell.strip()
        elif 'Other parties' in newLabel:
            newLine[2] = newCell
        elif 'Decision date' in newLabel or 'Determination date' in newLabel:
            newLine[3] = newCell.strip()
        elif 'Application number' in newLabel:
            newLine[4] = newCell
            applicationType= newCell
    summaryText = stripCharacters(summary)
    print num,' - ',summaryText
    result = ''
    if 'vary' in summaryText:
        result = 'vary'
    elif 'affirm' in summaryText:
        result = 'affirm'
    elif 'set aside' in summaryText:
        result = 'set aside'
    else:
        result = 'other'

    if 'MR' in applicationType:
        reviewType = 'FOI'
    elif 'RQ' in applicationType:
        reviewType = 'Vexatious'
        result = 'vexatious'
    elif 'c1' in applicationType or 'CP' in applicationType:
        reviewType = 'Privacy'
    else:
        reviewType = 'other'
    newLine.append(requestURL)
    newLine.append(result)
    newLine.append(reviewType)
    newLine.append(summaryText)
    resultsList.append(newLine)

for i in range(0, len(years)):
    pageContent = scrape(url,years[i],'')
    soup = BeautifulSoup(pageContent)
    findLinks = soup.findAll('a')
    linkNumber = len(findLinks)
    lastLinkNumber = linkNumber - 4 #Always an extra four links on these pages.
    targetLinksStart = findLinks[:lastLinkNumber]
    targetLinksFinish = targetLinksStart[14:] #Always an extra 14 links at start of pages
    targetLinksNumber.append(len(targetLinksFinish))
    #Here, I want the numbers of links. All the pages go up chronologically from 1. i push the links to an array and get the array length

for j in range(0, len(targetLinksNumber)):
    for num in range(1, targetLinksNumber[j]+1):
        extender = '%s.%s' %(num,'html') #eg 1.html
        requestURL = '%s/%s/%s' %(url,years[j],extender)
        pageContent = scrape(url,years[j],extender) #eg http://www5.austlii.edu.au/au/cases/cth/AICmr/2015/1.html
        soup = BeautifulSoup(pageContent)
        allContent = soup.findAll(True)
        allTables = soup.findAll('table')[1] #Need the second, the first is table labels.
        summaryParagraph = soup.find('ol')
        appendRow(allTables, summaryParagraph, num, requestURL)

'''
for q in range(0, len(allContent)):
#This loop finds the heading 'Summary' and gets the next element index. That's the 'Summary'
    if 'Summary' in allContent[q].getText():
        indexNumber = q + 1
'''

def insertionSort(arrayToSort, dateElem):
    def getDate(dateToConvert):
        dateToConvert = dateToConvert.strip()
        print datetime.datetime.strptime(dateToConvert, "%d %B %Y") #According to this site - http://www.tutorialspoint.com/python/time_strptime.htm - %B is shortcode for a full printed date.
        return datetime.datetime.strptime(dateToConvert, "%d %B %Y") 
    def insert(elemToInsert):
        loop = True
        j = 0
        while(loop):
            if getDate(elemToInsert[dateElem]) < getDate(arrayToSort[j][dateElem]):
                arrayToSort.insert(j,elemToInsert)
                loop = False
            else:
                j += 1
    arrayLength = len(arrayToSort)
    for x in range(1, arrayLength):
        if getDate(arrayToSort[x][dateElem]) < getDate(arrayToSort[x-1][dateElem]):
            elemToInsert = arrayToSort[x]
            arrayToSort.pop(x)
            insert(elemToInsert)

insertionSort(resultsList, 3) #0 is the elemenent where the date is in the sub array

with open('resultsCSV.csv', 'w') as csvFile:
    csvWriter = csv.writer(csvFile, delimiter=',') #This delimeter, because commas are interfering
    topRow = ['Applicant/complainant','Respondent','Other parties','Decision date','Application number','Decision link','Review decision','Review type','Decision summary']
    csvWriter.writerow(topRow)
    for p in range(0, len(resultsList)):
        csvWriter.writerow(resultsList[p])