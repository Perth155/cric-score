import sys
import urlmanager
import scorecard
import argparse
import fonts



def printList(inNum, inList):
	for i in range(inNum):
		for j in range(len(inList[0])):
			print(inList[i][j])
		print("\n\n")



def main(numgames = 3, displayType = "summary", keyWord = "", showAll = False):
	
	gameList = urlmanager.urlList()
	numberOfLiveGames = len(gameList)

	if(showAll == True):
		trim = numberOfLiveGames #showing results for all games.
	elif(numgames < numberOfLiveGames):
		trim = numgames
	else:
		sys.stderr.write(fonts.RED+"There are live scores available for "+str(numberOfLiveGames) + " games at the moment." + fonts.ANSI_RESET+"\n")
		trim = numberOfLiveGames
	printList(trim, gameList)


main()