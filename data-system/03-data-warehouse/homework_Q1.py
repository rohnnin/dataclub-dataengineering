
import duckdb

# Connect to DuckDB
conn = duckdb.connect("rides_pipeline.duckdb")
conn.sql("SET search_path = 'rides_dataset'")

print("="*70)
print("TOTAL RECORD COUNT")
print("="*70 + "\n")

# Count all records
result = conn.sql("SELECT COUNT(*) as total_records FROM rides").df()
total = result['total_records'].values[0]

print(f"Total records in 'rides' table: {total:,}\n")

# Additional breakdown
print("="*70)
print("BREAKDOWN BY MONTH (Estimated)")
print("="*70 + "\n")

breakdown = conn.sql("""
    SELECT 
        EXTRACT(MONTH FROM tpep_pickup_datetime) as month,
        COUNT(*) as record_count,
        ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM rides), 2) as percentage
    FROM rides
    GROUP BY EXTRACT(MONTH FROM tpep_pickup_datetime)
    ORDER BY month
""").df()

print(breakdown)

print("\n" + "="*70)
print("QUICK STATS")
print("="*70 + "\n")

stats = conn.sql("""
    SELECT 
        COUNT(*) as total_rides,
        COUNT(DISTINCT DATE(tpep_pickup_datetime)) as days_covered,
        COUNT(DISTINCT vendor_id) as vendors,
        MIN(tpep_pickup_datetime) as earliest_trip,
        MAX(tpep_pickup_datetime) as latest_trip
    FROM rides
""").df()

print(stats)

print("\n✅ Count complete!")

conn.close()