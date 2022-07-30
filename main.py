import os
import shutil
import argparse
from module import Twitterscraping, do_lda, extract_content, negaposi, do_lda

def main():
    out_dir = "./out"
    parser = argparse.ArgumentParser(description="do lda")
    parser.add_argument("-r", "--reset", help="Clear output file and retry scraping.", action="store_true")
    args = parser.parse_args()
    if args.reset or not os.path.exists(out_dir):
        if os.path.exists(out_dir):
            shutil.rmtree(out_dir)
            os.mkdir(out_dir)
        print("twitter scraping...")
        Twitterscraping(out_dir)
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