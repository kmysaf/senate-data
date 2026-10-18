"""Daily Senate run: scrape new PTRs, recover tickers, write senate_trades.csv.

Runs on GitHub Actions (US servers) because efdsearch.senate.gov refuses
connections from outside the US. XYZ Terminal downloads the CSV this writes.

scrape_senate.py, schema.py and entities.py are copied unchanged from
Quantgress (MIT, see LICENSE). Only the Senate half of entities.py is used:
the other sources need tables this repo never builds.

Usage:
    python daily_senate.py            # scrape, resolve, export
    python daily_senate.py --export   # export only, from the DB already here
"""

import sys

import duckdb

import entities
import scrape_senate
from schema import DB_PATH, ensure_schema

CSV_PATH = "senate_trades.csv"
SENATE = entities.SOURCES[0]
assert SENATE["table"] == "senate_trades"


def resolve_tickers():
    con = duckdb.connect(DB_PATH)
    try:
        ensure_schema(con)
        for col in (SENATE["guess_col"], SENATE["how_col"]):
            con.execute(f"ALTER TABLE senate_trades ADD COLUMN IF NOT EXISTS {col} VARCHAR")
        entities.resolve(con, SENATE, entities.extract_congress, dry=False)
    finally:
        con.close()


def export():
    con = duckdb.connect(DB_PATH)
    try:
        ensure_schema(con)
        con.execute(
            "COPY (SELECT * FROM trades WHERE chamber = 'S' ORDER BY filed_date, link,"
            " txn_date, asset_name, tx_type, owner, amount_low)"
            f" TO '{CSV_PATH}' (HEADER)")
        n = con.execute("SELECT count(*) FROM senate_trades").fetchone()[0]
    finally:
        con.close()
    print(f"{n} Senate trades written to {CSV_PATH}")


if __name__ == "__main__":
    if "--export" not in sys.argv:
        scrape_senate.main()
        resolve_tickers()
    export()
