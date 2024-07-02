import csv
from pymongo import MongoClient
import os

# MongoDB配置
mongo_uri = "mongodb://localhost:27017/"  # MongoDB连接URI，默认为localhost和默认端口
mongo_db_name = "wushulian"  # MongoDB数据库名称

# 连接到MongoDB
client = MongoClient(mongo_uri)
db = client[mongo_db_name]


def import_csv_to_mongodb(year, csv_file, collection):
    # 读取CSV文件并插入数据到MongoDB集合中
    with open(csv_file, 'r', encoding='utf-8-sig') as f:
        csv_reader = csv.DictReader(f)  # 使用DictReader可以直接将每行转换为字典
        for row in csv_reader:
            rank = int(row['排名'])  # 转换排名为整数
            school = row['学校']

            # 构造要插入的文档
            document = {
                '年份': year,
                '排名': rank,
                '学校': school
            }

            # 插入文档到集合中
            collection.insert_one(document)

        # 循环处理2015到2023年的数据


for year in range(2015, 2024):
    csv_file = f"{year}武书连中国大学排名.csv"
    collection_name = f"wushulian_{year}"
    collection = db[collection_name]

    if os.path.exists(csv_file):
        import_csv_to_mongodb(year, csv_file, collection)
        print(f"Data from {csv_file} has been imported successfully to {collection_name}.")
    else:
        print(f"File {csv_file} does not exist.")

