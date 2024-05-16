import os
import re
import polars as pl




def get_data_source():
    try:
        print("Creating DATA_SOURCE from arrow file")
        data_source = pl.scan_ipc("../app_data/output.arrow")
        print(data_source)
        return data_source
    except FileNotFoundError:
        print("Arrow file not found")
        return None

def get_data_source_score():
    try:
        print("Creating DATA_SOURCE from arrow file")
        data_source = pl.scan_ipc("../app_data/scores.arrow")
        print(data_source)
        return data_source
    except FileNotFoundError:
        print("Arrow file not found")
        return None


DATA_SOURCE = get_data_source()
column_names = DATA_SOURCE.columns

DATA_SOURCE_SCORE = get_data_source_score()
column_names_scores = DATA_SOURCE_SCORE.columns

def scan_ldf(
    filter_model=None,
    columns=None,
    sort_model=None,
):
    """
    This function start with DATA_SOURCE and add select and filter queries on top
    to generate a LazyFrame

    Parameters
    ----------
    filter_model : dict of {str : str}
            A filter model generated by dash-ag-grid component filters
    columns : list of str
            A list of columns to select

    Returns
    -------
    pl.LazyFrame
    """

    ldf = DATA_SOURCE
    if columns:
        ldf = ldf.select(columns)
    if filter_model:
        expression_list = make_filter_expr_list(filter_model)
        if expression_list:
            filter_query = None
            for expr in expression_list:
                if filter_query is None:
                    filter_query = expr
                else:
                    filter_query &= expr
            ldf = ldf.filter(filter_query)
    return ldf

def scan_ldf_part2(
    filter_model=None,
    columns=None,
    sort_model=None,
):
    """
    This function start with DATA_SOURCE and add select and filter queries on top
    to generate a LazyFrame

    Parameters
    ----------
    filter_model : dict of {str : str}
            A filter model generated by dash-ag-grid component filters
    columns : list of str
            A list of columns to select

    Returns
    -------
    pl.LazyFrame
    """

    ldf = DATA_SOURCE_SCORE
    if columns:
        ldf = ldf.select(columns)
    if filter_model:
        expression_list = make_filter_expr_list(filter_model)
        if expression_list:
            filter_query = None
            for expr in expression_list:
                if filter_query is None:
                    filter_query = expr
                else:
                    filter_query &= expr
            ldf = ldf.filter(filter_query)
    return ldf

def scan_ldf_sort(sortModel, columns):
    ldf = DATA_SOURCE_SCORE
    if columns:
        ldf = ldf.select(columns)
    if sortModel:
        for col in sortModel:
            if col["sort"] == "asc":
                ldf = ldf.sort(col["colId"])
            else:
                ldf = ldf.sort(col["colId"], reverse=True)
    return ldf

def make_filter_expr_list(filter_model):
    """
    Genearte all polar filter expressions from filter model

    Parameters
    ----------
    filter_model : dict of {str : str}
            A filter model generated by dash-ag-grid component filters

    Returns
    -------
    list of pl.Expr
    """
    expression_list = []
    for col_name in filter_model:
        if "operator" in filter_model[col_name]:
            if filter_model[col_name]["operator"] == "AND":
                expr1 = parse_column_filter(
                    filter_model[col_name]["condition1"], col_name
                )
                expr2 = parse_column_filter(
                    filter_model[col_name]["condition2"], col_name
                )
                expr = expr1 & expr2
            else:
                expr1 = parse_column_filter(
                    filter_model[col_name]["condition1"], col_name
                )
                expr2 = parse_column_filter(
                    filter_model[col_name]["condition2"], col_name
                )
                expr = expr | expr2
        else:
            expr = parse_column_filter(filter_model[col_name], col_name)
        expression_list.append(expr)

    return expression_list


def get_filter_values(col_name):
    """
    Get a list of unique values in a column
    This is used to create categorical filters in dash-ag-grid
    Parameters
    ----------
    col_name : str
            A name of a column in DATA_SOURCE

    Returns
    -------
    list
    """
    return (
        DATA_SOURCE.select(pl.col(col_name))
        .collect()
        .unique()
        .get_columns()[0]
        .to_list()
    )

def parse_column_filter(filter_obj, col_name):
    """
    Build a polars filter expression for a column based on the corrosponding filter item

    Parameters
    ----------
    col_name : str
            A name of a column in DATA_SOURCE

    Returns
    -------
    pl.Expr
    """
    if filter_obj["filterType"] == "set":
        expr = None
        for val in filter_obj["values"]:
            expr |= pl.col(col_name).cast(pl.Utf8).cast(pl.Categorical) == val
    else:
        if filter_obj["filterType"] == "date":
            crit1 = filter_obj["dateFrom"]

            if "dateTo" in filter_obj:
                crit2 = filter_obj["dateTo"]

        else:
            if "filter" in filter_obj:
                crit1 = filter_obj["filter"]
            if "filterTo" in filter_obj:
                crit2 = filter_obj["filterTo"]

        if filter_obj["type"] == "contains":
            lower = (crit1).lower()
            expr = pl.col(col_name).str.to_lowercase().str.contains(lower)

        elif filter_obj["type"] == "notContains":
            lower = (crit1).lower()
            expr = ~pl.col(col_name).str.to_lowercase().str.contains(lower)
        elif filter_obj["type"] == "startsWith":
            lower = (crit1).lower()
            expr = pl.col(col_name).str.starts_with(lower)

        elif filter_obj["type"] == "notStartsWith":
            lower = (crit1).lower()
            expr = ~pl.col(col_name).str.starts_with(lower)

        elif filter_obj["type"] == "endsWith":
            lower = (crit1).lower()
            expr = pl.col(col_name).str.ends_with(lower)

        elif filter_obj["type"] == "notEndsWith":
            lower = (crit1).lower()
            expr = ~pl.col(col_name).str.ends_with(lower)

        elif filter_obj["type"] == "blank":
            expr = pl.col(col_name).is_null()

        elif filter_obj["type"] == "notBlank":
            expr = ~pl.col(col_name).is_null()

        elif filter_obj["type"] == "equals":
            expr = pl.col(col_name) == crit1

        elif filter_obj["type"] == "notEqual":
            expr = pl.col(col_name) != crit1

        elif filter_obj["type"] == "lessThan":
            expr = pl.col(col_name) < crit1

        elif filter_obj["type"] == "lessThanOrEqual":
            expr = pl.col(col_name) <= crit1

        elif filter_obj["type"] == "greaterThan":
            expr = pl.col(col_name) > crit1

        elif filter_obj["type"] == "greaterThanOrEqual":
            expr = pl.col(col_name) >= crit1

        elif filter_obj["type"] == "inRange":
            if filter_obj["filterType"] == "date":
                expr = (pl.col(col_name) >= crit1) & (pl.col(col_name) <= crit2)
            else:
                expr = (pl.col(col_name) >= crit1) & (pl.col(col_name) <= crit2)
        else:
            None

    return expr
