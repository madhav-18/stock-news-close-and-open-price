import requests
import schedule
import os

STOCK_NAME = "TSLA"
STOCK_API_KEY = os.environ["STOCK_API_KEY"]
NEWS_API_KEY = os.environ["NEWS_API_KEY"]
COMPANY_NAME = "Tesla Inc"
STOCK_ENDPOINT = "https://www.alphavantage.co/query?"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything?"
bot_token = os.environ["bot_token"]
bot_chatID = os.environ["bot_chatID"]
BOT_ENDPOINT = f"https://api.telegram.org/bot{bot_token}/sendMessage"

stock_parameters = {

    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}

stock_response = requests.get(url=STOCK_ENDPOINT, params=stock_parameters)
stock_data = stock_response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in stock_data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
print(yesterday_closing_price)

day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
print(day_before_yesterday_closing_price)

difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

diff_percentage = round((difference / float(yesterday_closing_price)) * 100)
print(diff_percentage)


def get_articles(output_func):
    news_parameters = {
        "qInTitle": COMPANY_NAME,
        "apiKey": NEWS_API_KEY,
    }

    news_response = requests.get(url=NEWS_ENDPOINT, params=news_parameters)
    articles = news_response.json()["articles"]
    first_three_articles = articles[:3]
    # print(first_three_articles)

    formatted_articles = [f"{STOCK_NAME}: {up_down}{diff_percentage}%\nHeadline: {articles['title']}. \nBrief: {articles['description']}\n\n{articles['url']}" for
                          articles in first_three_articles]
    for article in formatted_articles:
        output_func(article)


def send_msg(text):
    parameters_bot = {
        "chat_id": bot_chatID,
        "text": text,
    }
    send_text = requests.post(BOT_ENDPOINT, params=parameters_bot)
    send_text.raise_for_status()


if abs(diff_percentage) > -0.8:
    get_articles(send_msg)

