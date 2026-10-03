from pathlib import Path
import sqlite3

import pandas as pd


ACTIVITY_DIR = Path(__file__).resolve().parents[1]
INPUT_FILE = ACTIVITY_DIR / "data" / "ventas.csv"
OUTPUT_FILE = ACTIVITY_DIR / "submission" / "ventas.csv"
DATABASE_FILE = ACTIVITY_DIR / "temp" / "ventas.db"


SUPPLIER_NAMES = {
    "amazon web services colombia": "Amazon Web Services Colombia",
    "bancolombia s.a.": "Bancolombia S.A.",
    "cementos argos sa": "Cementos Argos S.A.",
    "cementos argos s.a.": "Cementos Argos S.A.",
    "corona sas": "Corona S.A.S.",
    "google colombia ltda.": "Google Colombia Ltda.",
    "ibm colombia sas.": "IBM Colombia S.A.S.",
    "ibm colombia s.a.s.": "IBM Colombia S.A.S.",
    "microsoft colombia inc.": "Microsoft Colombia Inc.",
    "nutresa sa": "Nutresa S.A.",
    "nutresa s.a.": "Nutresa S.A.",
    "oracle colombia ltda.": "Oracle Colombia Ltda.",
    "postobon s.a.": "Postobón S.A.",
    "postobón s.a.": "Postobón S.A.",
    "sap colombia sas": "SAP Colombia S.A.S.",
    "siemens s.a.s.": "Siemens S.A.S.",
}


def normalize_text(value):
    if value is None:
        return None
    return " ".join(str(value).strip().split())


def normalize_supplier(value):
    text = normalize_text(value)
    return SUPPLIER_NAMES.get(text.lower(), text)


def normalize_city(value):
    city = normalize_text(value)
    return {"bogotá": "Bogotá", "bogota": "Bogotá", "medellín": "Medellín", "medellin": "Medellín"}.get(city.lower(), city)


def normalize_date(value):
    text = normalize_text(value).replace("/", "-").replace(".", "-")
    if len(text) == 8 and text[2] == "-":
        text = f"{text[:6]}20{text[6:]}"
    if len(text) == 10 and text[4] != "-":
        first, second, year = text.split("-")
        day, month = (first, second) if int(first) > 12 else (second, first) if int(second) > 12 else (first, second)
        return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
    year, first, second = text.split("-")
    day, month = (first, second) if int(first) > 12 else (second, first)
    return f"{year}-{month.zfill(2)}-{day.zfill(2)}"


def normalize_number(value):
    text = normalize_text(value)
    if not text or text == "N/A":
        return None
    text = text.replace("COP ", "").replace("$", "")
    if text.endswith(".00K"):
        text = f"{text[:-4]}000"
    return float(text.replace(",", "").replace(".", ""))


def normalize_discount(value):
    text = normalize_text(value)
    if not text or text == "N/A":
        return None
    number = float(text.replace("%", ""))
    return number / 100 if number > 1 else number


def normalize_unit_price(value):
    text = normalize_text(value)
    if text is None or not text or text == "N/A":
        return None
    text = text.replace("$", "")
    if text.endswith(".00"):
        text = text[:-3]
    return float(text.replace(",", "").replace(".", ""))


def normalize_weight(value):
    text = normalize_text(value)
    if not text or text == "N/A":
        return None
    text = text.lower().replace(",", ".")
    if text.endswith(" kg"):
        return float(text[:-3])
    if text.endswith(" g"):
        return float(text[:-2]) / 1000
    if text.endswith(" ton"):
        return float(text[:-4]) * 1000
    return float(text)


def normalize_units(value):
    text = normalize_text(value)
    return None if text is None or not text or text.lower() in {"nan", "n/a"} else float(text)


def main():
    raw_sales = pd.read_csv(INPUT_FILE, dtype=str, keep_default_na=False)
    raw_sales.columns = [column.strip().lower().replace(" ", "_") for column in raw_sales.columns]

    DATABASE_FILE.unlink(missing_ok=True)
    with sqlite3.connect(DATABASE_FILE) as database:
        raw_sales.to_sql("raw_sales", database, index=False)
        database.create_function("normalize_supplier", 1, normalize_supplier)
        database.create_function("normalize_city", 1, normalize_city)
        database.create_function("normalize_date", 1, normalize_date)
        database.create_function("normalize_number", 1, normalize_number)
        database.create_function("normalize_discount", 1, normalize_discount)
        database.create_function("normalize_unit_price", 1, normalize_unit_price)
        database.create_function("normalize_weight", 1, normalize_weight)
        database.create_function("normalize_units", 1, normalize_units)

        database.execute(
            """
            CREATE TABLE cleaned_sales AS
            SELECT
                CAST(supplier_id AS INTEGER) AS supplier_id,
                normalize_supplier(supplier) AS supplier,
                'COL' AS country,
                normalize_city(city) AS city,
                normalize_date(purchase_date) AS purchase_date,
                normalize_number(amount) AS amount,
                normalize_discount(discount) AS discount,
                normalize_weight(weight) AS weight,
                normalize_units(units) AS units,
                normalize_unit_price(unit_price) AS unit_price,
                TRIM(contact_email) AS contact_email
            FROM raw_sales
            """
        )
        sales = pd.read_sql_query("SELECT * FROM cleaned_sales", database)

    sales.to_csv(OUTPUT_FILE, index=False)


if __name__ == "__main__":
    main()
