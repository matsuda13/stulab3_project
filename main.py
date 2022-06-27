import sys
import os
from TwitterScraping import Twitterscraping
from extract_content import extract_content
from negaposi import negaposi

def main():
    args = sys.argv
    if not os.path.exists("./out"):
        print("twitter scraping...")
        Twitterscraping()
    else:
        print("skip scraping.")
    if not os.path.exists("./out/content.csv"):
        print("extracting...")
        extract_content()
    else:
        print("skip extract.")
    print("judging...")
    try:
        negaposi()
        print("complete!")
    except:
        print("something went wrong.")
    
    

if __name__ == "__main__":
    main()