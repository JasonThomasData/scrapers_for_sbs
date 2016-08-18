import requests, csv, time, re
from bs4 import BeautifulSoup

def getRequest(url,urlExtender):
	r = requests.get(url + urlExtender)
	print url + urlExtender #Useful for diagnosing if URL is wrong - wrong URL, no markup
	soup = BeautifulSoup(r.content)
	return soup

totalResults = []
dataFields = ['Name', 'Link to soldier on AWM', 'Birth date', 'Date of birth', 'Birth place', 'Date and unit at enlistment (ORs)', 'Final rank', 'Date of discharge', 'Conflict', 'Unit', 'Units', 'Date of embarkation', 'Embarkation date', 'Service number', 'Death date', 'Date of death', 'Death place', 'Place of death']
collectAllFields = []

def getTableData(row):
	rowData = row.findAll(['td', 'th'])
	#for i in range(0, len(rowData)):
	if len(rowData) > 1:
		for f in range(0, len(dataFields)):
			if str(dataFields[f]).lower() in str(rowData[0].getText().strip()).lower():
				thisPersonTables[f] = rowData[1].getText().encode('utf-8').strip()
				return
		#If you get to this point, you know the field wasn't found, so add to the collectAllFields array
		collectAllFields.append(str(rowData[0].getText().strip()))
	else:
		print 'This row is only ' + len(rowData) + ' long'

def getRows(table):
	rows = table.findAll('tr')
	for row in rows:
		getTableData(row)

def getTables(peopleBio):
	#Parse all data to an object/ array.
	thisPersonTables = []
	for field in dataFields:
		thisPersonTables.append('none')
	tables = peopleBio.findAll('table')
	for table in tables:
		getRows(table)
	print thisPersonTables
	return thisPersonTables
	#Maybe a class? At the end, add these to an array

def getDivResults(peopleBio):
	try:
		divResult = peopleBio.find('div', {'class':'results-cas'})
	except IndexError:
		print 'Index Error'
	except ValueError:
		print 'Value Error'

def run_scraper():
	url = 'https://www.awm.gov.au'
	peopleArray = []
	firstExtender = '/people/profiles/#indigenousservice'
	#The initial scrape, get all links for each soldier
	soup = getRequest(url,firstExtender)	
	indigDiv = soup.find('div', {'id': 'indigenousservice'})
	allLinks = indigDiv.findAll('a')
	for a in allLinks:
		aHrefStr = str(a.get('href'))
		if 'people' in aHrefStr:
			peopleArray.append(aHrefStr)
	#Scrape the page for every person
	for p in range(0, len(peopleArray)):
	#for p in range(0, 10):
		time.sleep(2)
		peopleExtender = peopleArray[p] + '#biography'
		newSoup = getRequest(url,peopleExtender)
		contentDiv = newSoup.find('div', {'id': 'content'})
		pageTitleName = contentDiv.find('h1', {'class': 'pagetitle'})
		print p, pageTitleName.getText().strip()
		peopleBio = contentDiv.find('div', {'id': 'people-biography-page'})
		soldierResults = getTables(peopleBio)
		soldierResults[0] = pageTitleName.getText().strip().replace('\r','').replace('\n','')
		soldierResults[1] = url + peopleExtender
		totalResults.append(soldierResults)
		getDivResults(peopleBio)
	print collectAllFields
run_scraper()

with open('resultsCSV.csv', 'w') as csvFile:
    print totalResults
    csvWriter = csv.writer(csvFile, delimiter=',') #This delimeter, because commas are interfering
    csvWriter.writerow(dataFields)
    for p in range(0, len(totalResults)):
        csvWriter.writerow(totalResults[p])