'''
Manages all the espncricinfo urls.
Gives back either a list of strings of all match summaries
OR - a list of all URLs if full scorecard is requested by the user.
'''
import sys
import requests 
import fonts
import re

from bs4 import BeautifulSoup


BASE_URL = "http://www.espncricinfo.com"

# Open the live game url and return the HTML file data as a string.
def openLink(inURL):
	try:
		r = requests.get(inURL)
	except:
		sys.stderr.write("Couldn't open "+inURL)
		return 
	text = r.text
	return text



# Returns a 2D list of strings containing a very short summary of ongoing games.
# Each row represents 1 game. 
# values stored - "LIVE", title, venue, date, innings 1, innings 2 and URL to full scoreboard in that order.
def summaryList(soup, numgames):
	matchSummaryList = [[x for x in range(8)]for y in range(numgames)] #store all match summaries, including quick results and URLs to full scorecard in a 2D array. 
	index = 0
	allMatches = soup.find_all("section", class_ = "default-match-block")
	matchTitles = soup.find_all("div", {"class" : "match-section-head"})

	for item in allMatches:
		matchLocation = item.contents[3].find_all("a")[0].text + fonts.ANSI_RESET  #get rid of all leading tab and newline characters.

		matchSummaryList[index][0] = fonts.BG_CYAN + fonts.FG_WHITE + item.contents[1].contents[0] + fonts.ANSI_RESET  #"LIVE"
		matchSummaryList[index][3] = item.contents[3].find_all("span",{"class" : "bold"})[0].text #dates
		matchSummaryList[index][2] = re.sub("\s+"," ",matchLocation).lstrip() # venue of the game.
		matchSummaryList[index][4] = fonts.BOLD + re.sub("\s+"," ",item.contents[5].text).lstrip() + fonts.ANSI_RESET  #innings 1- remove all new line characters
		matchSummaryList[index][5] = fonts.BOLD + re.sub("\s+"," ",item.contents[7].text).lstrip() + fonts.ANSI_RESET # innings 2 info.
		matchSummaryList[index][6] = fonts.FG_MAGENTA+re.sub("\s+"," ",item.contents[9].text).lstrip()+ fonts.ANSI_RESET
		matchSummaryList[index][7] = (BASE_URL+ item.contents[3].find_all("a")[0].get("href")) #URL to scoreboard.
		index+=1
	
	index = 0
	for title in matchTitles:
		matchSummaryList[index][1] = fonts.BG_YELLOW + title.contents[0].text +fonts.ANSI_RESET    #title of the game i.e. team 1 vs team 2
		index +=1
	
	return matchSummaryList 




# Return a list of urls to game scorecard webpages. Only return a list of 
# length of numgames param. Otherwise return all live scorecard URLs if numgames
# parameter exceeds the total number of live games. Set to 5 by default. 
# display type determines weather to return a list with the simple game summary or links to scorecard.
# If showAll parameter is true, print all games regardless of numgames parameter.
def urlList():
	htmlString = openLink(BASE_URL+"/ci/engine/match/index.html?view=live")
	# if(htmlString == None):
	# 	sys.exit(-1)
	soup = BeautifulSoup(htmlString, "html.parser")
	numberOfLiveGames = htmlString.count("<div class=\"match-info\">")  #find the number of live games.
	resultList = summaryList(soup, numberOfLiveGames)
	return resultList

urlList()
