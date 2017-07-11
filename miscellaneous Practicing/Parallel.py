#Script to parallelize the downloads
import zipfile
import os
import re
import sys
import urllib2
import requests
from bs4 import BeautifulSoup

def get_content(url):
	r = requests.get(url)
	return BeautifulSoup(r.content, "html.parser")

#download the content from given url
def downloadFile(url):
	try:
		df = urllib2.urlopen(url)
		fileName = url.split("\\")[-1]
		with open(fileName, "wb") as fp:
			fp.write(df.read())
	except Exception as e:
		print str(e)
		sys.exit()

#This method extracts contents from a given zip file and deletes that zipfile forever
def extractFiles(path):
	zipFilePtr = zipfile.ZipFile(path, 'r')
	zipFilePtr.extractAll(path)
	zipFilePtr.close()
	os.remove(path)

def main():
	companiesUrl = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
	ticketUrl = "https://finance.yahoo.com/quote//history?ltr=1"
	soup = get_content(companiesUrl)
	table = soup.findAll('table', {'class' : 'wikitable'})[0]
	trTags = table.findAll('tr')
	for trTag in trTags:
		tdTags = trTag.findAll("td")
		if len(tdTags) > 2:
			company = tdTags[1].text
			code = tdTags[0].text
			tempTicketUrl = ticketUrl[:32]+code+ticketUrl[32:]
			print tempTicketUrl
			tSoup = get_content(tempTicketUrl)
			tTable = tSoup.findAll('table')[1]
			if len(tTable) > 0:
				tTrTags = tTable.findAll('tr')[1]
				if len(tTrTags) > 0:
					tTdTags = tTrTags.findAll('td')
					if len(tTdTags) > 0:
						# print tTdTags[0].text, tTdTags[4].text
						pass

import mechanize
import bs4
def dmain():
	path = "https://www.oanda.com/fx-for-business/historical-rates"
	soup = get_content(path)
	navBar = soup.findAll("div", attrs = {'class':'nav'})
	for each in navBar:
		print bool(re.match( r".*accountControl.*", each.text, re.I) )
		div = each.findAll("div", attrs = {'class' : 'hcc-nav-primary-actions'})
		print div[0].findAll("div")
	# browser = mechanize.Browser()
	# browser.set_handle_equiv(True)
	# browser.set_handle_redirect(True)
	# browser.set_handle_referer(True)
	# browser.set_handle_robots(False)
	# browser.set_handle_gzip(True)
	# browser.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
	# browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
	# response = browser.open(path)
	# soup = bs4.BeautifulSoup(response.read(), 'html.parser')
	# with open('dummy.txt', 'w') as fp:
	# 	text = re.sub(r'\n+', '\n', soup.text)
	# 	for line in text.split('\n'):
	# 		fp.write(line)
	# browser.find_link(text = "Sign-in")
	# response = browser.click_link(text = "Sign-in")
	# browser.open(response)
	# print browser.response().read()
if __name__ == "__main__":
	dmain()

	