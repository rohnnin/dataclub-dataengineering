import duckdb

con = duckdb.connect("taxi.duckdb")

con.execute("""
DROP TABLE IF EXISTS yellow_raw
""")

con.execute("""
CREATE TABLE yellow_raw AS
SELECT *
FROM read_parquet('yellow_tripdata_2023-01.parquet')
""")

print(
    con.execute("SELECT COUNT(*) FROM yellow_raw").fetchall()
)