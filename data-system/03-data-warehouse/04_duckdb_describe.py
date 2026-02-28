
import duckdb

# Connect to the DuckDB database
conn = duckdb.connect("rides_pipeline.duckdb")
print("✓ Connected to: rides_pipeline.duckdb\n")

# Set search path to the dataset
conn.sql("SET search_path = 'rides_dataset'")
print("✓ Set search path to: rides_dataset\n")

# Describe the dataset to see loaded tables
print("📊 DESCRIBING TABLES:\n")
res = conn.sql("DESCRIBE").df()
print(res)

print("\n" + "="*70)
print("📋 DETAILED COLUMN INFORMATION:\n")
column_info = conn.sql("DESCRIBE rides").df()
print(column_info)

