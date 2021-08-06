# Web App to Get Stock Market Data from AlphaVantage Service

from flask import Flask
from flask import request
import requests

#Create app-object; __name__ assigned "__main__" when run
app = Flask(__name__)

#Function that displays the form
@app.route('/')
def main():
    html = ''#Add code to create html code to display a text box
    html += '<html>\n'
    html += '<body>\n'
    html += '<form method="POST" action="form_input">\n'
    html += 'Stock Symbol: <input type="text" name="stock_symbol" />\n'
    html += '<input type="submit" value="Submit" />'
    html += '</form>\n'
    html += '</body>\n'
    html += '</html>\n'
    #   labeled "Stock Symbol:" and a Submit button.
    return html

#Function that gets stock info from API
#  Returns results in list of two strings
def getStock(symbol):
    baseURL = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&datatype=csv'
    keyPart = '&apikey=' + "EVXJ4JR3X6HYGVRK" #Add API key
    symbolPart = '&symbol=' + symbol
    stockResponse = requests.get(baseURL+keyPart+symbolPart)
    return stockResponse.text  #Return only text part of response

#Function that computes and displays results
@app.route('/form_input', methods=['POST'])
def form_input():
    stockSymbol = request.form['stock_symbol'] #Add code to get the stock symbol from the input form.
    stocks = getStock(stockSymbol) #Add code to call getStock() with the stock symbol,
    stocks = stocks.strip().split()
    if len(stocks) == 2:#   then process the returned data to extract today's
        line1 = stocks[0].split(',')
        line2 = stocks[1].split(',')
        for i in line1:
            if (i == 'symbol'):
                symbolIndex = line1.index('symbol')
                stockSym = str('Stock Symbol: ' + line2[symbolIndex])
        for i in line1:
            if (i == 'open'):
                openIndex = line1.index('open')
                stockOpen = str('Open: ' + line2[openIndex])
        for i in line1:
            if (i == 'high'):
                highIndex = line1.index('high')
                stockHigh = str('High: ' + line2[highIndex])
        for i in line1:
            if (i == 'low'):
                lowIndex = line1.index('low')
                stockLow = str('Low: ' + line2[lowIndex])
        for i in line1:
            if (i == 'price'):
                priceIndex = line1.index('price')
                stockCurrent = str('Current: ' + line2[priceIndex])
        #   starting, high, low, and current prices for the stock,
        html = ''#display them on the web page, AND append them to an
        html += '<html>\n'
        html += '<body>\n'
        html += '<p>' + stockSym + '</p>\n'
        html += '<p>' + stockOpen + '</p>\n'
        html += '<p>' + stockHigh + '</p>\n'
        html += '<p>' + stockLow + '</p>\n'
        html += '<p>' + stockCurrent + '</p>\n'
        html += '<a href="/">Back</a>\n'
        html += '</body>\n'
        html += '</html>\n'
    #   If the stock was not found, tell the user and ask them
    #   to enter another stock symbol.
    #   output file stock_prices.txt.
        stockFile = open("stock_prices.txt", "a")
        stockFile.write(stockSym + '\n' + stockOpen + '\n' + stockHigh + '\n' + stockLow + '\n' + stockCurrent + '\n' + '============================\n')
    else:
        noData = str("Sorry, no stock found with that symbol.\n Please go back and try another stock symbol.")
        html = ''
        html += '<html>\n'
        html += '<body>\n'
        html += '<p>' + noData + '</p>\n'
        html += '<a href="/">Back</a>\n'
        html += '</body>\n'
        html += '</html>\n'
    return html

#Code that starts the app
if __name__ == '__main__':
    app.run()
