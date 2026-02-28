import dlt

# Recreate pipeline object (needed for sql_client)
pipeline = dlt.pipeline(
    pipeline_name="rides_pipeline",
    destination="duckdb",
    dataset_name="rides_dataset",
)

print("🔗 Using pipeline.sql_client() to query:\n")

# Provide a resource name to query a table of that name
with pipeline.sql_client() as client:
    with client.execute_query("SELECT count(1) as total_rides FROM rides") as cursor:
        data = cursor.df()

print("Total Rides:")
print(data)

print("\n" + "="*70)
print("\n✅ Query complete!")