## normalize.py
##
## Normalize and clean CSV data
##
## Arguments:
## -i/--input  : (str) Input file; the CSV to normalize
## -o/--output : (str) Output file; should be path to .csv file (include file name)
##

import csv
import argparse
import math

ANSI_RESET = '\x1b[0m'
ANSI_RED = '\x1b[0;41m'
ANSI_YELLOW = '\x1b[0;43m'
ANSI_GREEN = '\x1b[0;42m'

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", type=str, required=True, help="(str) Input folder; contains all CSVs to aggregate")
parser.add_argument("-o", "--output", type=str, default="./result.csv", required=False, help="(str) Output file; should be path to .csv file (include file name)")
args = parser.parse_args()

def saveDictionaryAsCSV(header: [str], dict: {str: [str]}, outputPath: str):
    with open(outputPath, 'w') as csvFile:
        writer = csv.writer(csvFile)
        csvHeader = ["Symbol"]
        for item in header:
            csvHeader.append(item)
        writer.writerow(csvHeader)
        for ticker, metrics in dict.items():
            metrics.insert(0, ticker)
            writer.writerow(metrics)

def csvToDict(path: str) -> ([str], {str: [str]}):
    result: {str: any} = {}
    resultHeader: [str] = []
    with open(path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        header = None
        for line in reader:
            if header is None:
                header = line
                if line[0] != "Symbol":
                    print(ANSI_RED + " ERROR " + ANSI_RESET + " Invalid CSV format: Should contain header with first column `Symbol`")
                    return None
                for i in range(1, len(line)):
                    resultHeader.append(line[i])
            else:
                if len(line) != len(header):
                    print(ANSI_RED + " ERROR " + ANSI_RESET + " Invalid CSV format: Rows and columns must be uniform.")
                    return None
                symbol: str = line[0]
                result[symbol] = []
                for i in range(1, len(line)):
                    result[symbol].append(line[i])
    return (resultHeader, result)

def normalizeEntry(header: [str], entry: [str], maxVals: [str], minVals: [str]) -> [str]:
    normalizedEntry: [str] = []
    for i in range(0, len(header)):
        normVal: str = ""
        metric: str = header[i]
        if metric == "Volume":
            normVal = str(float(entry[i]) / float(maxVals[i]))
        elif metric == "Market Cap":
            normVal = str(math.log10(float(entry[i])) / math.log10(float(maxVals[i])))
        elif metric == "P/E Ratio":
            if entry[i] == "N/A":
                normVal = "0"
            elif entry[i] == "0":
                normVal = "1"
            else:
                normVal = str(1 / float(entry[i]))
        elif metric == "Volatility":
            normVal = entry[i]
        elif metric == "Description":
            normVal = entry[i].replace("\n"," ")
        else:
            normVal = entry[i]
        normalizedEntry.append(normVal)
    return normalizedEntry

def normalize(header: [str], data: {str: [str]}) -> {str: [str]}:
    result: {str: [str]} = {}

    # calculate maximum values for the parameters that need them
    maxVals: [float] = []
    minVals: [float] = []
    for i in range(0, len(header)):
        maxVals.append(0)
        minVals.append(math.inf)
    for key in list(data.keys()):
        for i in range(0, len(header)):
            if header[i] == "Volume" or header[i] == "Market Cap":
                maxVals[i] = max(maxVals[i], float(data[key][i]))
                minVals[i] = min(minVals[i], float(data[key][i]))

    # normalize each row
    for key in list(data.keys()):
        result[key] = normalizeEntry(header, data[key], maxVals, minVals)
    return result

def main(input: str, output: str):
    originalResult = csvToDict(input)
    header = originalResult[0]
    normalizedData = normalize(header, originalResult[1])

    # validate data and warn for discrepancies
    for symbol, metrics in normalizedData.items():
        for i in range(0, len(header)):
            metricVal = metrics[i]
            if not metricVal.replace('.','',1).replace('-','',1).isdigit():
                print(ANSI_YELLOW + " WARNING " + ANSI_RESET, "Field `" + header[i] + "` for `" + symbol + "` is not a number.")
            elif float(metricVal) == 0 and header[i] != "P/E Ratio":
                print(ANSI_YELLOW + " WARNING " + ANSI_RESET, "Field `" + header[i] + "` for `" + symbol + "` is 0.")

    saveDictionaryAsCSV(header, normalizedData, output)
    print(ANSI_GREEN + " SUCCESS " + ANSI_RESET, "Normalized", len(normalizedData), "entries with", len(header), "parameters.")

main(args.input, args.output)