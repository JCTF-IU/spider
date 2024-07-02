import csv

import requests
from bs4 import BeautifulSoup

url = 'http://www.chinaxy.com/2022index/news/news.jsp?information_id=10972'  # 请替换为实际的URL

# 发送HTTP请求
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
response = requests.get(url, headers=headers)
response.raise_for_status()  # 如果请求失败，抛出异常

# 解析HTML内容
soup = BeautifulSoup(response.text, 'html.parser')

# 找到包含排名的表格
ranking_tables = soup.find_all('table', {'border': '1', 'width': '102%'})

# 用于存储所有排名的列表
all_rankings = []

# 迭代处理所有表格
for table in ranking_tables:
    rows = table.find_all('tr')[1:]  # 跳过表头行

    # 提取排名信息
    for row in rows:
        cols = row.find_all('td')
        rank_str = cols[0].get_text(strip=True)

        # 处理并列排名
        if '*' in rank_str:
            rank = int(rank_str.split('*')[0])  # 提取数字部分作为排名
        else:
            rank = int(rank_str)

        all_rankings.append({
            '排名1': rank,
            '学校': cols[1].get_text(strip=True),
            '总分': cols[2].get_text(strip=True),
            '星级': cols[3].get_text(strip=True),
            '办学层次': cols[4].get_text(strip=True)
        })

    # 取前两百条记录
top_200_rankings = all_rankings[:200]

for i, ranking in enumerate(top_200_rankings, start=1):
    ranking['排名'] = i

# 将排名信息保存为CSV文件
with open('../data1/2024校友会中国大学排名.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['排名', '排名1', '学校', '总分', '星级', '办学层次']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()  # 写入表头
    for ranking in top_200_rankings:
        writer.writerow(ranking)  # 写入每一行数据

print("CSV文件已保存。")
