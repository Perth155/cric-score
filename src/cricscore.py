#!/usr/bin/env python
import sys
import requests
import urlmanager
import argparse
import fonts
import timer

global f # font class object.
global currentHighlight # stores the most recent live commentry. Skips if repeat detected.
global inactivityCount # time in 30 secs of no updates from espncricinfo website.

def printList(inNum, inList, inTeamName):
	global f
	gamesIgnored = 0
	for i in range(inNum):
		if(((inTeamName.lower() not in inList[i]["innings1"].lower()) and (inTeamName.lower() not in inList[i]["innings2"].lower()))):
			gamesIgnored+=1
			continue  #The team we were looking for is not playing any games.

		for keys,values in inList[i].items():
			print(values)
		print("\n")
	if(gamesIgnored == inNum):
		print("No games found for team : "+f.BG_RED+f.FG_WHITE+inTeamName+f.ANSI_RESET)



# print the titles of all ongoing matches
def displayLiveMatchSelection(matches, trim):
	print("Select the index of the match you want to get live score and commentry, (default: 1)")
	for i, entry in enumerate(matches):
		print(str(i+1) + " "+entry["title"] + "\n" + entry["innings1"] + "\t" + entry["innings2"]+"\n")
		if(i == trim-1):
			break



# handles command line arguments and flags
def user_opts():
	descLine1 = "Cricscore is not affiliated with espncricinfo. Please report any bugs to: abrar.a.amin@gmail.com. "
	descLine2 = "URL: https://www.github.com/Perth155/cric-score. To uninstall run: cricscore_uninstall"
	parser = argparse.ArgumentParser(description=descLine1+descLine2)
	parser.add_argument(
				"-a", "--all",
				help="Display all live game summaries.",
				action = "store_true"
	)
	parser.add_argument(
				"-c", "--count",
				type = int,
				default = -1,
				help="Print number of games specified by count."
	)
	parser.add_argument(
				"-f",
				"--fontstyle",
				help="Use stylized fonts to print results.",
				action = "store_true"
	)
	parser.add_argument(
				"-l",
				"--listner",
				help="Initiates a listener to one live game.",
				action = "store_true"
	)
	parser.add_argument(
				"-r", "--result",
				action="store_true",
	 			help="Display results of recently finished matches."
	)
	parser.add_argument("-t", "--team", type=str, default="", help="Search by team name.")
	parser.add_argument("-s", "--scorecard", metavar="", help="Display full scorecard of the match(es) [UNIMPLEMENTED.]")

	args = parser.parse_args()
	return args




def liveCommentry(jsonURL):
	global currentHighlight, inactivityCount
	#print(jsonURL)
	data = urlmanager.getJSObject(jsonURL)
	matchUrl = jsonURL[:-4]+"html"
	display = (data["description"] +"\n"+data["match"]["current_summary"] + "\n" + data["live"]["status"] + "\n"+matchUrl+"\n\n")
	if(currentHighlight == display):
		inactivityCount+=1
		print("No updates...")
	else:
		print(display)
		currentHighlight = display   #updates currentHighlight global var with the most recent text displayed to console.



# Starts the live match listener that refreshes the scores every 30 seconds. Exits by default at 5 minutes of inactivity.
def startListner(gameList, gameIndex):
	global currentHighlight, inactivityCount
	currentHighlight = ""
	if(gameIndex == ""):
		gameIndex = 1
	try:
		matchUrl = gameList[int(gameIndex)-1]["url"]
	except:
		sys.stderr.write("Invalid selection.\n")
		return
	jsonURL = matchUrl[:-4]+"json"
	inactivityCount = 0

	liveCommentry(jsonURL)
	rt = timer.RepeatTimer(30, liveCommentry, jsonURL)

	inArg = input(f.BG_RED+f.FG_WHITE+"Refresh interval = 30s; Press Q to stop listner:"+f.ANSI_RESET+"\n")
	if(inArg.lower() == 'q'):
		rt.stop()
	return






#def main(numgames = 3, displayType = "summary", team = "", showAll = False, showDetailedScoreCard = False, showLive = False):
def main():
	global f
	options = user_opts()
	f = fonts.fonts()
	fStyle = True
	showPastResult = False
	if(not options.fontstyle):
		f.disable()
		fStyle = False
	if(options.result):
		showPastResult = True
	gameList = urlmanager.urlList(fStyle, showPastResult)
	numberOfLiveGames = len(gameList)
	if(numberOfLiveGames == 0):
		print("No games were retreived.")
		sys.exit(0)
	if(options.count == -1):
		trim = numberOfLiveGames #showing results for all games.
	elif(options.count <= numberOfLiveGames and options.count > 0):
		trim = options.count
	else:
		sys.stderr.write(f.BG_RED+f.FG_WHITE+"There are live scores available for "+str(numberOfLiveGames) + " games at the moment." +
		f.ANSI_RESET+"\n"+ "You requested: "+str(options.count)+"\n")
		sys.exit(1)
	if(not options.listner):
		printList(trim, gameList, options.team)
	else:
		displayLiveMatchSelection(gameList, trim)
		matOpt = input("Select option: ")
		startListner(gameList, matOpt)
	sys.exit(0)


if __name__ == "__main__":
    main()
