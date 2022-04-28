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

# Imports
import json
from urllib.request import urlopen
import pandas as pd

# This is a constant metric calculated by subtracting the return rate of AA bonds by the inflation rate
# Source: U.S. Department of the Treasury
RISK_FREE_RATE_PER_ANNUM = 0.015

# Source: U.S. Department of the Treasury
EXPECTED_RETURN_OF_THE_MARKET_PER_ANNUM = 0.064

# Source: U.S. Department of the Treasury
AA_BOND_EFFECTIVE_YIELD = 0.0175

# Call API and concatenate JSON files for current year data
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
    profileURL = "https://financialmodelingprep.com/api/v3/profile/" + ticker + "?apikey=82e32bddd70d4deecdf507b9a13b2867"
    profile = get_jsonparsed_data(profileURL)

    df1 = pd.DataFrame([balanceSheet[0]])
    df2 = pd.DataFrame([outstandingShares[0]])
    df3 = pd.DataFrame([enterpriseValue[0]])
    df4 = pd.DataFrame([incomeStatement[0]])
    df5 = pd.DataFrame([profile[0]])
    data = pd.concat([df1, df2, df3, df4, df5])
    data.reset_index(drop=True, inplace=True)

    # Sourced from Stack Overflow
    data.to_json(ticker + "Data.json")
    dt = open(ticker + "Data.json")
    return json.load(dt)

# Call API and concatenate JSON files for last year's data
def pull_data_prev_year(ticker):
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
        elif key == "outstandingShares":
            for key, value in value.items():
                if value != None:
                    metrics["outstandingShares"] = value
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
        elif key == "beta":
            for key, value in value.items():
                if value != None:
                    metrics["averageBeta"] = value
        elif key == "longTermDebt":
            for key, value in value.items():
                if value != None:
                    metrics["longTermDebt"] = value

    # This is a constant metric calculated by subtracting the return rate of AA bonds by the inflation rate
    # Source: U.S. Department of the Treasury
    metrics["riskFreeRatePerAnnum"] = RISK_FREE_RATE_PER_ANNUM

    # Source: U.S. Department of the Treasury
    metrics["expectedReturnOfTheMarketPerAnnum"] = EXPECTED_RETURN_OF_THE_MARKET_PER_ANNUM

    # Source: U.S. Department of the Treasury
    metrics["AABondEffectiveYield"] = AA_BOND_EFFECTIVE_YIELD

    return metrics

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

def computations(metrics, prevMetrics):
    computations = {}

    # This value is inflated because I am using ebitda instead of ebita
    NOPLAT = (metrics["ebitda"]) * (1 - (metrics["incomeTaxExpense"] / metrics["ebitda"]))
    computations["NOPLAT"] = NOPLAT
    print("NOPLAT :", str(computations["NOPLAT"]))

    investedCapital = (metrics["totalCurrentAssets"] - metrics["totalCurrentLiabilities"])
    computations["investedCapital"] = investedCapital
    print("investedCapital :", str(computations["investedCapital"]))

    investedCapitalOverRevenue = computations["investedCapital"] / metrics["revenue"]
    computations["investedCapitalOverRevenue"] = investedCapitalOverRevenue
    print("investedCapitalOverRevenue :", str(computations["investedCapitalOverRevenue"]))

    investedCapitalPrevYear = (prevMetrics["totalCurrentAssets"] - prevMetrics["totalCurrentLiabilities"])
    computations["investedCapitalPrevYear"] = investedCapitalPrevYear
    print("investedCapitalPrevYear :", str(computations["investedCapitalPrevYear"]))

    newNetInvestment = computations["investedCapital"] - computations["investedCapitalPrevYear"]
    computations["newNetInvestment"] = newNetInvestment
    print("newNetInvestment :", str(computations["newNetInvestment"]))

    operatingFreeCashFlow = computations["NOPLAT"] - computations["newNetInvestment"]
    computations["operatingFreeCashFlow"] = operatingFreeCashFlow
    print("operatingFreeCashFlow :", str(computations["operatingFreeCashFlow"]))

    leveredRate = (metrics["averageBeta"]) * (1 + (metrics["longTermDebt"] / metrics["marketCap"]))
    computations["leveredRate"] = leveredRate
    print("leveredRate :", str(computations["leveredRate"]))

    averageBeta = ((computations["leveredRate"]) + (metrics["averageBeta"])) / 2
    computations["averageBeta"] = averageBeta
    print("averageBeta :", str(computations["averageBeta"]))

    CAPM = metrics["riskFreeRatePerAnnum"] + computations["averageBeta"] * (metrics["expectedReturnOfTheMarketPerAnnum"] - metrics["riskFreeRatePerAnnum"])
    computations["CAPM"] = CAPM
    print("CAPM :", str(computations["CAPM"] * 100) + "%")

    equityLinkedCostOfCapital = metrics["marketCap"] / (metrics["longTermDebt"] + metrics["marketCap"]) * computations["CAPM"]
    computations["equityLinkedCostOfCapital"] = equityLinkedCostOfCapital
    print("equityLinkedCostOfCapital :", str(computations["equityLinkedCostOfCapital"]))

    debtLinkedCostOfCapital = metrics["longTermDebt"] / (metrics["longTermDebt"] + metrics["marketCap"]) * metrics["AABondEffectiveYield"] * (1 - metrics["incomeTaxExpense"] / metrics["ebitda"])
    computations["debtLinkedCostOfCapital"] = debtLinkedCostOfCapital
    print("debtLinkedCostOfCapital :", str(computations["debtLinkedCostOfCapital"]))

    WACC = computations["debtLinkedCostOfCapital"] + computations["equityLinkedCostOfCapital"]
    computations["WACC"] = WACC
    print("WACC :", str(computations["WACC"]))

    discountFactor = 1 / (1 + computations["WACC"])
    computations["discountFactor"] = discountFactor
    print("discountFactor :", str(computations["discountFactor"]))

    discountedFreeCashFlow = computations["operatingFreeCashFlow"] * computations["discountFactor"]
    computations["discountedFreeCashFlow"] = discountedFreeCashFlow
    print("discountedFreeCashFlow :", str(computations["discountedFreeCashFlow"]))

    return computations

def get_jsonparsed_data(url):
    # Sourced from Financial Modeling Prep
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
    prevData = pull_data_prev_year(ticker)
    metrics = isolate_data(data)
    sharePrice = share_price(ticker, metrics)
    metrics["marketCap"] = sharePrice * metrics["outstandingShares"]
    prevMetrics = isolate_data_prev_year(prevData)
    computations = computations(metrics, prevMetrics)
    #valuation = valuation(computations())
    #compare(valuation, sharePrice)
