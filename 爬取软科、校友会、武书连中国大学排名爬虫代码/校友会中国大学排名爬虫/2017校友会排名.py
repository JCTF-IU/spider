import csv
import requests
from bs4 import BeautifulSoup


# 定义一个函数来抓取和解析网页上的表格数据
def get_rankings(url, table_index):
    # 发送HTTP请求
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # 如果请求失败，抛出异常

    # 解析HTML内容
    soup = BeautifulSoup(response.text, 'html.parser')

    # 找到所有表格，并选择目标表格
    all_tables = soup.find_all('table')
    target_table = all_tables[table_index]

    # 提取排名信息
    rows = target_table.find_all('tr')
    rankings = []
    for row in rows[1:]:  # 跳过表头行
        cols = row.find_all('td')
        rank_str = cols[0].get_text(strip=True)
        # 处理并列排名
        if '*' in rank_str:
            rank = int(rank_str.split('*')[0])
        else:
            try:
                rank = int(rank_str)
            except ValueError:
                continue

        rankings.append({
            '排名1': rank,
            '学校': cols[1].get_text(strip=True),
            '地区': cols[2].get_text(strip=True),
            '总分': cols[4].get_text(strip=True),
        })
    return rankings


# 抓取两个网页上的表格数据
url1 = 'http://www.chinaxy.com/2022index/news/news.jsp?information_id=1471'
url2 = 'http://www.chinaxy.com/2022index/news/mynews.jsp?information_id=1472'

rankings1 = get_rankings(url1, 5)
rankings2 = get_rankings(url2, 1)

all_rankings = rankings1 + rankings2
for i, ranking in enumerate(all_rankings, start=1):
    ranking['排名'] = i

# 将排名信息保存为CSV文件
with open('../data1/2017校友会中国大学排名.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    fieldnames = ['排名', '排名1', '学校', '地区', '总分']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()  # 写入表头
    writer.writerows(all_rankings)  # 写入所有数据

print("CSV文件已保存。")