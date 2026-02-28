import duckdb

conn = duckdb.connect("rides_pipeline.duckdb")
conn.sql("SET search_path = 'rides_dataset'")

print("="*60)
print("TRIP COUNT BY VENDOR")
print("="*60)

result = conn.sql("""
    SELECT vendor_id, COUNT(*) as trips, AVG(fare_amount) as avg_fare
    FROM rides
    GROUP BY vendor_id
    ORDER BY vendor_id
""").df()
print(result)

print("\n" + "="*60)
print("TRIPS BY DAY OF WEEK")
print("="*60)

result = conn.sql("""
    SELECT 
        DAYOFWEEK(tpep_pickup_datetime) as day,
        COUNT(*) as trips
    FROM rides
    GROUP BY DAYOFWEEK(tpep_pickup_datetime)
    ORDER BY day
""").df()
print(result)

print("\n" + "="*60)
print("ALL AVAILABLE COLUMNS")
print("="*60)

# Show all columns
cols = conn.sql("SELECT * FROM rides LIMIT 1").df()
print("Columns:")
for col in cols.columns:
    print(f"  - {col}")