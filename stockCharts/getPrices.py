import csv, requests, json, os, pytz
from datetime import datetime
from pytz import timezone
 
#HEY!! LIST OF TIMEZONES - https://stackoverflow.com/questions/13866926/python-pytz-list-of-timezones
 
array = [[]]
 
r = requests.get('https://chartapi.finance.yahoo.com/instrument/1.0/^AORD/chartdata;type=quote;range=7d/json') #Request URL must be exactly the same as what the API expects
try:
    str = str(r.text)
    firstBrack = str.find('(') + 1
    lastBrack = str.find(')')
    str = str[firstBrack:lastBrack] #Get the string only containing json, without the callback data function lines
    jsonData = json.loads(str)
    data = jsonData['series']
except IndexError:
    print 'IndexError'
   
with open("data.csv", "wb") as file:
    csv_file = csv.writer(file)
    csv_file.writerow(['Time', 'close'])
    for item in data:
        newFormat = datetime.fromtimestamp(int(item['Timestamp']))
#        tzFormat = newFormat.astimezone(timezone('America/New_York'))
        finalFormat = newFormat.strftime('%H:%M:%S')
        csv_file.writerow([finalFormat, item['close']])