import plotly.graph_objects as go
from plotly import express as px
import polars as pl
import pandas as pd


def fig1():
    """
    create a bar chart of the top 40 genes based on the total score
    """
    df = pl.read_csv("./app_data/app_scores.csv")
    df = df.sort("total_score", reverse=True).head(40)
    # pdf = df.to_pandas()
    # fig1 = px.bar(df, x="gene", y="total")
    fig1 = px.bar(df, x="gene", y="total_score")
    y_min = df["total_score"].min()
    fig1.update_layout(yaxis=dict(range=[y_min-0.1, 1]))

    return fig1






