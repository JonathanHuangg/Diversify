## get_yf_data.py
##
## Get stock market data from Yahoo Finance
##
## Install dependencies: pip install -r requirements.txt
##
## Arguments
## -i/--input     : (str) Input file; should be txt file of all tickers separated by \n
## -o/--output    : (str) Output file; should be path to .csv file (include file name)
## -d/--delay     : (int) Delay each query by the specified number of seconds to avoid excessive requests 
## -s/--start     : (int) Start queries at a certain point in the input list. Useful for recovery.
## -t/--tempcache : (bool) Determine whether a temporary CSV should be stored after each query (./temp.csv)
##
##  Minimum Syntax: python get_yf_data.py -i [TICKERS_LIST]
## Extended Syntax: python get_yf_data.py -i [TICKERS_LIST] -o [OUTPUT_CSV] -d [DELAY_SECS] -s [START_INDEX] -t [BOOL_STORE_TEMP_CSV]
##

import csv
import argparse
import requests
import time

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", type=str, required=True, help="(str) Input file; should be txt file of all tickers separated by \\n")
parser.add_argument("-o", "--output", type=str, default="./result.csv", required=False, help="(str) Output file; should be path to .csv file (include file name)")
parser.add_argument("-d", "--delay", type=int, default=0, required=False, help="(int) Delay each query by the specified number of seconds to avoid excessive requests ")
parser.add_argument("-s", "--start", type=int, default=0, required=False, help="(int) Start queries at a certain point in the input list. Useful for recovery.")
parser.add_argument("-t", "--tempcache", type=bool, default=False, required=False, help="(bool) Determine whether a temporary CSV should be stored after each query (./temp.csv)")
args = parser.parse_args()

ANSI_RESET = '\x1b[0m'
ANSI_RED = '\x1b[0;41m'
ANSI_GREEN = '\x1b[0;42m'

def saveDictionaryAsCSV(dict: {str: str}, outputPath: str):
    with open(outputPath, 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(["Symbol", "Volume", "Market Cap", "P/E Ratio"])
        for ticker, metrics in dict.items():
            writer.writerow([ticker, metrics["volume"], metrics["market_cap"], metrics["pe_ratio"]])

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
    
def readTickers(inputPath: str) -> [str]:
    file = open(inputPath, 'r')
    lines: [str] = file.read().splitlines()
    file.close()
    return lines

def getQuoteManually(ticker: str, cookies: {str: any}, crumb: str) -> {str: any}:
    result: {str: any} = {}
    headers: {str: str} = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
    response = requests.get("https://query2.finance.yahoo.com/v7/finance/quote?symbols=" + ticker + "&crumb=" + crumb, headers=headers, cookies=cookies)
    # check for possible errors in response
    if response.status_code != 200:
        print(ticker, ": Error with status code ", response.status_code)
        return None
    if response.content is None:
        print(ticker, ": Received null data")
        return None
    responseJson: {str: any} = response.json()

    # only retrieve relevant metrics
    if not (("quoteResponse" in responseJson) and ("result" in responseJson["quoteResponse"]) and len(responseJson["quoteResponse"]["result"]) >= 1):
        print(ticker, ": Malformed response", responseJson)
        return None
    
    fullQuote = responseJson["quoteResponse"]["result"][0]
    if "marketCap" in fullQuote:
        result["market_cap"] = fullQuote["marketCap"]
    else:
        print(ANSI_RED + " WARNING " + ANSI_RESET + " Unexpectedly missing `market_cap` for", ticker)
        result["market_cap"] = "**ERR**"

    if "averageDailyVolume3Month" in fullQuote:
        result["volume"] = fullQuote["averageDailyVolume3Month"]
    else:
        print(ANSI_RED + " WARNING " + ANSI_RESET + " Unexpectedly missing `volume` for", ticker)
        result["volume"] = "**ERR**"

    if "trailingPE" in fullQuote:
        result["pe_ratio"] = fullQuote["trailingPE"]
    else:
        result["pe_ratio"] = "N/A"

    return result

def main(input: str, output: str, delay: int, start: int, temp: bool):
    tickers: [str] = readTickers(input)
    result: {str: {str: any}} = {}
    didAbort: bool = False

    # in order to access YF API, we must obtain a cookie and a crumb (essentially a token)
    headers: {str: str} = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
    cookieRes = requests.get("https://fc.yahoo.com", headers=headers, allow_redirects=True)
    cookie = list(cookieRes.cookies)[0]
    cookies = {cookie.name: cookie.value}
    crumbRes = requests.get(
            "https://query1.finance.yahoo.com/v1/test/getcrumb",
            headers=headers,
            cookies=cookies,
            allow_redirects=True,
        )
    crumb = crumbRes.text

    print("Fetch", len(tickers) - start, "symbols with", delay, "second delay")
    i = start # start iteration at specified index (typically 0 unless previously aborted)
    successes = 0
    while i < len(tickers): # manually iterate to allow for skipping/rewinding
        print(i, ": Fetching", tickers[i])
        quote = getQuoteManually(tickers[i], cookies, crumb)
        if quote is None: # some error occurred
            userAction = promptShouldContinue()
            if userAction == 0: # abort
                didAbort = True
                break
            elif userAction == 1: # retry
                continue
        else: # query successful
            result[tickers[i]] = quote
            if temp:
                saveDictionaryAsCSV(result, "./tmp.csv")
            successes += 1
        i += 1
        time.sleep(delay) # delay to minimize Yahoo flagging excessive requests
    
    # output results and save
    print("RESULTS")
    print("-----------------")
    for key in result:
        print(key, result[key])
    print("-----------------")
    print("Saving to CSV...")
    saveDictionaryAsCSV(result, output)
    if didAbort:
        print(ANSI_RED + " ABORTED " + ANSI_RESET + " To retry at this point, use flag -s", i)
    else:
        print(ANSI_GREEN + " SUCCESS " + ANSI_RESET + " Retrieved metrics for", successes, "symbols.")

main(args.input, args.output, args.delay, args.start, args.tempcache)