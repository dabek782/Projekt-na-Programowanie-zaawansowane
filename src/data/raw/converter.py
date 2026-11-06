import pandas as pd
import os

# dir_path = os.path.dirname(os.path.realpath(__file__))
# print(dir_path)
# pd.read_csv(dir_path + "/Data_telemetry_1793987272.csv").to_parquet(dir_path+"/Data_telemetry_1793987272.parquet")

csv_file = pd.read_csv(dir_path + "/Data_telemetry_1793987272.csv")
parquet_file = pd.read_parquet(dir_path + "/Data_telemetry_1793987272.parquet")
print(csv_file.equals(parquet_file))