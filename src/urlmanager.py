'''
Manages all the espncricinfo urls.
Gives back either a list of strings of all match summaries
OR - a list of all URLs if full scorecard is requested by the user.
author : Abrar Amin (abrar.a.amin@gmail.com)
'''
import sys
import requests
import fonts
import re
import json
from bs4 import BeautifulSoup



global f #used to maintain the instance of the fonts class.
BASE_URL = "http://www.espncricinfo.com"

# Open the (live games) url and return the HTML file data as a string.
def openLink(inURL):
	try:
		r = requests.get(inURL)
	except:
		sys.stderr.write("Couldn't open "+inURL)
		return
	text = r.text
	return text


# Returns a list of dictionaries, each entry holds information on one game.
def createGameDictionaryList(numberOfGames):
	keys = ["status", "title", "venue", "date", "innings1", "innings2", "summary", "url"]
	gameDictionary = {key: "" for key in keys}  #store all match summaries, including quick results and URLs to full scorecard in this dictionary..
	gameDictionaryList = []
	for i in range(numberOfGames):
		gameDictionaryList.append(gameDictionary.copy())
	return gameDictionaryList


#Assign title to each game e.g. "Sheffield Sheild", "One Day International", etc.
def assignTitles(inList, soup):
	global f
	# find the number of games under each different titles.
	text = soup.prettify()
	matchTitleList = text.split("<div class=\"match-section-head\"")[1:] #store all the contents of the HTML file in between game title tags. Skip 1st element, as no games.
	numGameForTitle = []
	for i in range(len(matchTitleList)):
		numGameForTitle.append(matchTitleList[i].count("default-match-block"))

	matchTitles = soup.find_all("div", {"class" : "match-section-head"})
	index = 0 #tracks game dictionary list.
	numGameForTitleIndex = 0 #tracks number of games per title list.

	for title in matchTitles:
		for i in range(numGameForTitle[numGameForTitleIndex]):
			inList[index]["title"] = f.BOLD + title.contents[0].text +f.ANSI_RESET    #title of the game i.e. team 1 vs team 2
			index+=1
		numGameForTitleIndex+=1




# Returns a list of dictionaries.
# Each row represents 1 game.
# values stored - "LIVE", title, venue, date, innings 1, innings 2 and URL to full scoreboard in that order.
def summaryList(soup, numgames):
	global f
	matchSummaryList = createGameDictionaryList(numgames)
	index = 0
	allMatches = soup.find_all("section", class_ = "default-match-block")

	for item in allMatches:
		n = 3
		if(re.sub("\s+"," ",(item.contents[1].contents[0])).lstrip() == ""):
			matchSummaryList[index]["status"] = f.BG_GREEN + f.FG_WHITE + "COMPLETE" + f.ANSI_RESET  #"Completed"
			matchSummaryList[index]["venue"] = re.sub("\s+"," ",item.contents[1].contents[5].find_all("a")[0].text + f.ANSI_RESET).lstrip() # venue of the game. get rid of all leading tab and newline characters.
			matchSummaryList[index]["date"] = re.sub("\s+"," ",item.contents[1].contents[1].text).lstrip() #dates
			matchSummaryList[index]["url"] = (BASE_URL+ item.contents[1].contents[5].find_all("a")[0].get("href")) #URL to scoreboard.

		else:
			matchSummaryList[index]["status"] = f.BG_CYAN + f.FG_WHITE + item.contents[1].contents[0] + f.ANSI_RESET  #"LIVE"
			matchLocation = item.contents[n].find_all("a")[0].text + f.ANSI_RESET
			matchSummaryList[index]["date"] = item.contents[n].find_all("span",{"class" : "bold"})[0].text #dates
			matchSummaryList[index]["venue"] = re.sub("\s+"," ",matchLocation).lstrip() # venue of the game. get rid of all leading tab and newline characters.
			matchSummaryList[index]["url"] = (item.contents[3].find_all("a")[0].get("href")) #URL to scoreboard.
			n+=2
		matchSummaryList[index]["innings1"] = f.BOLD + re.sub("\s+"," ",item.contents[n].text).lstrip() + f.ANSI_RESET  #innings 1- remove all new line characters
		matchSummaryList[index]["innings2"] = f.BOLD + re.sub("\s+"," ",item.contents[n+2].text).lstrip() + f.ANSI_RESET # innings 2 info.
		matchSummaryList[index]["summary"] = f.FG_MAGENTA+f.BOLD+re.sub("\s+"," ",item.contents[n+4].text).lstrip()+ f.ANSI_RESET
		index+=1

	assignTitles(matchSummaryList, soup)

	return matchSummaryList


# Take in a URL and get data.
def getJSObject(url):
	try:
		res = requests.get(url)
	except:
		sys.stderr.write("Couldn't open "+url+"\n")
		return
	dataText = res.text
	JSONdata = json.loads(dataText)

	# with open(dataText) as data_file:
	# 	data = json.load(data_file)
	return JSONdata


# Return a list of urls to game scorecard webpages. Only return a list of
# length of numgames param. Otherwise return all live scorecard URLs if numgames
# parameter exceeds the total number of live games. Set to 5 by default.
# display type determines weather to return a list with the simple game summary or links to scorecard.
# If showAll parameter is true, print all games regardless of numgames parameter.
def urlList(enableFontStyle, resultMode):
	global f
	f = fonts.fonts()
	if(not enableFontStyle):
		f.disable()
	if(not resultMode):
		htmlString = openLink(BASE_URL+"/ci/engine/match/index.html?view=live")
	else:
		htmlString = openLink(BASE_URL+"/ci/engine/match/index.html?view=week")
	soup = BeautifulSoup(htmlString, "html.parser")
	numberOfLiveGames = htmlString.count("<div class=\"match-info\">")  #find the number of live games.
	resultList = summaryList(soup, numberOfLiveGames)
	return resultList
