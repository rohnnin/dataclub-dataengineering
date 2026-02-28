/* @bruin
name: staging_trips
type: duckdb.sql
materialization:
  type: table
depends:
  - trips
@bruin */

SELECT *
FROM trips;