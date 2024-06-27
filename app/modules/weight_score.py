import polars as pl
import json
import csv
import config


def add_weight(selected_columns, df_all, jsonl_data):
    """
    This function calculates the total score of each gene based on the selected columns and the weights of each column.
    
    """
    
    new_columns = []
    for column in selected_columns:
        if column != "gene" and column != "count_targeted" and column != "count_deg":
            new_columns.append(column)
        else:
            pass
    
    
    # Find the maximum and minimum values of count_targeted
    count_list = df_all["count_targeted"].to_list()
    max_count_targeted = max(count_list)
    min_count_targeted = min(count_list)

    # Find the maximum and minimum values of count_deg
    count_deg_list = df_all["count_deg"].to_list()
    max_count_deg = max(count_deg_list)
    min_count_deg = min(count_deg_list)

    max_min = []
    # Find the maximum and minimum values of the remaining columns
    for column in new_columns:
        column_list = df_all[column].to_list()
        max_column = max(column_list)
        min_column = min(column_list)  
        max_min.append({"column":column, "max":max_column, "min":min_column})


    new_jsonl_data = []
    for data in jsonl_data:
        # Max-min normalization
        # for count_targeted, less is better. so, we subtract the count from the maximum value of count_targeted
        data["count_targeted"] = ((max_count_targeted - data["count_targeted"]) - min_count_targeted) / (max_count_targeted - min_count_targeted)
        data["count_targeted"] = round(data["count_targeted"] * config.WEIGHTS["count_targeted"], 3)
        data["count_deg"] = (data["count_deg"] - min_count_deg) / (max_count_deg - min_count_deg)
        data["count_deg"] = round(data["count_deg"] * config.WEIGHTS["count_deg"], 3)
        for d in max_min:
            column_name = d["column"]
            if column_name in config.score_invert:
                data[column_name] = ((d["max"] - data[column_name]) - d["min"]) / (d["max"] - d["min"])
                data[column_name] = round(data[column_name] * config.WEIGHTS[column_name], 3)
            else:
                data[column_name] = (abs(data[column_name]) - d["min"]) / (d["max"] - d["min"])
                data[column_name] = round(data[column_name] * config.WEIGHTS[column_name], 3)

        data["total_score"] = round(data["count_targeted"] + data["count_deg"] + sum(data[col] for col in new_columns), 3)   
        new_jsonl_data.append(data)
    return new_jsonl_data

