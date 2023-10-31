## CompanyInfo_AV.py
##
## Given a list of company stock tickers, fetch the description of each company
## from Alpha Vantage and save as a CSV.
##
## Input format should be a text file of tickers separated by \n
##
## Install dependencies: pip install -r requirements_av.txt
## Usage: python CompanyInfo_AV.py -k [API_KEY] -i [INPUT_PATH] -o [OUTPUT_CSV_PATH]
##

import argparse
import requests
import csv

parser = argparse.ArgumentParser()
parser.add_argument("-k", "--key", type=str, required=True)
parser.add_argument("-i", "--input", type=str, required=True)
parser.add_argument("-o", "--output", type=str, default="./result.csv", required=False)
args = parser.parse_args()

ANSI_RESET = '\x1b[0m'
ANSI_RED = '\x1b[0;41m'
ANSI_GREEN = '\x1b[32m'

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

def getCompanyDescription(apiKey: str, ticker: str, showPreview: bool = True) -> str:
    params = {
        'function': 'OVERVIEW',
        'symbol': ticker,
        'apikey': apiKey
    }
    response = requests.get('https://www.alphavantage.co/query', params=params)
    responseJson: {str: any} = response.json()
    # check for possible errors in response
    if response.status_code != 200:
        print(ticker, ": Error with status code ", response.status_code)
        return None
    if responseJson is None:
        print(ticker, ": Received null data")
        return None
    if 'Information' in responseJson:
        print(ticker, ":", responseJson['Information'])
        return None
    if 'Description' not in responseJson:
        print(ticker, ": Could not read description")
        return None
    # success, presumably
    if showPreview:
        print(ticker, ": ", ANSI_GREEN, responseJson['Description'][:32], "...", ANSI_RESET)
    return responseJson['Description']

def getAllCompanyDescriptions(apiKey: str, tickers: [str]) -> {str: str}:
    resultDict: {str: str} = {}
    i: int = 0
    while (i < len(tickers)): # manually cycle through list to allow for retries
        ticker = tickers[i]
        description: str = getCompanyDescription(apiKey, ticker)
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

def readTickers(inputPath: str) -> [str]:
    file = open(inputPath, 'r')
    lines: [str] = file.read().splitlines()
    file.close()
    return lines

def main(apiKey: str, input: str, output: str):
    tickers: [str] = readTickers(input)
    resultDict: {str: str} = getAllCompanyDescriptions(apiKey, tickers)
    saveDictionaryAsCSV(resultDict, output)

main(args.key, args.input, args.output)