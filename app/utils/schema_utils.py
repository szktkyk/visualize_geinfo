import sys
import os

# Add the parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import config

new_columns = []
for column in config.selected_columns:
    if column != "gene" and column != "count_targeted" and column != "count_deg":
        new_columns.append(column)
    else:
        pass


FILTER_TYPE_DICT = {
    "pmid": "agTextColumnFilter",
    "targeted_genes": "agTextColumnFilter",
    "differentially_expressed_genes": "agTextColumnFilter",
    "species": "agSetColumnFilter",
    "genome_editing_tools": "agSetColumnFilter",
    "genome_editing_event": "agSetColumnFilter",
    "phenotypes": "agTextColumnFilter",
}

FILTER_TYPE_DICT_PART2 = {
    "gene":"agTextColumnFilter",
    "count_targeted":"agNumberColumnFilter",
    "count_deg":"agNumberColumnFilter",
    "count_targeted_weighted":"agNumberColumnFilter",
    "count_deg_weighted":"agNumberColumnFilter",
    "total_score":"agNumberColumnFilter",
}

for column in new_columns:
    FILTER_TYPE_DICT_PART2[column] = "agNumberColumnFilter"
    FILTER_TYPE_DICT_PART2[f"{column}_weighted"] = "agNumberColumnFilter"
    

VISIBLE_COLUMNS = [
    "pmid",
    "targeted_genes",
    "differentially_expressed_genes",
    "species",
    "genome_editing_tools",
    "genome_editing_event",
    "phenotypes"
]


VISIBLE_COLUMNS_PART2 = [
    "gene",
    "count_targeted",
    "count_deg",
    "count_targeted_weighted",
    "count_deg_weighted",
    "total_score"
]

for column in new_columns:
    VISIBLE_COLUMNS_PART2.append(column)
    VISIBLE_COLUMNS_PART2.append(f"{column}_weighted")