import pandas as pd
import snscrape.modules.twitter as sntwitter #pip install snscrape 
import itertools
import os

#ツイート検索するキーワード
def Twitterscraping():
    out_dir = "./out"
    search = "コロナ"
    #Twitterでスクレイピングを行い特定キーワードの情報を取得
    scraped_tweets = sntwitter.TwitterSearchScraper(search).get_items()
    # #最初の10ツイートだけを取得し格
    sliced_scraped_tweets = itertools.islice(scraped_tweets, 1000)
    #データフレームに変換する
    df = pd.DataFrame(sliced_scraped_tweets) 
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)
    df.to_csv("./out/sample.csv")
