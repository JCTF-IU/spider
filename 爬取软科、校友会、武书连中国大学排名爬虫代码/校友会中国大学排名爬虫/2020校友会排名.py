import csv
import requests
from bs4 import BeautifulSoup

url = 'http://www.chinaxy.com/2022index/news/news.jsp?information_id=709'

# 发送HTTP请求
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
response = requests.get(url, headers=headers)
response.raise_for_status()  # 如果请求失败，抛出异常

# 解析HTML内容
soup = BeautifulSoup(response.text, 'html.parser')

# 找到所有表格
all_tables = soup.find_all('table')

target_tables = all_tables[7:9]

# 用于存储所有排名的列表
all_rankings = []

# 迭代处理目标表格
for table in target_tables:
    rows = table.find_all('tr')
    if len(rows) > 1:
        rows = rows[1:]

        # 提取排名信息
    for row in rows:
        cols = row.find_all('td')
        if cols:
            rank_str = cols[0].get_text(strip=True) if cols else ''
            # 处理并列排名
            if '*' in rank_str:
                rank = int(rank_str.split('*')[0])  # 提取数字部分作为排名
            else:
                try:
                    rank = int(rank_str)
                except ValueError:
                    rank = None  # 如果转换整数失败，则设置为None

            if rank is not None:  # 确保排名是有效的
                all_rankings.append({
                    '排名1': rank,
                    '学校': cols[1].get_text(strip=True) if len(cols) > 1 else '',
                    '总分': cols[2].get_text(strip=True) if len(cols) > 2 else '',
                    '星级': cols[3].get_text(strip=True) if len(cols) > 3 else '',
                    '办学层次': cols[4].get_text(strip=True) if len(cols) > 4 else '',
                })

                # 取前两百条记录
            top_200_rankings = all_rankings[:200]
for i, ranking in enumerate(all_rankings, start=1):
    ranking['排名'] = i

# 将排名信息保存为CSV文件
with open('../data1/2020校友会中国大学排名.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['排名', '排名1', '学校', '总分', '星级', '办学层次']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()  # 写入表头
    for ranking in all_rankings:
        writer.writerow(ranking)  # 写入每一行数据

print("CSV文件已保存。")
