import pymysql
import csv
import os

# 数据库服务器配置
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '20031010',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

# 尝试连接到MySQL服务器（不指定数据库）
connection = pymysql.connect(**db_config)

# 创建数据库（如果不存在）
with connection.cursor() as cursor:
    cursor.execute("CREATE DATABASE IF NOT EXISTS AlumniAssociation")

db_config['db'] = 'AlumniAssociation'
connection = pymysql.connect(**db_config)


def import_csv_to_db(year, csv_file):
    table_name = f'AlumniData_{year}'

    # 创建表（如果尚未存在）
    with connection.cursor() as cursor:
        cursor.execute(f"""  
        CREATE TABLE IF NOT EXISTS {table_name} (  
            id INT AUTO_INCREMENT PRIMARY KEY,  
            排名 INT,  
            排名1 INT,  
            学校 VARCHAR(255)  
        ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;  
        """)

        # 导入CSV数据到数据库表
    with open(csv_file, 'r', encoding='utf-8-sig') as f, connection.cursor() as cursor:  # 使用utf-8-sig处理BOM
        csv_reader = csv.reader(f)
        next(csv_reader)  # 跳过标题行
        for row in csv_reader:
            cursor.execute(f"INSERT INTO {table_name} (排名, 排名1, 学校) VALUES (%s, %s, %s)",
                           (row[0], row[1], row[2]))

            # 提交事务
    connection.commit()


# 循环处理2015到2024年的数据
for year in range(2015, 2025):
    csv_file = f"{year}校友会中国大学排名.csv"
    if os.path.exists(csv_file):
        import_csv_to_db(year, csv_file)
        print(f"Data from {csv_file} has been imported successfully.")
    else:
        print(f"File {csv_file} does not exist.")

    # 关闭数据库连接
connection.close()
