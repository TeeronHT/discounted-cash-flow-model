'''
Author: Teeron Hajebi Tabrizi

Description:
The aim of this program will be to calculate the expected value of a company’s shares
using the Discounted Cash Flow (DCF) method. DCF’s have long been utilized by traders
and bankers to evaluate the expected price of a given stock using financial data.
Although they are generally used to complement industry and market knowledge, it allows
one to see the intrinsic value of a company. It can also help when trying to find out
whether a company is over or undervalued. This project will act as a way for me to further
learn about how to implement and use APIs. Financial Modeling Prep has a free API that
lets me pull a company’s various financial metrics. It will mostly be data science oriented
as I will have to fetch and clean vast amounts of information, but I may be able to
incorporate some machine learning by creating projections to estimate the valuation at a
later point in time. If I am able to fulfill some of my reach goals, this application will
serve as a way to find undervalued stocks to purchase or overvalued shares to shares through
the use of the initial DCF model and other metrics.

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

    df1 = pd.DataFrame([balanceSheet[0]])
    df2 = pd.DataFrame([outstandingShares[0]])
    df3 = pd.DataFrame([enterpriseValue[0]])
    df4 = pd.DataFrame([incomeStatement[0]])
    data = pd.concat([df1, df2, df3, df4])
    data.reset_index(drop=True, inplace=True)

    # Sourced from Stack Overflow
    data.to_json(ticker + "Data.json")
    dt = open(ticker + "Data.json")
    return json.load(dt)

def pull_data_prev_years(ticker):
    # Sourced from Financial Modeling Prep
    balanceSheetUrl = "https://financialmodelingprep.com/api/v3/balance-sheet-statement/" + ticker + "?limit=120&apikey=82e32bddd70d4deecdf507b9a13b2867"
    balanceSheet = get_jsonparsed_data(balanceSheetUrl)
    outstandingSharesUrl = "https://financialmodelingprep.com/api/v4/shares_float?symbol=" + ticker + "&apikey=82e32bddd70d4deecdf507b9a13b2867"
    outstandingShares = get_jsonparsed_data(outstandingSharesUrl)
    enterpriseValueUrl = "https://financialmodelingprep.com/api/v3/enterprise-values/" + ticker + "?limit=40&apikey=82e32bddd70d4deecdf507b9a13b2867"
    enterpriseValue = get_jsonparsed_data(enterpriseValueUrl)
    incomeStatementURl = "https://financialmodelingprep.com/api/v3/income-statement/" + ticker + "?limit=120&apikey=82e32bddd70d4deecdf507b9a13b2867"
    incomeStatement = get_jsonparsed_data(incomeStatementURl)

    df1 = pd.DataFrame([balanceSheet[1]])
    df2 = pd.DataFrame([enterpriseValue[1]])
    df3 = pd.DataFrame([incomeStatement[1]])
    data = pd.concat([df1, df2, df3])
    data.reset_index(drop=True, inplace=True)

    # Sourced from Stack Overflow
    data.to_json(ticker + "Data(YearPrev).json")
    dt = open(ticker + "Data(YearPrev).json")
    return json.load(dt)

def isolate_data_prev_year(prevData):
    prevMetrics = {}

    # For year previous
    for key, value in prevData.items():
        if key == "totalCurrentAssets":
            for key, value in value.items():
                if value != None:
                    prevMetrics["totalCurrentAssets"] = value
        elif key == "totalCurrentLiabilities":
            for key, value in value.items():
                if value != None:
                    prevMetrics["totalCurrentLiabilities"] = value

    return prevMetrics

def isolate_data(data):
    metrics = {}

    # For current year
    for key, value in data.items():
        if key == "date":
            for key, value in value.items():
                if value != None:
                    metrics["date"] = value
        elif key == "ebitda":
            for key, value in value.items():
                if value != None:
                    metrics["ebitda"] = value
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

    '''
    previousMetrics = isolate_data_prev_year(data)
    combinedMetrics = metrics | previousMetrics
    return combinedMetrics
    '''

    return metrics

def computations(metrics, prevMetrics):
    computations = {}

    # This value is inflated because I am using ebitda instead of ebita
    NOPLAT = (metrics["ebitda"]) * (1 - (metrics["incomeTaxExpense"] / metrics["ebitda"]))
    computations["NOPLAT"] = NOPLAT
    print("NOPLAT :", str(computations["NOPLAT"]))

    investedCapital = (metrics["totalCurrentAssets"] - metrics["totalCurrentLiabilities"])
    computations["investedCapital"] = investedCapital
    print("investedCapital :", str(computations["investedCapital"]))

    # Review computations
    investedCapitalPrevYear = (prevMetrics["totalCurrentAssets"] - prevMetrics["totalCurrentLiabilities"])
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

def share_price(ticker, metrics):

    sharePriceURL = "https://financialmodelingprep.com/api/v3/historical-price-full/" + ticker + "?serietype=line&apikey=82e32bddd70d4deecdf507b9a13b2867"
    sharePrice = get_jsonparsed_data(sharePriceURL)

    # Create a range of possible dates as the API doesn't have every single day
    # The range is between two days (+/-) of the income statement's release
    date = metrics["date"]
    dateRange = [str(date[:7] + str(int(date[7:]) + 1)), str(date[:7] + str(int(date[7:]) - 1)), str(date[:7] + str(int(date[7:]) + 2)), str(date[:7] + str(int(date[7:]) - 2))]

    for key, value in sharePrice.items():
        if key == "historical":
            for index in range(len(value)):
                if value[index]["date"] in dateRange:
                    print("Value on", value[index]["date"], ":", value[index]["close"])
                    return value[index]["close"]

def compare(valuation, sharePrice):
    return

if __name__ == "__main__":
    ticker = input("Input ticker: ")
    data = pull_data(ticker)
    prevData = pull_data_prev_years(ticker)
    metrics = isolate_data(data)
    prevMetrics = isolate_data_prev_year(prevData)
    computations = computations(metrics, prevMetrics)
    #valuation = valuation(computations())
    sharePrice = share_price(ticker, metrics)
    #compare(valuation, sharePrice)
