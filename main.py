import os
import shutil
import argparse
from module import Twitterscraping, do_lda, extract_content, negaposi, do_lda

def main():
    parser = argparse.ArgumentParser(description="do lda")
    parser.add_argument("-r", "--reset", help="Clear output file and retry scraping.", action="store_true")
    args = parser.parse_args()
    if args.reset or not os.path.exists("./out"):
        if os.path.exists("./out"):
            shutil.rmtree("./out")
        print("twitter scraping...")
        Twitterscraping()
        print("extracting...")
        extract_content()
        print("judging...")
        negaposi()

    else:
        print("skip scraping.")
        print("skip extract.")
        print("skip judge.")
    print("topic modeling...")
    do_lda()
    print("complete!")
    

if __name__ == "__main__":
    main()