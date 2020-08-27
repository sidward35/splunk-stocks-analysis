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
		output += " ticker="+ticker+" current_price="+str(quote_json.get('c'))+" high_price="+str(quote_json.get('h'))+" low_price="+str(quote_json.get('l'))+" open_price="+str(quote_json.get('o'))+" prev_close_price="+str(quote_json.get('pc'))

		fins = requests.get('https://finnhub.io/api/v1/stock/metric?symbol='+ticker+'&metric=all&token=brqivm7rh5rc4v2pmq8g')
		fins_json = json.loads(str(fins.json()).replace('\'','"').replace('None','"None"').replace('True','"True"').replace('False','"False"'))
		fins_json = fins_json["metric"]
		output += " 52WeekHigh="+str(fins_json.get('52WeekHigh'))+" 52WeekLow="+str(fins_json.get('52WeekLow'))+" beta="+str(fins_json.get('beta'))+" 52WeekPriceReturnDaily="+str(fins_json.get('52WeekPriceReturnDaily'))+" 26WeekPriceReturnDaily="+str(fins_json.get('26WeekPriceReturnDaily'))+" 13WeekPriceReturnDaily="+str(fins_json.get('13WeekPriceReturnDaily'))+" bookValuePerShareAnnual="+str(fins_json.get('bookValuePerShareAnnual'))+" bookValuePerShareQuarterly="+str(fins_json.get('bookValuePerShareQuarterly'))+" bookValueShareGrowth5Y="+str(fins_json.get('bookValueShareGrowth5Y'))+" capitalSpendingGrowth5Y="+str(fins_json.get('capitalSpendingGrowth5Y'))+" cashFlowPerShareAnnual="+str(fins_json.get('cashFlowPerShareAnnual'))+" ebitdAnnual="+str(fins_json.get('ebitdAnnual'))+" epsGrowthQuarterlyYoy="+str(fins_json.get('epsGrowthQuarterlyYoy'))+" marketCapitalization="+str(fins_json.get('marketCapitalization'))+" netIncomeCommonAnnual="+str(fins_json.get('netIncomeCommonAnnual'))+" netProfitMargin5Y="+str(fins_json.get('netProfitMargin5Y'))+" netProfitMarginAnnual="+str(fins_json.get('netProfitMarginAnnual'))+" peNormalizedAnnual="+str(fins_json.get('peNormalizedAnnual'))+" priceRelativeToSP50052Week="+str(fins_json.get('priceRelativeToS&P50052Week'))+" priceRelativeToSP50026Week="+str(fins_json.get('priceRelativeToS&P50026Week'))+" priceRelativeToSP50013Week="+str(fins_json.get('priceRelativeToS&P50013Week'))+" priceRelativeToSP5004Week="+str(fins_json.get('priceRelativeToS&P5004Week'))+" revenueAnnual="+str(fins_json.get('revenueAnnual'))+" revenueGrowth3Y="+str(fins_json.get('revenueGrowth3Y'))+" revenueGrowth5Y="+str(fins_json.get('revenueGrowth5Y'))+" revenueGrowthQuarterlyYoy="+str(fins_json.get('revenueGrowthQuarterlyYoy'))+" roi5Y="+str(fins_json.get('roi5Y'))+" roiAnnual="+str(fins_json.get('roiAnnual'))

		aggr = requests.get('https://finnhub.io/api/v1/scan/technical-indicator?symbol='+ticker+'&resolution=D&token=brqivm7rh5rc4v2pmq8g')
		aggr_json = json.loads(str(aggr.json()).replace('\'','"').replace('None','"None"').replace('True','"True"').replace('False','"False"'))
		aggr_json = aggr_json["technicalAnalysis"]
		output += " signal="+str(aggr_json.get('signal')).replace(" ","_")
		if(aggr_json.get('count')!='None'):
			output += " buy_count="+str(aggr_json["count"]["buy"])+" neutral_count="+str(aggr_json["count"]["neutral"])+" sell_count="+str(aggr_json["count"]["sell"])

		senti = requests.get('https://finnhub.io/api/v1/news-sentiment?symbol='+ticker+'&token=brqivm7rh5rc4v2pmq8g')
		senti_json = json.loads(str(senti.json()).replace('\'','"').replace('None','"None"').replace('True','"True"').replace('False','"False"'))
		if(senti_json.get('buzz')!='None'):
			output += " newsArticleCount="+str(senti_json["buzz"]["articlesInLastWeek"])+" avgWeeklyArticleCount="+str(senti_json["buzz"]["weeklyAverage"])+" buzz="+str(senti_json["buzz"]["buzz"])
		if(senti_json.get('sentiment')!='None'):
			output += " bearSentiment="+str(senti_json["sentiment"]["bearishPercent"])+" bullSentiment="+str(senti_json["sentiment"]["bullishPercent"])
		output += " companyNewsScore="+str(senti_json.get('companyNewsScore'))+" sectorAvgNewsScore="+str(senti_json.get('sectorAverageNewsScore'))+" sectorAvgBullishPercent="+str(senti_json.get('sectorAverageBullishPercent'))

		export_json(output)


arg_list = sys.argv
if len(arg_list) > 1:
	sys.argv.pop(0)
	for input in sys.argv:
		get_basic_info(str(input))
else:
	get_basic_info('')

si.outputStreamResults(results)
