import itertools
import os
from random import sample
import pandas as pd
import snscrape.modules.twitter as sntwitter #pip install snscrape 
import oseti
import numpy as np
from oseti.oseti import Analyzer

import pandas as pd

ana = Analyzer()

def Twitterscraping():
    """
    Retrieve 25,000 texts containing "Corona" from users, user profiles, hashtags, searches, tweets (single or threaded), list posts, and trends. Then output to csv file.
    Filename is "scraping_results.csv".
    """
    out_dir = "./out"
    search = "コロナ" # ツイート検索するキーワード
    # Twitterでスクレイピングを行い特定キーワードの情報を取得
    scraped_tweets = sntwitter.TwitterSearchScraper(search).get_items()
    # 最初の25000ツイートだけを取得し格納する
    sliced_scraped_tweets = itertools.islice(scraped_tweets, 25000)
    # データフレームに変換する
    df = pd.DataFrame(sliced_scraped_tweets)
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)
    df.to_csv("./out/sample.csv")


def extract_content():
    """
    "scraping_results.csv" have various data such as URL, date, ID, etc.
    Extract only contents.
    """
    out_dir = "./out/"
    df = pd.read_csv(out_dir+"sample.csv")
    con = df["content"]
    con.to_csv(out_dir+"content.csv", index=False)
    
def judge(text):
    """
    Judges text as negative-positive.
    Args:
        text (String): contents(include tweets, hashtags and replies.)

    Returns:
        int: score(Closer to -1 is considered positive and closer to -1 is considered negative.)
    """
    try:
        review = ana.analyze(text)
        re_view = np.average(review)
        return re_view
    except:
        return 1

def negaposi():
    """_summary_
    """
    out_dir = "./out/"
    df = pd.read_csv(out_dir+"content.csv")
    for t in df["content"]:
        if t==0:
            print("空白")
    df['negaposi'] = df['content'].map(judge)
    df = df[df["negaposi"]<0]
    df.to_csv(out_dir+"nega.csv",index=False)