import sys
from TwitterScraping import Twitterscraping
from extract_content import extract_content

def main():
    args = sys.argv
    Twitterscraping()
    extract_content()
    
    
    

if __name__ == "__main__":
    main()