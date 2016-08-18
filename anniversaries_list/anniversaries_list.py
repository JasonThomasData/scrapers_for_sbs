import requests
from bs4 import BeautifulSoup
import time

#Create the list of anniversaries that we're searching for
def populate_possible_aniversaries(this_year, main_anniversaries):
    for i in range(1,5,1): #1 to 4
        year_to_add = this_year - i
        main_anniversaries.append([year_to_add, i])
    for j in range(5,55,5): #5 to 50
        year_to_add = this_year - j
        main_anniversaries.append([year_to_add, j])
    for k in range(60,410,10): #60 to 400
        year_to_add = this_year - k
        main_anniversaries.append([year_to_add, k])
    return main_anniversaries

#This is the code that the program needs to run. Consider putting this in a config.py if you get time.	
this_year = 2016 #Year to start search with - goes to 2017, 18 etc
main_anniversaries = []
print populate_possible_aniversaries(this_year, main_anniversaries)
day_limits_by_month = [31,29,31,30,31,30,31,31,30,31,30,31]

def parse_td_match_years(td_no_headings):
    if '<td align="RIGHT" valign="TOP" width="10%">' in str(td_no_headings):
        for year in main_anniversaries:
            if str(year[0]) in str(td_no_headings):
                return year[1]
    return False

def parse_td_strip_headings(td):
    if 'Australian History' not in str(td) and 'Born on this day' not in str(td) and 'World History' not in str(td):
        parse_td_result = parse_td_match_years(td)
        if parse_td_result != False:
            return parse_td_result
    return False

def scrape_one_page(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content)
    table = soup.find_all('table')[2]
    table2 = table.find_all('table')[0]
    table3 = table2.find_all('table')[0] #Tables nested in tables - people actually used to design websites like that.
    for tr in table3:
        next_one = False
        for td in tr:
            parse_td_result = parse_td_strip_headings(td)
            if parse_td_result != False:
                #So, here I'm saying, if this element is not a heading (defined in the function) and it is a date, then we want to save it. If it's False then it's heading or not a date, do nothing.
                b = soup.find_all('b')[1]
                print '%s%s<br>' %(b, ' (today)')
                print '<b>%s years anniversary</b><br>' %(parse_td_result)
                print '%s <br>' %(td)
                next_one = True
            elif next_one == True:
                print '%s <br><br><br>' %(td)
                next_one = False

#Prepare string to send in querym to fetch site data.
def format_string_for_request(i, j):
    new_i = str(i) #month parse as string
    new_j = str(j) #date parse as string
    if i < 10:
        new_i = '0%s' %(i) #Put a zero in front of numbers below 10, because that's what the server is expecting.
    if j < 10:
        new_j = '0%s' %(j)
    formatted_request = 'http://today.wmit.net.au/?today_day=%s&today_month=%s&today_year=%s' %(new_j, new_i, this_year) 
    return formatted_request

#Starting variables to start the collection. We don't want anything before May 18.
#For the year ahead, make these blank.
month_number = 4 #May
day_number = 18 #19th

#This ticks up through the days of each month, checking the dates on each against the target anniversaries.
def cycle_dates(day_limits_by_month):
    for i in range(month_number,len(day_limits_by_month)): #Remove the first param after this scrape
        for j in range(day_number, int(day_limits_by_month[i])):
            formatted_request = format_string_for_request(i+1, j+1)
            time.sleep(5)
            scrape_one_page(formatted_request)

cycle_dates(day_limits_by_month)