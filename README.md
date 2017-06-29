# cric-score
Scrape live cricket results from espncricinfo

## Pre-requisites
* Python3 (version 3.4)
* Python3-pip
* BeautifulSoup (beautifulsoup) download and install using pip
Alternatively
```
pip install -r requirements.txt
```

## Usage
* To run the script on Linux
```
python3 cricscore.py [args]
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
* Linux
