## CompanyInfo_Wikipedia.py
##
## Fetch the description of each company in the S&P 500
## from Wikipedia and save as a CSV.
##
## Input format should be a text file of tickers separated by \n
##
## Install dependencies: pip install -r requirements_wikipedia.txt
## Usage: python CompanyInfo_Wikipedia.py
##

import argparse
import requests
from bs4 import BeautifulSoup
import csv

ANSI_RESET = '\x1b[0m'
ANSI_RED = '\x1b[0;41m'
ANSI_GREEN = '\x1b[32m'

parser = argparse.ArgumentParser()
parser.add_argument("-o", "--output", type=str, default="./result.csv", required=False)
args = parser.parse_args()

def saveDictionaryAsCSV(dict: {str: str}, outputPath: str):
    with open(outputPath, 'w') as csvFile:
        writer = csv.writer(csvFile)
        for ticker, description in dict.items():
            writer.writerow([ticker, description])

def promptShouldContinue() -> int:
    while True:
        userResponse: str = input(ANSI_RED + " ERROR " + ANSI_RESET + " Unable to fetch entry. Abort, retry, or skip? [a/r/s]: ")
        userResponse = str.lower(str.strip(userResponse))
        if userResponse == 'a':
            return 0
        elif userResponse == 'r':
            return 1
        elif userResponse == 's':
            return 2

def getCompanyDescription(ticker: str, wikiUrl: str) -> str:
    response = requests.get(wikiUrl)
    soup = BeautifulSoup(response.content, "html.parser")
    articleWrapper = soup.find(id='mw-content-text').findAll()[0]
    articleContent = articleWrapper.findAll('p')

    for i in range(0, len(articleContent)):
        paragraph = articleContent[i].get_text()
        if len(str.strip(paragraph)) != 0:
            print(ticker, ":", paragraph[:32], "...")
            return paragraph
    
    print(ticker, ":", "Unable to get wiki page")
    return None

def getAllCompanyDescriptions(constituents: {str: str}) -> {str: str}:
    resultDict: {str: str} = {}
    i: int = 0
    tickers: [str] = list(constituents.keys())
    while (i < len(tickers)): # manually cycle through list to allow for retries
        ticker = tickers[i]
        description: str = getCompanyDescription(ticker, constituents[ticker])
        if description is not None:
            resultDict[ticker] = description
        else:
            promptResult: int = promptShouldContinue()
            if promptResult == 0:
                print("Saving current results and aborting...")
                break
            elif promptResult == 1:
                i -= 1 # rewind index by 1 and attempt to fetch again
        i += 1

    return resultDict

def getSP500Constituents() -> {str: str}:
    # https://medium.com/@nqabell89/scraping-the-s-p-500-from-wikipedia-with-pandas-beautiful-soup-ba22101cb5ed
    result: {str: str} = {}

    response = requests.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    soup = BeautifulSoup(response.content, "html.parser")
    main_table = soup.find(id='constituents')
    table = main_table.find('tbody').findAll('tr')
    table = table[1:]
    base_url = 'https://en.wikipedia.org'
    for item in table:
        ticker = str(item.findAll('a')[0].get_text())
        url = base_url + str(item.findAll('a')[1]['href'])
        result[ticker] = url
    return result

def main(output: str):
    constituents: {str: str} = getSP500Constituents()
    resultDict: {str: str} = getAllCompanyDescriptions(constituents)
    saveDictionaryAsCSV(resultDict, output)

main(args.output)