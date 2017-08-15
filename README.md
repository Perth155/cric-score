# cricscore
Scrape live cricket results from espncricinfo

## Pre-requisites
* python3 (version 3.4)
* python3-pip
* BeautifulSoup (package name: ```beautifulsoup4```), Alternatively:
```
pip install -r requirements.txt
```

## Usage
* To run the script on Linux
```
./cricscore [args]
```

## Optional Arguments
```
  -h, --help            show this help message and exit
  -a, --all             Display all live game summaries.
  -c COUNT, --count COUNT
                        Print number of games specified by count.
  -f, --fontstyle       Use stylized fonts to print results.
  -l, --listner         Initiates a listener to one live game.
  -r, --result          Display results of recently finished matches.
  -t TEAM, --team TEAM  Search by team name.
  -s , --scorecard      Display full scorecard of the match(es)
                        [UNIMPLEMENTED.]
```

## Installation
* Run the shell script ```installer.sh```
to install cricscore (requires root previliges).
Usage: ```cricscore [args]```
To uninstall run ```cricscore_uninstall```
