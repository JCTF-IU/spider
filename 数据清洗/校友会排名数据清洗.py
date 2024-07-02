import pandas as pd
import os


# 遍历当前目录下的所有文件
for filename in os.listdir('.'):
    if filename.endswith('.csv') and '校友会中国大学排名' in filename:
        # 读取CSV文件
        df = pd.read_csv(filename)

        # 只保留前三列
        df_trimmed = df.iloc[:, :3]

        # 覆盖原始文件
        df_trimmed.to_csv(filename, index=False)

        print(f"Processed and overwritten {filename}")