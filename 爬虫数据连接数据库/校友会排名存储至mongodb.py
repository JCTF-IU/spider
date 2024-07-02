import csv
import os
from pymongo import MongoClient

# MongoDB连接配置
mongo_config = {
    'host': 'localhost',
    'port': 27017,
}

# 连接到MongoDB
client = MongoClient(mongo_config['host'], mongo_config['port'])
db = client['AlumniAssociation']  # 使用或创建一个名为'AlumniAssociation'的数据库


def import_csv_to_mongodb(year, csv_file):
    collection_name = f'AlumniData_{year}'
    collection = db[collection_name]  # 使用或创建一个集合

    # 导入CSV数据到MongoDB集合
    with open(csv_file, 'r', encoding='utf-8-sig') as f:  # 使用utf-8-sig处理BOM
        csv_reader = csv.DictReader(f)  # 使用DictReader以便直接插入字典到MongoDB
        for row in csv_reader:

            # 插入数据到MongoDB集合
            collection.insert_one(row)


for year in range(2015, 2025):
    csv_file = f"{year}校友会中国大学排名.csv"
    if os.path.exists(csv_file):
        import_csv_to_mongodb(year, csv_file)
        print(f"Data from {csv_file} has been imported successfully.")
    else:
        print(f"File {csv_file} does not exist.")
