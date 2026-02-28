/* @bruin
name: trips_report
type: duckdb.sql
materialization:
  type: table
depends:
  - staging_trips
  - payment_lookup
@bruin */

SELECT s.pickup_datetime,
       s.passenger_count,
       s.total_amount,
       p.payment_type
FROM staging_trips s
LEFT JOIN payment_lookup p
  ON s.payment_type_id = p.payment_type_id;