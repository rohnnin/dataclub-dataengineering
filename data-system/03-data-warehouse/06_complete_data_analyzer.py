import duckdb

conn = duckdb.connect("rides_pipeline.duckdb")
conn.sql("SET search_path = 'rides_dataset'")

print("="*70)
print("1️⃣  TOTAL RECORD COUNT")
print("="*70 + "\n")

total = conn.sql("SELECT COUNT(*) as total_records FROM rides").df()
print(total)

print("\n" + "="*70)
print("2️⃣  TRIPS BY VENDOR")
print("="*70 + "\n")

vendor = conn.sql("""
    SELECT 
        vendor_id,
        COUNT(*) as trip_count,
        ROUND(AVG(fare_amount), 2) as avg_fare,
        ROUND(AVG(trip_distance), 2) as avg_distance
    FROM rides
    GROUP BY vendor_id
    ORDER BY vendor_id
""").df()
print(vendor)

print("\n" + "="*70)
print("3️⃣  TRIPS BY PAYMENT TYPE")
print("="*70 + "\n")

payment = conn.sql("""
    SELECT 
        payment_type,
        COUNT(*) as trip_count,
        ROUND(AVG(fare_amount), 2) as avg_fare,
        ROUND(AVG(total_amount), 2) as avg_total
    FROM rides
    GROUP BY payment_type
    ORDER BY payment_type
""").df()
print(payment)

print("\n" + "="*70)
print("4️⃣  TOP 10 PICKUP ZONES")
print("="*70 + "\n")

zones = conn.sql("""
    SELECT 
        pickup_zone,
        COUNT(*) as trip_count,
        ROUND(AVG(trip_distance), 2) as avg_distance,
        ROUND(AVG(fare_amount), 2) as avg_fare
    FROM rides
    WHERE pickup_zone IS NOT NULL
    GROUP BY pickup_zone
    ORDER BY trip_count DESC
    LIMIT 10
""").df()
print(zones)

print("\n" + "="*70)
print("5️⃣  FARE STATISTICS")
print("="*70 + "\n")

fare_stats = conn.sql("""
    SELECT 
        ROUND(MIN(fare_amount), 2) as min_fare,
        ROUND(AVG(fare_amount), 2) as avg_fare,
        ROUND(MAX(fare_amount), 2) as max_fare,
        ROUND(STDDEV(fare_amount), 2) as stddev_fare
    FROM rides
""").df()
print(fare_stats)

print("\n" + "="*70)
print("6️⃣  TRIPS BY DAY OF WEEK")
print("="*70 + "\n")

day_of_week = conn.sql("""
    SELECT 
        CASE 
            WHEN DAYOFWEEK(tpep_pickup_datetime) = 1 THEN 'Sunday'
            WHEN DAYOFWEEK(tpep_pickup_datetime) = 2 THEN 'Monday'
            WHEN DAYOFWEEK(tpep_pickup_datetime) = 3 THEN 'Tuesday'
            WHEN DAYOFWEEK(tpep_pickup_datetime) = 4 THEN 'Wednesday'
            WHEN DAYOFWEEK(tpep_pickup_datetime) = 5 THEN 'Thursday'
            WHEN DAYOFWEEK(tpep_pickup_datetime) = 6 THEN 'Friday'
            WHEN DAYOFWEEK(tpep_pickup_datetime) = 7 THEN 'Saturday'
        END as day_name,
        COUNT(*) as trip_count,
        ROUND(AVG(fare_amount), 2) as avg_fare
    FROM rides
    GROUP BY DAYOFWEEK(tpep_pickup_datetime)
    ORDER BY DAYOFWEEK(tpep_pickup_datetime)
""").df()
print(day_of_week)

print("\n" + "="*70)
print("✅ Analysis complete!")
print("="*70)

conn.close()