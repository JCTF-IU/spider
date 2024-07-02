import csv
import pymysql

# MySQL数据库配置
config = {
    'host': 'localhost',
    'user': 'root',
    'password': '20031010',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

# 连接数据库
connection = pymysql.connect(**config)

try:
    with connection.cursor() as cursor:
        # 创建数据库（如果尚不存在）
        cursor.execute("CREATE DATABASE IF NOT EXISTS ruanke")

        # 选择数据库
        cursor.execute("USE ruanke")

        # 为每年的数据创建一个表，并从对应的CSV文件中导入数据
        for year in range(2015, 2025):
            table_name = f'ruanke_{year}'
            create_table_query = f"""  
            CREATE TABLE IF NOT EXISTS {table_name} (  
                id INT AUTO_INCREMENT PRIMARY KEY,  
                学校 VARCHAR(255) NOT NULL,  
                省份 VARCHAR(255) NOT NULL,  
                类别 VARCHAR(255) NOT NULL,  
                排名 INT NOT NULL,  
                总分 FLOAT NOT NULL  
            )  
            """
            cursor.execute(create_table_query)

            csv_file = f'{year}年软科中国大学排名.csv'

            with open(csv_file, 'r', encoding='utf-8-sig') as f:  # 使用utf-8-sig编码以处理BOM
                reader = csv.reader(f)
                next(reader)  # 跳过CSV文件的标题行
                for row in reader:
                    insert_query = f"""  
                    INSERT INTO {table_name} (学校, 省份, 类别, 排名, 总分)  
                    VALUES (%s, %s, %s, %s, %s)  
                    """
                    cursor.execute(insert_query, row)
                    # 提交事务
            connection.commit()
finally:
    connection.close()