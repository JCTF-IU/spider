import csv
from pymongo import MongoClient

# MongoDB配置
mongo_config = {
    'host': 'localhost',
    'port': 27017,
    'db_name': 'ruanke'
}

# 连接MongoDB
client = MongoClient(mongo_config['host'], mongo_config['port'])
db = client[mongo_config['db_name']]

# 为每年的数据创建一个集合，并从对应的CSV文件中导入数据
for year in range(2015, 2025):
    collection_name = f'ruanke_{year}'
    collection = db[collection_name]

    csv_file = f'{year}年软科中国大学排名.csv'

    with open(csv_file, 'r', encoding='utf-8-sig') as f:  # 使用utf-8-sig编码以处理BOM
        reader = csv.DictReader(f)  # 使用DictReader可以直接将每行转换为字典
        for row in reader:
            # 插入数据到MongoDB集合中
            collection.insert_one(row)

        # 关闭MongoDB连接
client.close()