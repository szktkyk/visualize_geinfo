import polars as pl
import os
import glob
import config
from modules import weight_score
import csv

def main():
    # llm_counts.csvを読み込む
    df_llm_counts = pl.read_csv("./app_data/llm_counts.csv")
    df_llm_counts = df_llm_counts.with_columns(df_llm_counts["gene"].str.to_uppercase().alias("gene"))
    print(df_llm_counts.height)

    # score.tsvを読み込む
    file = glob.glob(os.path.join("./app_data", "score*"))
    if file[0].endswith(".tsv"):
        df_score = pl.read_csv(file[0], sep="\t")
    else:
        df_score = pl.read_csv(file[0])
    df_score = df_score.with_columns(df_score["gene"].str.to_uppercase().alias("gene"))
    print(df_score.height)

    merged_df = df_llm_counts.join(df_score, on="gene")
    print(merged_df.height)
    selected_df = merged_df.select(config.selected_columns)
    print(selected_df.height)
    selected_df.write_csv("./app_data/llm_scores.csv")
    weighted_jsonl_data = weight_score.add_weight()
    df_weighted = pl.DataFrame(weighted_jsonl_data)
    df = selected_df.join(df_weighted, on="gene", how="inner")
    df.write_csv("./app_data/app_scores.csv")
   


def detect_file_type(filename):
    file_extension = os.path.splitext(filename)[1]
    if file_extension.lower() == '.tsv':
        return "tsv"
    elif file_extension.lower() == '.csv':
        return "csv"
    else:
        return 'unknown' 
    
if __name__ == "__main__":
    main()