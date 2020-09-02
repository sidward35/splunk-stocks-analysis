# Splunk App for Stock Market Analysis
### Splunk app with custom 'quote' command that fetches stock market data from [Finnhub API](https://finnhub.io/docs/api)
Download the latest version of the app [here](https://github.com/sidward35/splunk-stocks-analysis/releases/download/v0.7.1/splunk-stocks-analysis.spl)!

![Pre-built dashboard](https://i.imgur.com/vQhmrwY.png)

## Command Behavior
- Data will be returned in JSON format
- Each event contains information for an individual symbol

## Search Syntax: `|quote {symbol}`
`{symbol}` = any stock market symbol ('DJIA' is not a real symbol, but can also be used as an argument to get all 30 stocks in it)
- Multiple arguments can be given; any duplicate arguments will be removed
- Arguments are optional
  - If no value for `{symbol}` is given, 10 default symbols will be used: SPLK, TSLA, AMZN, NFLX, MSFT, NVDA, INTC, PYPL, VMW, NET

## Usage Examples
- `|quote` returns stock info for the default symbols as noted above
- `|quote SPLK` returns stock info for SPLK
- `|quote SPLK DJIA AMZN` returns stock info for SPLK, all 30 stocks in the DJIA, and AMZN
