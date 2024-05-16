# TODO: 汎用性がないので書き換える

import polars as pl
import json
import csv
import config


def add_weight():
    df_all = pl.read_csv("./app_data/llm_scores.csv")
    df_all.write_ndjson("./app_data/llm_scores.jsonl")

    with open('./app_data/llm_scores.jsonl') as f:
        jsonl_data = [json.loads(l) for l in f.readlines()]

    # count_targetedの最大値と最小値を求める
    count_list = df_all["count_targeted"].to_list()
    max_count_targeted = max(count_list)
    min_count_targeted = min(count_list)

    # count_degの最大値と最小値を求める
    count_deg_list = df_all["count_deg"].to_list()
    max_count_deg = max(count_deg_list)
    min_count_deg = min(count_deg_list)

    # PD_scoreの最大値と最小値を求める
    PDscore_list = df_all["PD_score"].to_list()
    max_PDscore = max(PDscore_list)
    min_PDscore = min(PDscore_list)

    # ON_scoreの絶対値の最大値と最小値を求める
    ONscore_list = df_all["ON_score"].to_list()
    ONscore_list = [abs(i) for i in ONscore_list]
    max_ONscore = max(ONscore_list)
    min_ONscore = min(ONscore_list)


    new_jsonl_data = []
    for data in jsonl_data:
        # countの最大値からcountを引いた値を新しいcountとする
        data["count_targeted"] = ((max_count_targeted - data["count_targeted"]) - min_count_targeted) / (max_count_targeted - min_count_targeted)
        data["count_targeted"] = round(data["count_targeted"] * config.WEIGHTS["count_targeted"], 3)
        data["count_deg"] = (data["count_deg"] - min_count_deg) / (max_count_deg - min_count_deg)
        data["count_deg"] = round(data["count_deg"] * config.WEIGHTS["count_deg"], 3)
        # ONscoreは絶対値の値を新しいONscoreとする
        data["ON_score"] = (abs(data["ON_score"]) - min_ONscore) / (max_ONscore - min_ONscore)
        data["ON_score"] = round(data["ON_score"] * config.WEIGHTS["ON_score"], 3)
        # NU_PMIDs_PDの最大値からNU_PMIDs_PDを引いた値を新しいNU_PMIDs_PDとする
        data["PD_score"] = ((max_PDscore - data["PD_score"]) - min_PDscore)/ (max_PDscore - min_PDscore)
        data["PD_score"] = round(data["PD_score"] * config.WEIGHTS["PD_score"], 3)
        data["total_score"] = round(data["count_targeted"] + data["count_deg"] + data["PD_score"] + data["ON_score"], 3)    
        new_jsonl_data.append(data)
    return new_jsonl_data


