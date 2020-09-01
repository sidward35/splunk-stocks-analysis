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
	row['_raw'] = json.dumps(content)
	results.append(row)

def get_basic_info(stock):
	if(stock==''):
		tickers = ["SPLK", "TSLA", "AMZN", "NFLX", "MSFT", "NVDA", "INTC", "PYPL", "VMW", "NET"]
	else:
		tickers=[stock]

	for ticker in tickers:
		output = {}
		output['ticker'] = ticker

		quote = requests.get('https://finnhub.io/api/v1/quote?symbol='+ticker+'&token=brqivm7rh5rc4v2pmq8g')
		quote_json = json.loads(str(quote.json()).replace('\'','"').replace('None','"None"').replace('True','"True"').replace('False','"False"'))
		output['quote'] = quote_json

		fins = requests.get('https://finnhub.io/api/v1/stock/metric?symbol='+ticker+'&metric=all&token=bt4oq4f48v6um6kgq5gg')
		fins_json = json.loads(str(fins.json()).replace('\'','"').replace('None','"None"').replace('True','"True"').replace('False','"False"'))
		fins_json = fins_json["metric"]
		output['financials'] = fins_json

		aggr = requests.get('https://finnhub.io/api/v1/scan/technical-indicator?symbol='+ticker+'&resolution=D&token=bt6pumf48v6oqmgq7j1g')
		aggr_json = json.loads(str(aggr.json()).replace('\'','"').replace('None','"None"').replace('True','"True"').replace('False','"False"'))
		aggr_json = aggr_json["technicalAnalysis"]
		output['technicalAnalysis'] = aggr_json

		senti = requests.get('https://finnhub.io/api/v1/news-sentiment?symbol='+ticker+'&token=bt6pv3n48v6oqmgq7j70')
		senti_json = json.loads(str(senti.json()).replace('\'','"').replace('None','"None"').replace('True','"True"').replace('False','"False"'))
		output['sentiment'] = senti_json

		export_json(output)


arg_list = sys.argv
if len(arg_list) > 1:
	sys.argv.pop(0)
	for input in sys.argv:
		get_basic_info(str(input))
else:
	get_basic_info('')

si.outputStreamResults(results)
