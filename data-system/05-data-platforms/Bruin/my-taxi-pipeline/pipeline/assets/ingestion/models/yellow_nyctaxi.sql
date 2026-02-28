/* @bruin
name: yellow_nyctaxi
type: duckdb.sql
materialization:
  type: table
depends:
  - yellow_raw
@bruin */

SELECT
    VendorID,
    tpep_pickup_datetime,
    tpep_dropoff_datetime,
    passenger_count,
    trip_distance,
    total_amount,
    DATE(tpep_pickup_datetime) AS pickup_date
FROM yellow_raw
WHERE trip_distance > 0
  AND total_amount > 0;