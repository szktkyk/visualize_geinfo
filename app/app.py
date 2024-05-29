import polars as pl
from dash import Dash, html, dcc, Input, Output, State, ALL, ctx, no_update
from dash.exceptions import PreventUpdate
import dash_mantine_components as dmc

from utils.data_utils import *
from utils.schema_utils import VISIBLE_COLUMNS, FILTER_TYPE_DICT
from utils import layout_utils
from utils.chart_utils import fig1
import dash_ag_grid as dag



app = Dash(
    __name__,
    external_stylesheets=[
        "assets/style.css"
    ])
app.title = "gem_llm"

# 見た目の整理
app.layout = dmc.MantineProvider(
    theme={"colorScheme": "light"},
    children=html.Div(
        children=[          
            # ヘッダー周辺のレイアウト
            dmc.Group(
                # 画面の左と右で要素を分ける（flexbox)
                style={
                    "display": "flex",
                    "justify-content": "space-between",
                    "align-items": "center",
                    "border-bottom": "solid",
                    "bottom-border-color": "#FFFFFF",
                    "padding-bottom": "1em",
                    "margin-left": "0.5em",
                    "margin-right": "1em",
                },
                children=[
                    # 左側の要素。タイトルの表示。
                    dmc.Group(
                        position="left",
                        children=[
                    dmc.Title("Genome Editing Metadata by LLM"),
                        ]
                    ),
                    # 右側の要素。諸々のリンクを表示。
                    dmc.Group(
                        position="right",
                        children=[
                            dmc.Anchor("Contact", href="https://bonohu.hiroshima-u.ac.jp/index_en.html",target="_blank", id="contact-link", size="xl"),
                        ]
                    )
                ],
            ),

            # Browse Data周辺のレイアウト
            dmc.Center(
                style={"margin-top": "0.5em"},
                children=dmc.Title(
                    "Browse LLM results"
                )
            ),

            # Select Columnsボタン
            dmc.Group(
                children=[
                    dmc.Menu(
                        id="columns-selection-menu",
                        clickOutsideEvents=False,
                        closeDelay=False,
                        closeOnClickOutside=False,
                        closeOnEscape=False,
                        closeOnItemClick=False,
                        styles={"dropdown": {"background-color": "#2d3038"}},
                        children=[
                            dmc.MenuTarget(
                                html.Button(
                                    "Select Columns",
                                    id="open-modal-bttn",
                                    # variant="light",
                                    style={
                                        "border-color": "#000000",
                                        "color": "#000000",
                                        "margin-bottom": "0.5em",
                                    },
                                ),
                            ),
                            dmc.MenuDropdown(
                                children=[
                                    dmc.MenuItem(
                                        style={
                                            "padding": "0",
                                        },
                                        children=layout_utils.render_columns_modal(),
                                    ),
                                ],
                            ),
                        ],
                    ),
                    html.A(
                        html.Button(
                            "Refresh Table", 
                            id="viz-bttn2", 
                            style={"border-color": "#000000", "color": "#000000", "margin-bottom": "0.5em"}), 
                            href="/"),
                    dcc.Location(id='url', refresh=True),
                ],
                position="left",
            ),

            # テーブルのレイアウト
            # TODO: 検索で大文字小文字区別つかないようにする
            # TODO: リンクをつける（遺伝子とかBioProIDとか）> むずすぎるので諦め。もし時間があればいつかまた試す。
            dmc.LoadingOverlay(
                overlayColor="black",
                loaderProps={"variant": "dots"},
                zIndex=299,
                children=[
                    dag.AgGrid(
                        # TODO: それぞれのカラムの検索方法の見直し
                        id="infinite-grid",
                        rowModelType="infinite",
                        columnDefs=layout_utils.generate_column_defintions(),
                        pagination=True,
                        paginationPageSize=100,
                        className="ag-theme-balham",
                        defaultColDef={"filter": True},
                    ),
                    dcc.Store(id="filter-model"),
                ],
            ),
            # Browse Data周辺のレイアウト
            dmc.Center(
                style={"margin-top": "1.5em"},
                children=dmc.Title(
                    "Score Table"
                )
            ),
            # 2個目のテーブルを表示
            dmc.LoadingOverlay(
                overlayColor="black",
                loaderProps={"variant": "dots"},
                zIndex=299,
                children=[
                    dag.AgGrid(
                        # TODO: それぞれのカラムの検索方法の見直し
                        id="infinite-grid_part2",
                        rowModelType="infinite",
                        enableEnterpriseModules=True,
                        columnDefs=layout_utils.generate_column_defintions_part2(),
                        # columnDefs=layout_utils.generate_column_defs(),
                        pagination=True,
                        paginationPageSize=100,
                        className="ag-theme-balham",
                        defaultColDef={"filter": True},
                    ),
                ],
            ),
            # 下記以下は色々と考える（まだ例をそのままコピペした状態）
             # Browse Data周辺のレイアウト
            dmc.Center(
                style={"margin-top": "1.5em"},
                children=dmc.Title(
                    "Visualize Data"
                )
            ),
            dmc.Group(
                [
                    html.Button(
                        "Refresh Plots",
                        id="viz-bttn",
                        # variant="light",
                        style={
                            "border-color": "#000000",
                            "color": "#000000",
                        },
                    ),
                ],
                position="left",
                style={
                    "margin-bottom": "1em",
                    "margin-top": "0.5em",
                },
            ),
            dmc.LoadingOverlay(
                overlayColor="black",
                loaderProps={"variant": "dots"},
                zIndex=299,
                children=[
                    dmc.Group(
                        [
                            html.Div(
                                dcc.Graph(
                                    id="allscore-plot",
                                ),
                                style={"width": "95%"},
                            ),
                        ]
                    )
                ],
            ),

            html.P(
                    children=[
                        "This work is licensed under ",
                        html.A(
                            children=[
                                "CC BY 4.0",
                                html.Img(
                                    src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1",
                                    style={"height": "22px", "margin-left": "3px", "vertical-align": "text-bottom"},
                                    alt=""
                                ),
                                html.Img(
                                    src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1",
                                    style={"height": "22px", "margin-left": "3px", "vertical-align": "text-bottom"},
                                    alt=""
                                )
                            ],
                            href="https://creativecommons.org/licenses/by/4.0/?ref=chooser-v1",
                            target="_blank",
                            rel="license noopener noreferrer",
                            style={"display": "inline-block"}
                        )
                    ],
                    style={"padding-top": "2em", "padding-left":"0.5em"}  # 適宜スタイルを調整
                )
            ]
    )
)

# Select Columnsボタンを使った時の処理
# TODO: utilsのdataとlayoutの処理を理解する
@app.callback(
    Output("infinite-grid", "columnDefs"),
    Output("columns-selection-menu", "opened"),
    Input("open-modal-bttn", "n_clicks"),
    Input("apply-bttn", "n_clicks"),
    State("columns-selection-menu", "opened"),
    State({"type": "checkbox", "field": ALL}, "checked"),
    State({"type": "checkbox", "field": ALL}, "label"),
    prevent_initial_call=True,
)
def update_columns(
    click1,
    click2,
    opened,
    columns_checked,
    columns_label,
):
    if ctx.triggered_id == "open-modal-bttn":
        return no_update, not opened
    column_list = []
    for i, col in enumerate(columns_label):
        if columns_checked[i]:
            column_list.append(col)
    columnDefs = layout_utils.generate_column_defintions(column_list)
    return columnDefs, False

# テーブルの動作に関する処理?
# TODO: 今度内容をさらに理解する
@app.callback(
    Output("infinite-grid", "getRowsResponse"),
    Output("filter-model", "data"),
    Input("infinite-grid", "getRowsRequest"),
    Input("infinite-grid", "columnDefs"),
)
def infinite_scroll(request, columnDefs):
    if request is None:
        raise PreventUpdate
    columns = [col["field"] for col in columnDefs]
    ldf = scan_ldf(filter_model=request["filterModel"], columns=columns)
    df = ldf.collect()
    partial = df.slice(request["startRow"], request["endRow"]).to_pandas()
    
    return {
        "rowData": partial.to_dict("records"),
        "rowCount": len(df),
    }, request["filterModel"]


@app.callback(
    Output("infinite-grid_part2", "getRowsResponse"),
    Input("infinite-grid_part2", "getRowsRequest"),
    Input("infinite-grid_part2", "columnDefs"),
)
def infinite_scroll_part2(request, columnDefs):
    if request is None:
        raise PreventUpdate
    columns = [col["field"] for col in columnDefs]
    ldf = None
    if request["filterModel"]:
        ldf = scan_ldf_part2(filter_model=request["filterModel"], columns=columns)
    elif request["sortModel"]:
        ldf = scan_ldf_sort(sortModel = request["sortModel"], columns=columns)
    else:
        ldf = scan_ldf_part2(columns=columns)
    if ldf is None:
        raise ValueError("ldf is None, unable to process request")
    df = ldf.collect()
    partial = df.slice(request["startRow"], request["endRow"]).to_pandas()
    return {
        "rowData": partial.to_dict("records"),
        "rowCount": len(df),
    }


@app.callback(
    Output("allscore-plot", "figure"),
    # Output("genes-getool-plot", "figure"),
    # Output("year-getool-plot", "figure"),
    # Output("year-taxonomy-plot", "figure"),
    Input("filter-model", "data"),
    Input("viz-bttn", "n_clicks"),
)
def visualize(filter_model,n_clicks):
    # columns = ["getool", "taxonomy_category", "pmid", "genesymbol","pubdate"]
    # if filter_model:
    #     columns_to_filter = [col for col in filter_model]
    #     columns = list(set([*columns_to_filter, *columns]))
    # ldf = scan_ldf(filter_model=filter_model, columns=columns)
    # df = ldf.collect()
    figure1 = fig1()
    # figure1, figure2 = fig1_and_fig2(df)
    # figure3, figure4 = fig3_and_fig4(df)
    return figure1


if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0')
