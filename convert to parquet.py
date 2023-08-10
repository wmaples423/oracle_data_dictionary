import pandas as pd

csv_file = r'C:\Users\MaplesWi\OneDrive - Clayton Homes\Desktop\oracle_data_dictionary.csv'
parquet_file = r'C:\Users\MaplesWi\OneDrive - Clayton Homes\Desktop\oracle_data_dictionary.parquet'

df = pd.read_csv(csv_file)
df.to_parquet(parquet_file)