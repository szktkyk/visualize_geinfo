import polars as pl
import json
import os


def main():
    # output.arrowを作成する
    # llm結果がリストになっているので、strに変換する
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
    # arrowファイルの書き出し   
    df_llm.write_ipc("./app_data/output.arrow")


    # scores.arrowを作成する
    df_score = pl.read_csv("./app_data/app_scores.csv")
    df_score.write_ipc("./app_data/scores.arrow")


def file_exists(directory, filename):
    filepath = os.path.join(directory, filename)
    return os.path.isfile(filepath)


if __name__ == "__main__":
    main()