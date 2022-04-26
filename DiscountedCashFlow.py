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
    sharePriceURL = "https://financialmodelingprep.com/api/v3/historical-price-full/" + ticker + "?serietype=line&apikey=82e32bddd70d4deecdf507b9a13b2867"
    sharePrice = get_jsonparsed_data(sharePriceURL)

    # What I can do is subtract today's date from the date in the income statement and find that index
    '''
    for i in range(sharePrice)
        for key, value in data.items():
            if key == "date":
                for key, value in value.items():
                    if value != None:
                        metrics["date"] = value
    '''

    df1 = pd.DataFrame([balanceSheet[0]])
    df2 = pd.DataFrame([outstandingShares[0]])
    df3 = pd.DataFrame([enterpriseValue[0]])
    df4 = pd.DataFrame([incomeStatement[0]])
    df5 = pd.DataFrame([sharePrice[0]])
    data = pd.concat([df1, df2, df3, df4, df5])
    data.reset_index(drop=True, inplace=True)

    # Sourced from Stack Overflow
    data.to_json(ticker + "Data.json")
    dt = open(ticker + "Data.json")
    return json.load(dt)

def isolate_data(data):
    metrics = {}

    # For current year
    for key, value in data.items():
        if key == "ebitda":
            for key, value in value.items():
                if value != None:
                    metrics["ebitda"] = value
        elif key == "close": # Open the "historical" array, search through the dictionary
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
        elif key == "incomeTaxExpense":
            for key, value in value.items():
                if value != None:
                    metrics["incomeTaxExpense"] = value
        elif key == "totalCurrentAssets":
            for key, value in value.items():
                if value != None:
                    metrics["totalCurrentAssets"] = value
        elif key == "totalCurrentLiabilities":
            for key, value in value.items():
                if value != None:
                    metrics["totalCurrentLiabilities"] = value

    # For year previous

    return metrics

def computations(metrics):
    computations = {}

    # This value is inflated because I am using ebitda instead of ebita
    NOPLAT = (metrics["ebitda"]) * (1 - (metrics["incomeTaxExpense"] / metrics["ebitda"]))
    computations["NOPLAT"] = NOPLAT
    print("NOPLAT :", str(computations["NOPLAT"]))

    investedCapital = (metrics["totalCurrentAssets"] - metrics["totalCurrentLiabilities"])
    computations["investedCapital"] = investedCapital
    print("investedCapital :", str(computations["investedCapital"]))

    investedCapitalPrevYear = (metrics["totalCurrentAssetsPrevYear"] - metrics["totalCurrentLiabilitiesPrevYear"])
    computations["investedCapitalPrevYear"] = investedCapitalPrevYear
    print("investedCapitalPrevYear :", str(computations["investedCapitalPrevYear"]))

    investedCapitalOverRevenue = computations["investedCapital"] / metrics["revenue"]
    computations["investedCapitalOverRevenue"] = investedCapitalOverRevenue
    print("investedCapitalOverRevenue :", str(computations["investedCapitalOverRevenue"]))

    newNetInvestment = computations["investedCapital"] - computations["investedCapitalPrevYear"]
    computations["newNetInvestment"] = newNetInvestment
    print("newNetInvestment :", str(computations["newNetInvestment"]))

    operatingFreeCashFlow = computations["NOPLAT"] - computations["newNetInvestment"]
    computations["operatingFreeCashFlow"] = operatingFreeCashFlow
    print("operatingFreeCashFlow :", str(computations["operatingFreeCashFlow"]))

    return computations

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