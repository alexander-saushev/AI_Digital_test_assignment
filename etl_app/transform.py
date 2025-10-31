import logging
import pandas as pd

logger = logging.getLogger(__name__)

def transform_countries(raw_data):
    """
    Transform raw JSON data about countries into a pandas DataFrame
    with the required fields and formatting.

    Returns:
        pandas.DataFrame: A cleaned and structured DataFrame containing country information.
    """
    logger.info(f"Parsing JSON to Pandas Dataframe...")

    rows = []
    for item in raw_data:
        # Parse basic scalar and list-based columns
        name_common = item.get("name", {}).get("common")
        population = item.get("population")
        area = item.get("area")
        capital = ", ".join(item.get("capital", []) or [])
        flag_svg_url = item.get("flags", {}).get("svg")
        tld = ", ".join(item.get("tld", []) or [])
        borders = ", ".join(item.get("borders", []) or [])
        timezones = ", ".join(item.get("timezones", []) or [])

        # Parse languages: extract dictionary values
        langs = item.get("languages") or {}
        languages = ", ".join(list(langs.values()))

        # Parse currencies: format as "Full Name (Symbol)"
        currs = item.get("currencies") or {}
        cur_list = []
        for c in currs.values():
            cname = c.get("name")
            sym = c.get("symbol")
            if cname and sym:
                cur_list.append(f"{cname} ({sym})")
            elif cname:
                cur_list.append(cname)
        currencies = ", ".join(cur_list)

        rows.append({
            "name": name_common,
            "population": population,
            "area": area,
            "capital": capital,
            "flag_svg_url": flag_svg_url,
            "tld": tld,
            "borders": borders,
            "timezones": timezones,
            "languages": languages,
            "currencies": currencies,
        })

    df = pd.DataFrame(rows).dropna(subset=["name"])

    logger.info(f"Parsed {len(df)} rows.")
    return df