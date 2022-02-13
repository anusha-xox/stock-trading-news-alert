import requests
import datetime as dt
import pytz
from twilio.rest import Client

tz_NY = pytz.timezone("Asia/Kolkata")
now = dt.datetime.now(tz_NY)
date = now.date()
print(date)

STOCK = "TSLA"
COMPANY_NAME = "Tesla"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_API = ""

NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API = ""

account_sid = ""
auth_token = ""

stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_API,
}

stock_response = requests.get(STOCK_ENDPOINT, params=stock_parameters)
stock_data = stock_response.json()
prev1_close = float(stock_data["Time Series (Daily)"][list(stock_data["Time Series (Daily)"].keys())[0]]["4. close"])
prev2_close = float(stock_data["Time Series (Daily)"][list(stock_data["Time Series (Daily)"].keys())[1]]["4. close"])
change_percent = round(((prev1_close - prev2_close) / prev1_close) * 100, 2)

if change_percent <= -5 or change_percent >= 5:
    if change_percent <= 0:
        change_percent *= -1
        line_1 = f"{STOCK}: 🔻{change_percent}%"
    else:
        line_1 = f"{STOCK}: 🔺{change_percent}%"

    news_parameters = {
        "qInTitle": COMPANY_NAME,
        "sortBy": "publishedAt",
        "apiKey": NEWS_API,
        "language": "en"
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_parameters)
    news_data = news_response.json()

    for i in range(3):
        news_headline = f'Headline: {news_data["articles"][i]["title"]} ({STOCK})'
        news_description = f'Brief: {news_data["articles"][i]["description"]}'
        news_url = news_data["articles"][i]["url"]

        print(line_1)
        print(news_headline)
        print(news_description)
        print(news_url)

        client = Client(account_sid, auth_token)
        message = client.messages \
            .create(
            body=f"\n{line_1}\n{news_headline}\n{news_description}\n{news_url}",
            from_='',  # Trial no.
            to=''
        )

        print(message.status)
