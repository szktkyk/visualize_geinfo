import subprocess
import json
import re
import ast
import csv


def make_synonyms(genes:list, taxid, outputfilepath):
    # 遺伝子txtファイルの読み込み
    # aliasをリスト化しておく
    synonyms_data = []
    # geneidの場合
    if re.match(r"^\d+$", genes[0]):
        geneids = genes
        for geneid in geneids:
            geneid = int(geneid)
            synonyms, genename = get_genesynonyms_from_geneid(geneid)
            if type(synonyms) != list:
                synonyms = ast.literal_eval(synonyms)
            else:
                synonyms = synonyms
            synonyms.append(genename)
            synonyms_data.append({"gene": genename,"synonyms": synonyms})
            print({"gene": genename,"synonyms": synonyms})
    
    # gene symbolの場合    
    else:
        for gene in genes:
            synonyms = get_genesynonyms_from_genesymbol(gene, taxid)
            gene = gene.lower()
            if type(synonyms) != list:
                synonyms = ast.literal_eval(synonyms)
            else:
                synonyms = synonyms
            synonyms.append(gene)
            synonyms_data.append({"gene": gene,"synonyms": synonyms})
            print({"gene": gene,"synonyms": synonyms})
    
    field_name_gene = ["gene","synonyms",]
    with open(outputfilepath,"w",) as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_name_gene)
        writer.writeheader()
        writer.writerows(synonyms_data) 

def get_genesynonyms_from_genesymbol(gene_name, taxid):
    req2 = subprocess.run(
        ["datasets", "summary", "gene", "symbol", "{}".format(gene_name), "--taxon", "{}".format(taxid)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    try:
        req_gene = json.loads(req2.stdout.decode())
        if req_gene["total_count"] == 0:
            print("no gene from genesymbol..")
            synonyms = []
        else:
            synonyms = req_gene["reports"][0]["gene"]["synonyms"]
            synonyms = [synonym.lower() for synonym in synonyms]
    except:
        print(f"error at synonyms from genesymbol {gene_name}...")
        synonyms = []

    return synonyms


def get_genesynonyms_from_geneid(geneid):
    req2 = subprocess.run(
        ["datasets", "summary", "gene", "gene-id", "{}".format(geneid)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    req_gene = json.loads(req2.stdout.decode())
    if req_gene["total_count"] == 0:
        print(f"no gene from genesymbol {geneid}..")
        synonyms = []
        gene_name = ""
    else:
        gene_name = req_gene["reports"][0]["gene"]["symbol"]
        gene_name = gene_name.lower()
        try:
            synonyms = req_gene["reports"][0]["gene"]["synonyms"]
            synonyms = [synonym.lower() for synonym in synonyms]
        except:
            synonyms = []

    return synonyms, gene_name