import re
import datetime
import xml.etree.ElementTree as ET

selected_columns = ["gene","count_targeted","count_deg","ON_score","PD_score"]

WEIGHTS = {
    "count_targeted":0.35,
    "count_deg":0.15,
    "ON_score":0.45,
    "PD_score":0.05,
}


API_GENEID_BASE = "http://127.0.0.1:8000/search_geneid/?id=" 
API_GENE_BASE = "http://127.0.0.1:8000/search_gene/?name=" 


t_delta = datetime.timedelta(hours=9)
JST = datetime.timezone(t_delta, "JST")
now = datetime.datetime.now(JST)
date = now.strftime("%Y%m%d")

taxonomy_id = "9606"



