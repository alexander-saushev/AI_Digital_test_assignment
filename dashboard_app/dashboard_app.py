import os
import logging
import pandas as pd
from dash import Dash, html, dash_table, Input, Output
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

logger = logging.getLogger(__name__)
engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")


def load_data(engine):
    """
    Load country data from the PostgreSQL database.

    Checks if the 'countries' table exists and is not empty.
    Returns a pandas DataFrame with the table content, or an empty DataFrame if unavailable.
    """
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' AND table_name = 'countries'
                );
            """))
            if not result.scalar():
                return pd.DataFrame()

            count_result = conn.execute(text("SELECT COUNT(*) FROM public.countries;"))
            if count_result.scalar() == 0:
                return pd.DataFrame()

            return pd.read_sql("SELECT * FROM public.countries", engine)

    except (OperationalError, Exception) as e:
        logger.warning(f"Error loading data: {e}")
        return pd.DataFrame()


def serve_layout():
    """
    Build and return the Dash app layout.

    Displays a table of countries and a flag section.
    If no data is available, shows a warning message.
    """
    dash_df = load_data(engine)

    if dash_df.empty:
        return html.Div([
            html.H3("No data available. Please restart ETL and/or refresh page.")
        ])

    return html.Div([
        html.H2("Countries Dashboard"),
        html.Div([
            html.Div([
                dash_table.DataTable(
                    id="table",
                    data=dash_df.to_dict("records"),
                    columns=[{"name": i, "id": i} for i in dash_df.columns],
                    page_size=20,
                    sort_action="native",
                    sort_by=[{"column_id": "name", "direction": "asc"}],
                    row_selectable="single",
                    fixed_rows={"headers": True},
                    style_table={
                        "width": "100%",
                        "overflowX": "auto",
                        "overflowY": "scroll",
                        "height": "80vh",
                        "maxHeight": "80vh",
                    },
                    style_cell={
                        "textAlign": "left",
                        "padding": "5px",
                        "minWidth": "100px",
                        "width": "150px",
                        "maxWidth": "300px",
                        "whiteSpace": "normal",
                        "overflow": "hidden",
                    },
                    style_header={"backgroundColor": "#f8f8f8", "fontWeight": "bold"},
                )
            ], style={"width": "70%"}),

            html.Div([
                html.H3("Flag of selected country:"),
                html.Img(id="flag", src="", style={
                    "height": "200px",
                    "border": "1px solid #ccc",
                    "maxWidth": "100%",
                    "objectFit": "contain",
                })
            ], style={
                "width": "30%",
                "paddingLeft": "20px",
                "display": "flex",
                "flexDirection": "column",
                "alignItems": "center",
            })
        ], style={
            "display": "flex",
            "width": "100%",
            "alignItems": "flex-start",
            "gap": "10px",
        })
    ])


app = Dash(__name__, title="Countries Dashboard")
app.layout = serve_layout

@app.callback(
    Output("flag", "src"),
    Output("flag", "style"),
    Input("table", "derived_virtual_data"),
    Input("table", "derived_virtual_selected_rows"),  
)
def update_flag(rows, dv_selected_rows):
    """
    Update the displayed flag based on the selected country in the table.

    Args:
        rows (list[dict]): Current data displayed in the table.
        dv_selected_rows (list[int]): Indices of selected rows.

    Returns:
        tuple: (flag image URL, style dict for the image)
    """
    base_style = {"height": "200px", "maxWidth": "100%", "objectFit": "contain"}

    if not rows or not dv_selected_rows:
        return "", {**base_style, "border": "none"}

    idx = dv_selected_rows[0]
    flag_url = rows[idx].get("flag_svg_url", "")
    return flag_url, {**base_style, "border": "1px solid #ccc"}



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050)