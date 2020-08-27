import requests
import time
import json
import sys
import splunk.Intersplunk as si

results = []

def export_json(content):
	row={}
	row['_time'] = str(time.time())
	row['host'] = 'stock_market_analysis'
	row['source'] = 'finnhub_api'
	row['sourcetype'] = 'api'
	row['_raw'] = content
	results.append(row)

def get_basic_info(stock):
	if(stock==''):
		tickers = ["SPLK", "TSLA", "AMZN", "NFLX", "MSFT", "NVDA", "INTC", "PYPL", "VMW", "NET"]
	else:
		tickers=[stock]

	for ticker in tickers:
		output = "outputType=quote"

		quote = requests.get('https://finnhub.io/api/v1/quote?symbol='+ticker+'&token=brqivm7rh5rc4v2pmq8g')
		quote_json = json.loads(str(quote.json()).replace('\'','"').replace('None','"None"').replace('True','"True"').replace('False','"False"'))
		output += " ticker="+ticker+" current_price="+str(quote_json["c"])+" high_price="+str(quote_json["h"])+" low_price="+str(quote_json["l"])+" open_price="+str(quote_json["o"])+" prev_close_price="+str(quote_json["pc"])

		fins = requests.get('https://finnhub.io/api/v1/stock/metric?symbol='+ticker+'&metric=all&token=brqivm7rh5rc4v2pmq8g')
		fins_json = json.loads(str(fins.json()).replace('\'','"').replace('None','"None"').replace('True','"True"').replace('False','"False"'))
		fins_json = fins_json["metric"]
		output += " 52WeekHigh="+str(fins_json["52WeekHigh"])+" 52WeekLow="+str(fins_json["52WeekLow"])+" beta="+str(fins_json["beta"])+" 52WeekPriceReturnDaily="+str(fins_json["52WeekPriceReturnDaily"])+" 26WeekPriceReturnDaily="+str(fins_json["26WeekPriceReturnDaily"])+" 13WeekPriceReturnDaily="+str(fins_json["13WeekPriceReturnDaily"])+" bookValuePerShareAnnual="+str(fins_json["bookValuePerShareAnnual"])+" bookValuePerShareQuarterly="+str(fins_json["bookValuePerShareQuarterly"])+" bookValueShareGrowth5Y="+str(fins_json["bookValueShareGrowth5Y"])+" capitalSpendingGrowth5Y="+str(fins_json["capitalSpendingGrowth5Y"])+" cashFlowPerShareAnnual="+str(fins_json["cashFlowPerShareAnnual"])+" epsGrowthQuarterlyYoy="+str(fins_json["epsGrowthQuarterlyYoy"])+" marketCapitalization="+str(fins_json["marketCapitalization"])+" netProfitMargin5Y="+str(fins_json["netProfitMargin5Y"])+" netProfitMarginAnnual="+str(fins_json["netProfitMarginAnnual"])+" peNormalizedAnnual="+str(fins_json["peNormalizedAnnual"])+" priceRelativeToSP50052Week="+str(fins_json["priceRelativeToS&P50052Week"])+" priceRelativeToSP50026Week="+str(fins_json["priceRelativeToS&P50026Week"])+" priceRelativeToSP50013Week="+str(fins_json["priceRelativeToS&P50013Week"])+" priceRelativeToSP5004Week="+str(fins_json["priceRelativeToS&P5004Week"])+" revenueGrowth3Y="+str(fins_json["revenueGrowth3Y"])+" revenueGrowth5Y="+str(fins_json["revenueGrowth5Y"])+" revenueGrowthQuarterlyYoy="+str(fins_json["revenueGrowthQuarterlyYoy"])+" roi5Y="+str(fins_json["roi5Y"])+" roiAnnual="+str(fins_json["roiAnnual"])

		aggr = requests.get('https://finnhub.io/api/v1/scan/technical-indicator?symbol='+ticker+'&resolution=D&token=brqivm7rh5rc4v2pmq8g')
		aggr_json = json.loads(str(aggr.json()).replace('\'','"').replace('None','"None"').replace('True','"True"').replace('False','"False"'))
		aggr_json = aggr_json["technicalAnalysis"]
		output += " signal="+str(aggr_json["signal"]).replace(" ","_")+" buy_count="+str(aggr_json["count"]["buy"])+" neutral_count="+str(aggr_json["count"]["neutral"])+" sell_count="+str(aggr_json["count"]["sell"])

		senti = requests.get('https://finnhub.io/api/v1/news-sentiment?symbol='+ticker+'&token=brqivm7rh5rc4v2pmq8g')
		senti_json = json.loads(str(senti.json()).replace('\'','"').replace('None','"None"').replace('True','"True"').replace('False','"False"'))
		output += " newsArticleCount="+str(senti_json["buzz"]["articlesInLastWeek"])+" avgWeeklyArticleCount="+str(senti_json["buzz"]["weeklyAverage"])+" buzz="+str(senti_json["buzz"]["buzz"])+" companyNewsScore="+str(senti_json["companyNewsScore"])+" sectorAvgNewsScore="+str(senti_json["sectorAverageNewsScore"])+" bearSentiment="+str(senti_json["sentiment"]["bearishPercent"])+" bullSentiment="+str(senti_json["sentiment"]["bullishPercent"])+" sectorAvgBullishPercent="+str(senti_json["sectorAverageBullishPercent"])

		export_json(output)


arg_list = sys.argv
if len(arg_list) > 1:
	sys.argv.pop(0)
	for input in sys.argv:
		get_basic_info(str(input))
else:
	get_basic_info('')

si.outputStreamResults(results)
