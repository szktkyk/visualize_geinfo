# PMIDのフィルターをどうするか
# genesymbolとかPMIDとかはリンクをつけたい
# pubdateもフィルタリングできると嬉しい
FILTER_TYPE_DICT = {
    "pmid": "agTextColumnFilter",
    "targeted_genes": "agTextColumnFilter",
    "differentially_expressed_genes": "agTextColumnFilter",
    "species": "agSetColumnFilter",
    "genome_editing_tools": "agSetColumnFilter",
    "genome_editing_event": "agSetColumnFilter",
    "study_context": "agTextColumnFilter",
    "key_findings": "agTextColumnFilter",
    "implications": "agTextColumnFilter",
}

FILTER_TYPE_DICT_PART2 = {
    "gene":"agTextColumnFilter",
    "count_targeted":"agNumberColumnFilter",
    "count_deg":"agNumberColumnFilter",
    "ON_score":"agNumberColumnFilter",
    "PD_score":"agNumberColumnFilter",
    "count_targeted_right":"agNumberColumnFilter",
    "count_deg_right":"agNumberColumnFilter",
    "ON_score_right":"agNumberColumnFilter",
    "PD_score_right":"agNumberColumnFilter",
    "total_score":"agNumberColumnFilter"
}


VISIBLE_COLUMNS = [
    "pmid",
    "targeted_genes",
    "differentially_expressed_genes",
    "species",
    "genome_editing_tools",
    "genome_editing_event",
    "study_context",
    "key_findings",
    "implications",
]


VISIBLE_COLUMNS_PART2 = [
    "gene",
    "count_targeted",
    "count_deg",
    "ON_score",
    "PD_score",
    "count_targeted_right",
    "count_deg_right",
    "ON_score_right",
    "PD_score_right",
    "total_score"
]
