import json
import polars as pl
import csv
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from modules import synonyms, search_gem_llm, weight_score
import config
# import glob


def main():
    directory = "./app_data"
    if file_exists(directory, "llm.jsonl"):
        # load llm data
        with open("./app_data/llm.jsonl") as f:
            llm_data = [json.loads(l) for l in f.readlines()]
    else:
        print("llm.jsonl not found")
        return
    
    if file_exists(directory, "gene.txt"):
        # load gene list
        with open("./app_data/gene.txt") as f:
            gene_list = f.read().splitlines()
    else:
        print("gene.txt not found")
        return
    if file_exists(directory, "synonyms.csv"):
        # load synonyms data
        synonyms_df = pl.read_csv("./app_data/synonyms.csv")
        synonyms_data = synonyms_df.to_dicts()
    else:
        print("creating a list of synonyms for the gene list")
        synonyms.make_synonyms(gene_list, config.taxonomy_id, "./app_data/synonyms.csv")
        print("synonyms.csv has been created")
        synonyms_df = pl.read_csv("./app_data/synonyms.csv")
        synonyms_data = synonyms_df.to_dicts()

    if file_exists(directory, "llm_counts.csv"):
        print("llm_counts.csv already exists")

    else:
        print("counting for targted gene cases in llm data")
        gene_list = [gene.lower() for gene in gene_list]
        results = search_gem_llm.search_gem_llm(gene_list, llm_data, synonyms_data)
        
        field_name = [
            "gene",
            "count_targeted",
            "count_deg",
            "genome_editing_tools",
            "genome_editing_events"
        ]

        with open("./app_data/llm_counts.csv", "w",) as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=field_name)
            writer.writeheader()
            writer.writerows(results)
        
    # load llm_counts.csv
    df_llm_counts = pl.read_csv("./app_data/llm_counts.csv")
    df_llm_counts = df_llm_counts.with_columns(df_llm_counts["gene"].str.to_uppercase().alias("gene"))
    # print(df_llm_counts.height)

    if file_exists(directory, "score.tsv"):
        # load score data
        # file = glob.glob(os.path.join("./app_data", "score*"))
        # if file[0].endswith(".tsv"):
        df_score = pl.read_csv("./app_data/score.tsv", sep="\t")
        # else:
        #     df_score = pl.read_csv(file[0])
        df_score = df_score.with_columns(df_score["gene"].str.to_uppercase().alias("gene"))
        # print(df_score.height)
    else:
        print("score.tsv not found")
        return

    if file_exists(directory, "app_scores.csv"):
        print("app_scores.csv already exists")

    else:
        merged_df = df_llm_counts.join(df_score, on="gene")
        # print(merged_df.height)
        selected_df = merged_df.select(config.selected_columns)
        # print(selected_df.height)
        selected_df.write_csv("./app_data/llm_scores.csv")
        selected_df.write_ndjson("./app_data/llm_scores.jsonl")
        with open('./app_data/llm_scores.jsonl') as f:
            jsonl_data = [json.loads(l) for l in f.readlines()]
        weighted_jsonl_data = weight_score.add_weight(config.selected_columns, selected_df, jsonl_data)
        df_weighted = pl.DataFrame(weighted_jsonl_data)
        df = selected_df.join(df_weighted, on="gene", how="inner")
        new_columns = []
        for col in df.columns:
            if col.endswith("_right"):
                new_columns.append(col.replace("_right", "_weighted"))
            else:
                new_columns.append(col)  
        df.columns = new_columns
        df.write_csv("./app_data/app_scores.csv")
        
    if file_exists(directory, "output.arrow"):
        print("output.arrow already exists")

    else:
        # create output.arrow
        # covert it to str 
        if file_exists("./app_data", "llm_str.jsonl"):
            df_llm = pl.read_ndjson("./app_data/llm_str.jsonl")

        else:
            with open('./app_data/llm.jsonl') as f:
                jsonl_data = [json.loads(l) for l in f.readlines()]
            new_jsonl_list = []
            for jsonl in jsonl_data:
                jsonl["targeted_genes"] = ", ".join(jsonl["targeted_genes"])
                jsonl["differentially_expressed_genes"] = ", ".join(jsonl["differentially_expressed_genes"])
                jsonl["species"] = ", ".join(jsonl["species"])
                jsonl["genome_editing_tools"] = ", ".join(jsonl["genome_editing_tools"])
                jsonl["genome_editing_event"] = ", ".join(jsonl["genome_editing_event"])
                new_jsonl_list.append(jsonl)
            with open('./app_data/llm_str.jsonl', 'w') as f:
                f.writelines([json.dumps(l) for l in new_jsonl_list])
            df_llm = pl.read_ndjson("./app_data/llm_str.jsonl")  
        df_llm.write_ipc("./app_data/output.arrow")

    if file_exists(directory, "scores.arrow"):
        print("scores.arrow already exists")

    else:
        # create scores.arrow
        df_score = pl.read_csv("./app_data/app_scores.csv")
        df_score.write_ipc("./app_data/scores.arrow")  
    
    print("all files have been prepared")


def detect_file_type(filename):
    file_extension = os.path.splitext(filename)[1]
    if file_extension.lower() == '.tsv':
        return "tsv"
    elif file_extension.lower() == '.csv':
        return "csv"
    else:
        return 'unknown' 


def file_exists(directory, filename):
    filepath = os.path.join(directory, filename)
    return os.path.isfile(filepath)


if __name__ == "__main__":
    main()