import csv
import pymysql
import os

# MySQL配置
mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '20031010',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

# 连接到MySQL
connection = pymysql.connect(**mysql_config)
cursor = connection.cursor()

# 创建数据库
database_name = 'wushulian'
create_database_sql = f"CREATE DATABASE IF NOT EXISTS {database_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
cursor.execute(create_database_sql)

# 选择新创建的数据库
connection.select_db(database_name)


def import_csv_to_mysql(year, csv_file):
    table_name = f'wushulian_{year}'

    # 创建表SQL语句
    create_table_sql = f'''  
    CREATE TABLE IF NOT EXISTS {table_name} (  
        id INT AUTO_INCREMENT PRIMARY KEY,  
        排名 INT NOT NULL,  
        学校 VARCHAR(255) NOT NULL  
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;  
    '''
    cursor.execute(create_table_sql)

    # 读取CSV文件并插入数据到表中
    with open(csv_file, 'r', encoding='utf-8-sig') as f:
        csv_reader = csv.reader(f)
        next(csv_reader)  # 跳过标题行
        for row in csv_reader:
            rank, school = int(row[0]), row[1]
            insert_sql = f"INSERT INTO {table_name} (排名, 学校) VALUES ({rank}, '{school}');"
            cursor.execute(insert_sql)

            # 提交事务
    connection.commit()


# 循环处理2015到2023年的数据
for year in range(2015, 2024):
    csv_file = f"{year}武书连中国大学排名.csv"
    if os.path.exists(csv_file):
        import_csv_to_mysql(year, csv_file)
        print(f"Data from {csv_file} has been imported successfully.")
    else:
        print(f"File {csv_file} does not exist.")

    # 关闭数据库连接
cursor.close()
connection.close()
