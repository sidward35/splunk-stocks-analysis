# Splunk App for Stock Market Analysis
### Splunk app with custom 'quote' command that fetches stock market data from [Finnhub API](https://finnhub.io/docs/api)
Download the latest version of the app [here](https://github.com/sidward35/splunk-stocks-analysis/releases/download/v0.6.2/splunk-stocks-analysis.spl)!

## Command Behavior
- Data will be returned in JSON format
- Each event contains information for an individual symbol

## Search Syntax: `|quote {symbol}`
`{symbol}` = any stock market symbol
- Multiple arguments can be given
- Arguments are optional
  - If no value for `{symbol}` is given, 10 default symbols will be used: SPLK, TSLA, AMZN, NFLX, MSFT, NVDA, INTC, PYPL, VMW, NET

## Usage Examples
- `|quote` returns stock info for the default symbols as noted above
- `|quote SPLK` returns stock info for SPLK
- `|quote SPLK TSLA AMZN` returns stock info for SPLK, TSLA, and AMZN
