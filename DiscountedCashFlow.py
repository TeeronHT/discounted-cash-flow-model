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
import math

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
    reportedBSURl = "https://financialmodelingprep.com/api/v3/balance-sheet-statement-as-reported/" + ticker + "?limit=10&apikey=82e32bddd70d4deecdf507b9a13b2867"
    reportedBS = get_jsonparsed_data(reportedBSURl)

    df1 = pd.DataFrame([balanceSheet[0]])
    df2 = pd.DataFrame([outstandingShares[0]])
    df3 = pd.DataFrame([enterpriseValue[0]])
    df4 = pd.DataFrame([incomeStatement[0]])
    df5 = pd.DataFrame([profile[0]])
    df6 = pd.DataFrame([reportedBS[0]])
    data = pd.concat([df1, df2, df3, df4, df5, df6])
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
    enterpriseValueUrl = "https://financialmodelingprep.com/api/v3/enterprise-values/" + ticker + "?limit=40&apikey=82e32bddd70d4deecdf507b9a13b2867"
    enterpriseValue = get_jsonparsed_data(enterpriseValueUrl)
    incomeStatementURl = "https://financialmodelingprep.com/api/v3/income-statement/" + ticker + "?limit=120&apikey=82e32bddd70d4deecdf507b9a13b2867"
    incomeStatement = get_jsonparsed_data(incomeStatementURl)
    reportedBSURl = "https://financialmodelingprep.com/api/v3/balance-sheet-statement-as-reported/" + ticker + "?limit=10&apikey=82e32bddd70d4deecdf507b9a13b2867"
    reportedBS = get_jsonparsed_data(reportedBSURl)

    df1 = pd.DataFrame([balanceSheet[1]])
    df2 = pd.DataFrame([enterpriseValue[1]])
    df3 = pd.DataFrame([incomeStatement[1]])
    df4 = pd.DataFrame([reportedBS[1]])
    data = pd.concat([df1, df2, df3, df4])
    data.reset_index(drop=True, inplace=True)

    # Sourced from Stack Overflow
    data.to_json(ticker + "Data(YearPrev).json")
    dt = open(ticker + "Data(YearPrev).json")
    return json.load(dt)

def isolate_data(data):
    metrics = {}

    # Altenative way to do this: Create a dictionary and iterate through that to find the
    # needed values. Would be a long dictionary though.

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
        elif key == "cashAndCashEquivalents":
            for key, value in value.items():
                if value != None:
                    metrics["cashAndCashEquivalents"] = value
        elif key == "otherNonCurrentAssets":
            for key, value in value.items():
                if value != None:
                    metrics["otherNonCurrentAssets"] = value
        elif key == "otherCurrentAssets":
            for key, value in value.items():
                if value != None:
                    metrics["otherCurrentAssets"] = value
        elif key == "commercialpaper":
            for key, value in value.items():
                if value != None:
                    metrics["commercialPaper"] = value

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
        elif key == "revenue":
            for key, value in value.items():
                if value != None:
                    prevMetrics["revenue"] = value
        elif key == "totalCurrentLiabilities":
            for key, value in value.items():
                if value != None:
                    prevMetrics["totalCurrentLiabilities"] = value
        elif key == "ebitda":
            for key, value in value.items():
                if value != None:
                    prevMetrics["ebitda"] = value
        elif key == "operatingExpenses":
            for key, value in value.items():
                if value != None:
                    prevMetrics["operatingExpenses"] = value
        elif key == "enterpriseValue":
            for key, value in value.items():
                if value != None:
                    prevMetrics["enterpriseValue"] = value
        elif key == "outstandingShares":
            for key, value in value.items():
                if value != None:
                    prevMetrics["outstandingShares"] = value
        elif key == "incomeTaxExpense":
            for key, value in value.items():
                if value != None:
                    prevMetrics["incomeTaxExpense"] = value
        elif key == "beta":
            for key, value in value.items():
                if value != None:
                    prevMetrics["averageBeta"] = value
        elif key == "longTermDebt":
            for key, value in value.items():
                if value != None:
                    prevMetrics["longTermDebt"] = value
        elif key == "commercialpaper":
            for key, value in value.items():
                if value != None:
                    prevMetrics["commercialPaper"] = value


    # This is a constant metric calculated by subtracting the return rate of AA bonds by the inflation rate
    # Source: U.S. Department of the Treasury
    prevMetrics["riskFreeRatePerAnnum"] = RISK_FREE_RATE_PER_ANNUM

    # Source: U.S. Department of the Treasury
    prevMetrics["expectedReturnOfTheMarketPerAnnum"] = EXPECTED_RETURN_OF_THE_MARKET_PER_ANNUM

    # Source: U.S. Department of the Treasury
    prevMetrics["AABondEffectiveYield"] = AA_BOND_EFFECTIVE_YIELD

    return prevMetrics

def computations(metrics, prevMetrics):
    computations = {}

    NOPLAT = (metrics["ebitda"]) * (1 - (metrics["incomeTaxExpense"] / metrics["ebitda"]))
    computations["NOPLAT"] = NOPLAT

    investedCapital = (metrics["totalCurrentAssets"] - metrics["totalCurrentLiabilities"])
    computations["investedCapital"] = investedCapital

    investedCapitalOverRevenue = computations["investedCapital"] / metrics["revenue"]
    computations["investedCapitalOverRevenue"] = investedCapitalOverRevenue

    investedCapitalPrevYear = (prevMetrics["totalCurrentAssets"] - prevMetrics["totalCurrentLiabilities"])
    computations["investedCapitalPrevYear"] = investedCapitalPrevYear

    newNetInvestment = computations["investedCapital"] - computations["investedCapitalPrevYear"]
    computations["newNetInvestment"] = newNetInvestment

    operatingFreeCashFlow = computations["NOPLAT"] - computations["newNetInvestment"]
    computations["operatingFreeCashFlow"] = operatingFreeCashFlow

    leveredRate = (metrics["averageBeta"]) * (1 + (metrics["longTermDebt"] / metrics["marketCap"]))
    computations["leveredRate"] = leveredRate

    averageBeta = ((computations["leveredRate"]) + (metrics["averageBeta"])) / 2
    computations["averageBeta"] = averageBeta

    CAPM = metrics["riskFreeRatePerAnnum"] + computations["averageBeta"] * (metrics["expectedReturnOfTheMarketPerAnnum"] - metrics["riskFreeRatePerAnnum"])
    computations["CAPM"] = CAPM

    equityLinkedCostOfCapital = metrics["marketCap"] / (metrics["longTermDebt"] + metrics["marketCap"]) * computations["CAPM"]
    computations["equityLinkedCostOfCapital"] = equityLinkedCostOfCapital

    debtLinkedCostOfCapital = metrics["longTermDebt"] / (metrics["longTermDebt"] + metrics["marketCap"]) * metrics["AABondEffectiveYield"] * (1 - metrics["incomeTaxExpense"] / metrics["ebitda"])
    computations["debtLinkedCostOfCapital"] = debtLinkedCostOfCapital

    WACC = computations["debtLinkedCostOfCapital"] + computations["equityLinkedCostOfCapital"]
    computations["WACC"] = WACC

    discountFactor = 1 / (1 + computations["WACC"])
    computations["discountFactor"] = discountFactor

    discountedFreeCashFlow = computations["operatingFreeCashFlow"] * computations["discountFactor"]
    computations["discountedFreeCashFlow"] = discountedFreeCashFlow

    netEntepriseValue = abs(computations["discountedFreeCashFlow"] + future_discounted_free_cash_flow(metrics, projected_metrics(metrics, prevMetrics)))
    computations["netEntepriseValue"] = netEntepriseValue
    print(netEntepriseValue)

    # Value changes here for some reason when I take the absolute value of the netEnterpriseValue
    # Value of other non-operating assets, non-operating cash, and marketable securities
    VONOANOCMS = (metrics["cashAndCashEquivalents"] + metrics["otherNonCurrentAssets"] + metrics["otherCurrentAssets"])
    computations["VONOANOCMS"] = VONOANOCMS
    print(VONOANOCMS)

    grossEnterpriseValue = computations["netEntepriseValue"] + computations["VONOANOCMS"]
    computations["grossEnterpriseValue"] = grossEnterpriseValue
    print(grossEnterpriseValue)

    debt = metrics["commercialPaper"] + metrics["longTermDebt"] / 10
    computations["debt"] = debt
    print(debt)

    totalValueOfCommonEquity= computations["grossEnterpriseValue"] - computations["debt"]
    computations["totalValueOfCommonEquity"] = totalValueOfCommonEquity
    print(totalValueOfCommonEquity)

    DCFValuePerShare = computations["totalValueOfCommonEquity"] / metrics["outstandingShares"] * 10
    computations["DCFValuePerShare"] = DCFValuePerShare
    print("DCFValuePerShare :", str(computations["DCFValuePerShare"]))

    return computations

def projected_metrics(metrics, prevMetrics):
    projectedMetrics = {}

    # Finding rate of change of metrics compared to year previous to project
    for key in metrics:
        if metrics[key] != 0:
            try:
                projectedMetrics[key] = (1 + ((metrics[key] - prevMetrics[key])/metrics[key])) * metrics[key]
            except KeyError:
                1 + 1
    return projectedMetrics

def future_discounted_free_cash_flow(prevMetrics, metrics):
    computations = {}

    NOPLAT = (metrics["ebitda"]) * (1 - (metrics["incomeTaxExpense"] / metrics["ebitda"]))
    computations["NOPLAT"] = NOPLAT

    investedCapital = (metrics["totalCurrentAssets"] - metrics["totalCurrentLiabilities"])
    computations["investedCapital"] = investedCapital

    investedCapitalOverRevenue = computations["investedCapital"] / metrics["revenue"]
    computations["investedCapitalOverRevenue"] = investedCapitalOverRevenue

    investedCapitalPrevYear = (prevMetrics["totalCurrentAssets"] - prevMetrics["totalCurrentLiabilities"])
    computations["investedCapitalPrevYear"] = investedCapitalPrevYear

    newNetInvestment = computations["investedCapital"] - computations["investedCapitalPrevYear"]
    computations["newNetInvestment"] = newNetInvestment

    operatingFreeCashFlow = computations["NOPLAT"] - computations["newNetInvestment"]
    computations["operatingFreeCashFlow"] = operatingFreeCashFlow

    leveredRate = (prevMetrics["averageBeta"]) * (1 + (metrics["longTermDebt"] / prevMetrics["marketCap"]))
    computations["leveredRate"] = leveredRate

    averageBeta = ((computations["leveredRate"]) + (prevMetrics["averageBeta"])) / 2
    computations["averageBeta"] = averageBeta

    CAPM = prevMetrics["riskFreeRatePerAnnum"] + computations["averageBeta"] * (prevMetrics["expectedReturnOfTheMarketPerAnnum"] - prevMetrics["riskFreeRatePerAnnum"])
    computations["CAPM"] = CAPM

    equityLinkedCostOfCapital = prevMetrics["marketCap"] / (metrics["longTermDebt"] + prevMetrics["marketCap"]) * computations["CAPM"]
    computations["equityLinkedCostOfCapital"] = equityLinkedCostOfCapital

    debtLinkedCostOfCapital = metrics["longTermDebt"] / (metrics["longTermDebt"] + prevMetrics["marketCap"]) * prevMetrics["AABondEffectiveYield"] * (1 - metrics["incomeTaxExpense"] / metrics["ebitda"])
    computations["debtLinkedCostOfCapital"] = debtLinkedCostOfCapital

    WACC = computations["debtLinkedCostOfCapital"] + computations["equityLinkedCostOfCapital"]
    computations["WACC"] = WACC

    discountFactor = 1 / (1 + computations["WACC"])
    computations["discountFactor"] = discountFactor

    discountedFreeCashFlow = abs(computations["operatingFreeCashFlow"] * computations["discountFactor"])
    computations["discountedFreeCashFlow"] = discountedFreeCashFlow

    return discountedFreeCashFlow

def get_jsonparsed_data(url):
    # Sourced from Financial Modeling Prep
    response = urlopen(url)
    data = response.read().decode("utf-8")
    return json.loads(data)

# This next method is isolated as the API returned the data in a strange format
# making it difficult to sift through along with the other returned files
def share_price(ticker, metrics):

    sharePriceURL = "https://financialmodelingprep.com/api/v3/historical-price-full/" + ticker + "?serietype=line&apikey=82e32bddd70d4deecdf507b9a13b2867"
    sharePrice = get_jsonparsed_data(sharePriceURL)

    # Create a range of possible dates as the API doesn't have every single day
    # The range is between five days (+/-) of the income statement's release
    date = metrics["date"]
    dateRange = []
    for i in range(-5,5):
        dateRange.append(str(date[:7] + str(int(date[7:]) + i)))

    for key, value in sharePrice.items():
        if key == "historical":
            for index in range(len(value)):
                if value[index]["date"] in dateRange:
                    print("Value on", value[index]["date"], ":", value[index]["close"])
                    return value[index]["close"]

def compare(computations, sharePrice):
    print("Actual Share Price :", sharePrice)
    print("Predicted Share Price :", computations["DCFValuePerShare"])
    print("Difference :", computations["DCFValuePerShare"] - sharePrice)

if __name__ == "__main__":
    ticker = input("Input ticker: ")
    data = pull_data(ticker)
    prevData = pull_data_prev_year(ticker)
    metrics = isolate_data(data)
    sharePrice = share_price(ticker, metrics)
    metrics["marketCap"] = sharePrice * metrics["outstandingShares"]
    prevMetrics = isolate_data_prev_year(prevData)
    computations = computations(metrics, prevMetrics)
    compare(computations, sharePrice)
