import pandas as pd

csv_file = r'your csv from Oracle'
parquet_file = r'output parquet file'

df = pd.read_csv(csv_file)
df.to_parquet(parquet_file)