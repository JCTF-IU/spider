import requests
from bs4 import BeautifulSoup
import csv

URL = 'https://www.eol.cn/e_html/gk/dxpm/index.shtml'

# 发送HTTP请求获取网页内容
response = requests.get(URL)
response.encoding = 'utf-8'
response.raise_for_status()  # 确保请求成功

# 使用BeautifulSoup解析HTML内容
soup = BeautifulSoup(response.text, 'html.parser')

# 找到页面中的所有表格
tables = soup.find_all('table')

if len(tables) >= 8:
    eighth_table = tables[7]

    rows = eighth_table.find_all('tr')[1:]

    # 准备保存数据到CSV文件
    with open('../data2/2022武书连中国大学排名.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        # 写入CSV文件的标题行
        csvwriter.writerow(['排名', '学校', '总分'])

        # 遍历每一行，提取所需信息，并保存到CSV文件中
        count = 0  # 用于计数，只保存前200条数据
        for row in rows:
            if count >= 200:
                break  # 当达到200条数据时停止循环
            cells = row.find_all('td')
            if len(cells) == 3:
                rank = cells[0].get_text(strip=True)  # 提取排名
                school_name = cells[1].get_text(strip=True)  # 提取学校名称
                total_score = cells[2].get_text(strip=True)  # 提取总分
                csvwriter.writerow([rank, school_name, total_score])  # 写入CSV文件
                count += 1  # 计数器递增
else:
    print("页面中未找到足够的表格。")
