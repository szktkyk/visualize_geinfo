# visualize_geinfo
Visualize genome editing related information [extracted using LLM](https://github.com/szktkyk/extract_geinfo)

## Visualization Preview
<img width="996" alt="visualize_geinfo_fig" src="https://github.com/user-attachments/assets/aba9ca59-acb6-456a-b0f0-9fabfa0ac879">


## How to use
1. Place necessary files to the `app_data` directory
    - `llm.jsonl`: jsonl file that was created by [extract_geinfo](https://github.com/szktkyk/extract_geinfo)
    - `gene.txt`: text file including a list of genes separated by line
    - `score.tsv`: tsv file including other score data to visualize with this application
        - Genes must be the same as genes in `gene.txt`. The column name for genes must be `gene`.
        <!-- - Only columns with names ending in `_score` will be loaded in this application. Please see the example in this GitHub.repository. -->
    - `synonyms.csv`: csv file that was created when running [extract_geinfo](https://github.com/szktkyk/extract_geinfo)
        - If you do not have this, it will be automatically created in this application.
1. Fill in the `selected_columns`, `WEIGHTS`, `score_invert` in `config/config.py`
    - For `selected_columns`, include `gene`, `count_targeted`, and `count_deg` as fixed entries, and add any additional column names from score.tsv that you wish to include.
    - For `WEIGHTS`, assign weights to each score, including the additional scores, so that their total equals 1.
    - For `score_invert`, select and add a column_name that should be normalized and weighted with inverse (smaller number with more weight).
    - Please see the [example](https://github.com/szktkyk/visualize_geinfo/blob/main/config.py) in this GitHub repository.
1. Build Docker image
    - `docker build -t visualize_geinfo .`
1. Create other necessary files
    - `docker run --rm -it -v $(pwd):/app -p 8050:8050 visualize_geinfo python ./app/prepare_files.py`
1. Visualize data
    - `docker run --rm -it -v $(pwd):/app -p 8050:8050 visualize_geinfo python ./app/app.py`
    - Access `http://0.0.0.0:8050/`

