'''
Author: Teeron Hajebi Tabrizi
Date: 05/10/2022

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
import matplotlib.pyplot as plt
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

# Isolate the data from the combined JSON file created in the pull_data method
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
        elif key == "netDebt":
            for key, value in value.items():
                if value != None:
                    metrics["netDebt"] = value
        else:
            metrics["commercialPaper"] = 0

    # This is a constant metric calculated by subtracting the return rate of AA bonds by the inflation rate
    # Source: U.S. Department of the Treasury
    metrics["riskFreeRatePerAnnum"] = RISK_FREE_RATE_PER_ANNUM

    # Source: U.S. Department of the Treasury
    metrics["expectedReturnOfTheMarketPerAnnum"] = EXPECTED_RETURN_OF_THE_MARKET_PER_ANNUM

    # Source: U.S. Department of the Treasury
    metrics["AABondEffectiveYield"] = AA_BOND_EFFECTIVE_YIELD

    return metrics

# Isolate the data from the combined JSON file created in the pull_data_prev_year method
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

# Method where all of my computations are done using the data extracted from the above methods
def computations(metrics, prevMetrics):
    computations = {}

    # Non Operating Profit Less Adjusted for Taxes
    NOPLAT = (metrics["ebitda"]) * (1 - (metrics["incomeTaxExpense"] / metrics["ebitda"]))
    computations["NOPLAT"] = NOPLAT

    investedCapital = (metrics["totalCurrentAssets"] - metrics["totalCurrentLiabilities"])
    computations["investedCapital"] = investedCapital

    investedCapitalOverRevenue = computations["investedCapital"] / metrics["revenue"]
    computations["investedCapitalOverRevenue"] = investedCapitalOverRevenue

    # To find the invested capital of the previous year
    investedCapitalPrevYear = (prevMetrics["totalCurrentAssets"] - prevMetrics["totalCurrentLiabilities"])
    computations["investedCapitalPrevYear"] = investedCapitalPrevYear

    newNetInvestment = computations["investedCapital"] - computations["investedCapitalPrevYear"]
    computations["newNetInvestment"] = newNetInvestment

    operatingFreeCashFlow = computations["NOPLAT"] - computations["newNetInvestment"]
    computations["operatingFreeCashFlow"] = operatingFreeCashFlow

    # The levered rate is the internal rate of return of a string of cash flows with financing included
    leveredRate = (metrics["averageBeta"]) * (1 + (metrics["longTermDebt"] / metrics["marketCap"]))
    computations["leveredRate"] = leveredRate

    # How a security/asset grows in relation to the overall market
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

    # Multiply by 0.9 to account for overestimation as many companies had
    # very profitable years during covid. The flip side is that some also
    # had very rough years. These projections are incredibly rough
    netEntepriseValue = abs(computations["discountedFreeCashFlow"] + future_discounted_free_cash_flow(metrics, projected_metrics(metrics, prevMetrics))) * 0.7
    computations["netEntepriseValue"] = netEntepriseValue

    # Value changes here for some reason when I take the absolute value of the netEnterpriseValue
    # Value of other non-operating assets, non-operating cash, and marketable securities
    VONOANOCMS = (metrics["cashAndCashEquivalents"] + metrics["otherNonCurrentAssets"] + metrics["otherCurrentAssets"])
    computations["VONOANOCMS"] = VONOANOCMS

    grossEnterpriseValue = computations["netEntepriseValue"] + computations["VONOANOCMS"]
    computations["grossEnterpriseValue"] = grossEnterpriseValue

    # Generally under stated as many of the debt metrics
    # are not part of GAAP (Generally Accepted Accounting Principles),
    # making it difficult to calculate debt broadly
    debt = (metrics["commercialPaper"] + metrics["netDebt"]) / 10
    computations["debt"] = debt

    totalValueOfCommonEquity= computations["grossEnterpriseValue"] - computations["debt"]
    computations["totalValueOfCommonEquity"] = totalValueOfCommonEquity

    # This is where my value per share is computed. Given the above stated errors,
    # it isn't entirely accurate. I believe if I had more time (if I wasn't sick), I could
    # have made a web scraper myself that could take data off of the SEC's website to use
    DCFValuePerShare = computations["totalValueOfCommonEquity"] / metrics["outstandingShares"] * 10
    computations["DCFValuePerShare"] = DCFValuePerShare

    return computations

# Method where, using my previous data, I find the rate of change from last year to the year
# my data is from, adding one to it, and multiplying that with my current year's data
# to project for the next year. This is flawed given market volatility in 2021, so growth rates
# are likely not sustainable, and losses will most probably not last too long. This just exacerbates
# a single year's trend, making it not very useful. However, this is the best method without spending
# $10,000 on the Bloomberg terminal or creating a neural network to predict my data.
# This is also the reason why my program is not awfully accurate.
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

# Using the projected metrics and data from the current year, I calculate the discounted
# free cash flow in the following years, which is integral to my final calculation. This is
# where my inaccuracy begins.
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

# Parse my data from JSON files. Taken from Financial Modelling Prep
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
    for i in range(-10,10):
        dateRange.append(str(date[:7] + str(int(date[7:]) + i)))

    for key, value in sharePrice.items():
        if key == "historical":
            for index in range(len(value)):
                if value[index]["date"] in dateRange:
                    print("Value on", value[index]["date"], ":", value[index]["close"])
                    return value[index]["close"]

# Compares my computed DCF share price to the actual share price on the date of the
# release of the balance sheet.
def compare(computations, sharePrice):
    print("Predicted Share Price :", computations["DCFValuePerShare"])
    print("Difference :", computations["DCFValuePerShare"] - sharePrice)

# Creates a list comprised of all of the tickers of the companies in the NASDAQ 100.
def ticker_list():
    NASDAQListURL = "https://financialmodelingprep.com/api/v3/nasdaq_constituent?apikey=82e32bddd70d4deecdf507b9a13b2867"
    NASDAQList = get_jsonparsed_data(NASDAQListURL)

    tickerList = []

    for index in range(len(NASDAQList)):
        tickerList.append(NASDAQList[index]["symbol"])

    return tickerList

if __name__ == "__main__":

    # Loop through tickers to find their DCF valuation disparity
    userInput = True
    if userInput == False:
        tickerList = ticker_list()
        companyData = {}
        for ticker in tickerList:
            try:
                print(ticker)
                data = pull_data(ticker)
                prevData = pull_data_prev_year(ticker)
                metrics = isolate_data(data)
                sharePrice = share_price(ticker, metrics)
                metrics["marketCap"] = sharePrice * metrics["outstandingShares"]
                prevMetrics = isolate_data_prev_year(prevData)
                computation = computations(metrics, prevMetrics)
                compare(computation, sharePrice)
                companyData[ticker] = computation["DCFValuePerShare"] - sharePrice
            # Account for all possible errors because it will be difficult to make every
            # possible company work.
            except TypeError:
                print("Not Computable With Given Data - TypeError")
            except IndexError:
                print("Not Computable With Given Data - IndexError")
            except KeyError:
                print("Not Computable With Given Data - KeyError")
            except ValueError:
                print("Not Computable With Given Data - ValueError")

        #companyData = dict(sorted(companyData.items(), key=lambda item: item[1]))

        companySymbols = list(companyData.keys())
        sharePriceDifference = list(companyData.values())

        # Pulled from GeeksForGeeks
        # (Poorly) Displays the tickers and disparity between DCF Price and actual.
        fig, ax = plt.subplots(figsize=(16, 9))
        ax.barh(companySymbols, sharePriceDifference)
        for s in ['top', 'bottom', 'left', 'right']:
            ax.spines[s].set_visible(False)
        ax.xaxis.set_ticks_position('none')
        ax.yaxis.set_ticks_position('none')
        ax.xaxis.set_tick_params(pad=15)
        ax.yaxis.set_tick_params(pad=20)
        ax.grid(b=True, color='grey', linestyle='-.', linewidth=0.5, alpha=0.2)
        ax.invert_yaxis()
        for i in ax.patches:
            plt.text(i.get_width() + 0.2, i.get_y() + 0.5, str(round((i.get_width()), 2)), fontsize=6, fontweight='bold', color='grey')
        ax.set_title("Share Price Difference Per Company (NASDAQ)", loc="left", )
        fig.text(0.9, 0.15, "Teeron Hajebi Tabrizi", fontsize=12, color="grey", ha="right", va="bottom", alpha=0.7)
        plt.show()

    # For a specific company. (User selected)
    else:
        ticker = input("Input ticker: ")
        data = pull_data(ticker)
        prevData = pull_data_prev_year(ticker)
        metrics = isolate_data(data)
        sharePrice = share_price(ticker, metrics)
        metrics["marketCap"] = sharePrice * metrics["outstandingShares"]
        prevMetrics = isolate_data_prev_year(prevData)
        computations = computations(metrics, prevMetrics)
        compare(computations, sharePrice)
