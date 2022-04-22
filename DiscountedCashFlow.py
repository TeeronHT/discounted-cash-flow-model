'''
Author: Teeron Hajebi Tabrizi

Description:
'''

import json
from urllib.request import urlopen
import pandas as pd

def pull_data(ticker):
    # Sourced from Financial Modeling Prep
    balanceSheetUrl = "https://financialmodelingprep.com/api/v3/balance-sheet-statement/" + ticker + "?limit=120&apikey=82e32bddd70d4deecdf507b9a13b2867"
    balanceSheet = get_jsonparsed_data(balanceSheetUrl)
    outstandingSharesUrl = "https://financialmodelingprep.com/api/v4/shares_float?symbol=" + ticker + "&apikey=82e32bddd70d4deecdf507b9a13b2867"
    outstandingShares = get_jsonparsed_data(outstandingSharesUrl)
    enterpriseValueUrl = "https://financialmodelingprep.com/api/v3/enterprise-values/" + ticker + "?limit=40&apikey=82e32bddd70d4deecdf507b9a13b2867"
    enterpriseValue = get_jsonparsed_data(enterpriseValueUrl)
    incomeStatementURl = "https://financialmodelingprep.com/api/v3/income-statement/" + ticker + "?limit=120&apikey=82e32bddd70d4deecdf507b9a13b2867"
    incomeStatement = get_jsonparsed_data(incomeStatementURl)
    currentPriceURL = "https://financialmodelingprep.com/api/v3/quote-short/" + ticker + "?apikey=82e32bddd70d4deecdf507b9a13b2867"
    currentPrice = get_jsonparsed_data(currentPriceURL)

    df1 = pd.DataFrame([balanceSheet[0]])
    df2 = pd.DataFrame([outstandingShares[0]])
    df3 = pd.DataFrame([enterpriseValue[0]])
    df4 = pd.DataFrame([incomeStatement[0]])
    df5 = pd.DataFrame([currentPrice[0]])
    data = pd.concat([df1, df2, df3, df4, df5])
    data.reset_index(drop=True, inplace=True)

    # Sourced from Stack Overflow
    data.to_json(ticker + "Data.json")
    dt = open(ticker + "Data.json")
    return json.load(dt)

def isolate_data(data):
    metrics = {}
    for key, value in data.items():
        #print(key, ':', value)
        if key == "ebitda":
            for key, value in value.items():
                if value != None:
                    metrics["ebitda"] = value
        elif key == "price":
            for key, value in value.items():
                if value != None:
                    metrics["price"] = value
        elif key == "operatingExpenses":
            for key, value in value.items():
                if value != None:
                    metrics["operatingExpenses"] = value
        elif key == "revenue":
            for key, value in value.items():
                if value != None:
                    metrics["revenue"] = value
        elif key == "enterpriseValue":
            for key, value in value.items():
                if value != None:
                    metrics["enterpriseValue"] = value
        elif key == "numberOfShares":
            for key, value in value.items():
                if value != None:
                    metrics["numberOfShares"] = value
    return metrics

def computations(metrics):
    computations{}
    #NOPLAT = (Net Income + Tax + Interest + Non-Operating Gains/Losses) * (1 - (totalTaxExpenses/ebita))
    #computations["NOPLAT"] = NOPLAT
    return

# Sourced from Financial Modeling Prep
def get_jsonparsed_data(url):
    response = urlopen(url)
    data = response.read().decode("utf-8")
    return json.loads(data)

if __name__ == "__main__":
    ticker = input("Input ticker: ")
    data = pull_data(ticker)
    metrics = isolate_data(data)
    valuation = computations(metrics)

    for key, value in metrics.items():
        print(key, ':', value)