import sys
import urlmanager
#import scorecard
import argparse
import fonts

#from pprint import pprint



def printList(inNum, inList, inTeamName, isScoreCardDisplayed):
	gamesIgnored = 0
	for i in range(inNum):
		if(((inTeamName.lower() not in inList[i]["innings1"].lower()) and (inTeamName.lower() not in inList[i]["innings2"].lower()))):
			gamesIgnored+=1
			continue  #The team we were looking for is not playing any games.

		for keys,values in inList[i].items():
			print(values)
		print("\n")
	if(gamesIgnored == inNum):
		print("No games found for team : "+fonts.BG_RED+fonts.FG_WHITE+inTeamName+fonts.ANSI_RESET)



def getScorecardURLs():
	return
	#TO DO


def main(numgames = 3, displayType = "summary", team = "", showAll = False, showDetailedScoreCard = False):
	gameList = urlmanager.urlList()
	numberOfLiveGames = len(gameList)

	if(showAll == True):
		trim = numberOfLiveGames #showing results for all games.
	elif(numgames < numberOfLiveGames):
		trim = numgames
	else:
		sys.stderr.write(fonts.BG_RED+fonts.FG_WHITE+"There are live scores available for "+str(numberOfLiveGames) + " games at the moment." + fonts.ANSI_RESET+"\n"+
			"You requested: "+str(numgames)+"\n")
		trim = 0
	printList(trim, gameList, team, showDetailedScoreCard)



main(numgames = 10)
