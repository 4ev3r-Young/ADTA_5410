# ADTA 5410 Final Project Proposal
### Team VariUNTs: Luis Garcia Fuentes, Sonali Sabnam, Sonam Pohuja, Young Yu <br>
### Project Title: 
Predicting Stock Price Direction Using Sentiment Analysis of News <br>
### Idea/Research Question: 
How effectively can sentiment analysis of news articles and social media content predict the directional movement of daily stock prices for selected companies in the U.S. stock market? <br>
### Rationale and Background: 
Predicting stock prices is notoriously complex due to the dynamic interplay of financial, political, and social factors. However, investor sentiment, which can be shaped by news articles and social media trends, plays a crucial role in market behavior. Today, platforms like Facebook, Twitter, and TikTok dominate the digital landscape, quickly amplifying news and opinions. As public sentiment fluctuates rapidly in response to breaking news—such as company product launches, leadership changes, or world events—these shifts can directly impact stock prices. <br>
For example, unexpected events, such as a change in leadership or a public figure’s death, could trigger rapid investor responses. Consider Tesla: If a pivotal figure like Elon Musk passed away, investors would likely rush to sell shares, anticipating market volatility, and only re-enter the market once stability returns. Our study aims to explore how such sentiment-driven actions influence stock price directions.<br>
### Scope of Work: 
This project will collect and analyze two primary datasets:
- News sentiment data from TBD, focusing on news articles related to selected U.S. companies.
- Stock price data from Yahoo Finance or similar platforms, tracking daily closing prices and their direction.
Target Variables:
- Daily stock closing prices and price direction
- Sentiment scores from news articles and relevant social media posts
Deliverables:
- A forecast of stock price directional movement (gain or loss) for selected companies.
- Analysis of sentiment impact from news and social media trends on stock prices.
- Stretch goal – predicting % price change <br>
Methodology:
Sentiment Analysis, Logistic Regression, and other required methods as needed. TBD <br>


Pre-built models are used to filter financial news and then analyze the article to get a weighted sentiment score. News, historical stock prices and other engineered features will be used to train a custom RNN model to predict stock price direction and % price change. <br>

## Special Thanks

Special Thanks to [Ed and the Team @newscatcherapi](https://www.newscatcherapi.com/) for the student support. You can also find their GitHub [Here.](https://github.com/NewscatcherAPI)


# Acknowledgments ✨

We would like to acknowledge the following projects whose work we have incorporated into this project:

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->

| Package | Contribution | Link |
|---------|--------------|------|
| [python](https://www.python.org/) | Programming language | [Link to Python](https://www.python.org/) |
| [yfinance](https://github.com/ranaroussi/yfinance) | Financial data retrieval | [Link to GitHub](https://github.com/ranaroussi/yfinance) |
| [transformers](https://github.com/huggingface/transformers) | NLP and deep learning models | [Link to GitHub](https://github.com/huggingface/transformers) |
| [scikit-learn](https://github.com/scikit-learn/scikit-learn) | Machine learning library | [Link to GitHub](https://github.com/scikit-learn/scikit-learn) |
| [python-dotenv](https://github.com/theskumar/python-dotenv) | Environment variable management | [Link to GitHub](https://github.com/theskumar/python-dotenv) |
| [pandas](https://github.com/pandas-dev/pandas) | Data manipulation library | [Link to GitHub](https://github.com/pandas-dev/pandas) |
| [ipywidgets](https://github.com/jupyter-widgets/ipywidgets) | Interactive widgets for Jupyter | [Link to GitHub](https://github.com/jupyter-widgets/ipywidgets) |
| [requests](https://github.com/psf/requests) | HTTP requests library | [Link to GitHub](https://github.com/psf/requests) |
| [tf-keras](https://github.com/tensorflow/tensorflow) | Neural networks with TensorFlow | [Link to GitHub](https://github.com/tensorflow/tensorflow) |
| [psycopg2-binary](https://github.com/psycopg/psycopg2) | PostgreSQL database adapter | [Link to GitHub](https://github.com/psycopg/psycopg2) |
| [newscatcherapi](https://github.com/NewscatcherAPI/newscatcherapi-sdk-python) | News scraping API | [Link to GitHub](https://github.com/NewscatcherAPI/newscatcherapi-sdk-python) |


<!-- ALL-CONTRIBUTORS-LIST:END -->




