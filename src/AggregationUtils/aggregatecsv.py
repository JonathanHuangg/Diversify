## aggregatecsv.py
##
## Aggregate stock market data from multiple CSVs
##

import csv
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", type=str, required=True, help="(str) Input folder; contains all CSVs to aggregate")
parser.add_argument("-o", "--output", type=str, default="./result.csv", required=False, help="(str) Output file; should be path to .csv file (include file name)")
parser.add_argument("-f", "--fill", type=str, default="", required=False, help="(str) Value to populate empty cells.")
args = parser.parse_args()

ANSI_RESET = '\x1b[0m'
ANSI_RED = '\x1b[0;41m'
ANSI_GREEN = '\x1b[32m'

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

def csvToDict(path: str) -> ([str], {str: any}):
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

def mergeData(header1: [str], header2: [str], data1: {str: [str]}, data2: {str: [str]}, fill: str) -> ([str], {str: [str]}):
    newData: {str: [str]} = {}
    newHeader: [str] = header1.copy()
    mergedKeys: set = set()
    # merge header
    for col in header2: newHeader.append(col)

    # merge key sets for data
    for key in list(data1.keys()):
        mergedKeys.add(key)
    for key in list(data2.keys()):
        mergedKeys.add(key)
    
    for key in mergedKeys:
        newData[key] = []
        if not key in data1:
            if len(header1) > 0: print(ANSI_RED + " WARNING " + ANSI_RESET, key, "missing fields", header1)
            for _ in header1:
                newData[key].append(fill)
        else:
            for item in data1[key]:
                newData[key].append(item)

        if not key in data2:
            if len(header2) > 0: print(ANSI_RED + " WARNING " + ANSI_RESET, key, "missing fields", header2)
            for _ in header2:
                newData[key].append(fill)
        else:
            for item in data2[key]:
                newData[key].append(item)
    return (newHeader, newData)

def main(input: str, output: str, fill: str):
    files: [str] = os.listdir(input)
    resultHeader: [str] = []
    resultData: {str: [str]} = {}
    for file in files:
        csvPath: str = os.path.join(input, file)
        csvConversionResult = csvToDict(csvPath)
        if csvConversionResult is None:
            return
        header = csvConversionResult[0]
        csvDict = csvConversionResult[1]
        mergedResult = mergeData(resultHeader, header, resultData, csvDict, fill)
        if mergedResult is None:
            return
        resultHeader = mergedResult[0]
        resultData = mergedResult[1]
    print("Successfully merged CSV files!")
    saveDictionaryAsCSV(resultHeader, resultData, output)

main(args.input, args.output, args.fill)