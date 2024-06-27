import ast

def search_gem_llm(gene_list, llm_data, synonyms_data):
    """
    Parameters
    
    gene_list : list
        List of gene symbols
        
    llm_data : list
        List of dictionaries containing LLM data (jsonl)
    
    synonyms_data : list
        List of dictionaries containing gene synonyms
    
    This function will search for the gene symbols in the LLM data and count the number of targeted genes and DEGs.
    """
    results = []
    for gene in gene_list:
        print(gene)
        getools = []
        geevents = []
        count_targeted = 0
        count_deg = 0
        target_dict = next((item for item in synonyms_data if item.get("gene") == gene), None)
        try:
            synonyms = target_dict["synonyms"]
            if type(synonyms) != list:
                synonyms = ast.literal_eval(synonyms)
            else:
                synonyms = synonyms
            synonyms = [s.lower() for s in synonyms]
        except:
            print(f"no synonyms for gene: {gene}")
            synonyms = []
        # print(f"synonyms: {synonyms}")
        
        for llm in llm_data:
            # targeted_genesについて処理
            llm_genes = llm["targeted_genes"]
            if type(llm_genes) != list:
                llm_genes = ast.literal_eval(llm_genes)
            else:
                llm_genes = llm_genes
            llm_genes = [g.lower() for g in llm_genes]
            if any(alias in synonyms for alias in llm_genes):
                count_targeted += 1
                getool = llm["genome_editing_tools"]
                if type(getool) != list:
                    getool = ast.literal_eval(getool)
                else:
                    getool = getool
                for t in getool:
                    getools.append(t)
                geevent = llm["genome_editing_event"]
                if type(geevent) != list:
                    geevent = ast.literal_eval(geevent)
                else:
                    geevent = geevent
                for e in geevent:
                    geevents.append(e)
                continue
            else:
                pass
            
            # degについても同様に処理
            llm_deg = llm["differentially_expressed_genes"]
            if type(llm_deg) != list:
                llm_deg = ast.literal_eval(llm_deg)
            else:
                llm_deg = llm_deg
            llm_deg = [g.lower() for g in llm_deg]
            if any(alias in synonyms for alias in llm_deg):
                count_deg += 1
                getool = llm["genome_editing_tools"]
                if type(getool) != list:
                    getool = ast.literal_eval(getool)
                else:
                    getool = getool
                for t in getool:
                    getools.append(t)
                geevent = llm["genome_editing_event"]
                if type(geevent) != list:
                    geevent = ast.literal_eval(geevent)
                else:
                    geevent = geevent
                for e in geevent:
                    geevents.append(e)
                continue
            else:
                continue
        
        getools = list(set(getools))
        geevents = list(set(geevents))
            
        results.append({"gene": gene, "count_targeted": count_targeted, "count_deg": count_deg, "genome_editing_tools": getools, "genome_editing_events": geevents})
        print({"gene": gene, "count_targeted": count_targeted, "count_deg": count_deg, "genome_editing_tools": getools, "genome_editing_events": geevents})
    return results