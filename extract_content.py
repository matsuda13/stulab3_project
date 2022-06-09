from random import sample
import pandas as pd

def extract_content():
    out_dir = "./out/"
    df = pd.read_csv(out_dir+"sample.csv")
    con = df["content"]
    con.to_csv(out_dir+"content.csv", index=False)

if __name__ == "__main__":
    extract_content()