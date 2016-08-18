###Scrapers for SBS
####Here are the (reusable) scraping projects I completed for SBS News while I worked there.

I will apologise in advance - this code spans my entire experience with Python, so some of this code is messy and confusing. I will rewrite the code if I'm requested/if I get to it.

All of this code is procedural in nature. That means there's generally no classes and objects etc. I just have a bunch of functions that must be run, start to finish.

###The scrapers

- airSafetyNet - scrapes an online database of air crashes worldwide. I've used this data to show that, despite the reporting on plane crashes in 2014/15, the number of deaths and crashes had declined for decades. This article gets updated when there's a major air disaster - 

- anniversaris_list - scrapes an online list of anniversaries and tells you what's coming up in terms of the major ones - 1 years, 2, 3, 4, 5, 10, 15, 20, 25, 30, 35, 40, 40, 50, 55, 60, 70 years, etc.

- indigSoldiersAWN - scrapes the Australian War Memorial website, which has a list of Indigenous soldiers who fought in WWI. Details include birth place, theatre of war, age of soldier, etc.

- OAICaustliiScrape - scrapes the Australian Government law archive to retreive details about OAIC decisions. Used to make this story and dataviz - 

- rioOlympics - a scraper to retreive the details of Australian athletes attending the Rio Olympic games. I'm preparing this now for a future journalist to use.

- stockCharts - retreives same day trading data on Australian companies and stock indeces. Useful for stories about share market tumbles at end of day trading.

###Requirements

All of these projects were written in ```Python 2.7.8``` and on PC running ```Ubuntu 14.04```.

All projects use the Python packages ```requests``` and ```BeautifulSoup4```.

I use virtualenv for my tasks. I recommend you do so too, so that you can isolate the packages you run for each project. 

I run my scrapers locally, but another great option is to put your scrapers on Morph. Morph is a free 

I also sometimes run my scrapers from a linux-based vitual private server, automated to run at certain times with the handy scheduling program, ```crontab```. This means I can always scrape anything without turning my computer on.

Morph also provides automated scraping, but those are limited to one per day for each scraper (I think).

###Ethical issues addressed in the process of scraping

I don't really think there's too much to consider. If a provider puts content online then it's up to me how I choose to consume the content. There's no one who can expect you to view content through a standard web browser.

In saying that, if a site or data is privately owned, it is courteous to abide by their wishes. This means, checking if they explicitly say 'no scraping'.

Realistically, a site that doesn't allow scraping is going to be hard to find, since Google is a giant web scraper.

Regarding government-published web content, this is not an issue, as I'm a taxpayer - I own the government. Since it's my content anyway, I don't think I should have to read any such disclaimer, etc.

Since I'm a journalist, it's appropriate to tell people who I am at all times. Requests makes this simple to do. Just define a custom header when you make a request, like this:

	urlHeaders = {"User-Agent": "NAME, JOB, ORGANISATION, LINK TO GIT REPO, EMAIL ADDRESS"}
	r = requests.get(url, headers=urlHeaders, timeout=None)

I've identified myself here so if any admin type wonders what I'm up to, they can email me.

Another consideration is the burden of making requests. I think you should pad out each request by at least a second, and sometimes a few, to make sure you're not a burden on their server.

I do this with the standard module, time:

	time.sleep(3) #wait for three seconds

Finally, I think if you're going to scrape content, consier putting it online where others can get it. This may reduce the need for others to scrape content. You can do this by simply making a Gist on Github.

Another, possibly better, option is to put yor scrapers on Morph where anyone can use them.

