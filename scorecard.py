import json 
import requests
from pprint import pprint

def getScoreCardDictionary(url):
	try:
		r = requests.get(inURL)
	except:
		sys.stderr.write("Couldn't open "+inURL)
		return
	dataText = r.text

	with open dataText as data_file:
		data = json.load(data_file)
	return data


def generateScoreCard():
	matchDictionary = getScoreCardDictionary("http://www.espncricinfo.com/vijay-hazare-trophy-2016-17/engine/match/1053829.json")

	pprint(matchDictionary)
