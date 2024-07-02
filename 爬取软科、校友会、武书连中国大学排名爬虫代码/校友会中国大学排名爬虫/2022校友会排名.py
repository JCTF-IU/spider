import csv
import requests
from bs4 import BeautifulSoup

url = 'http://www.chinaxy.com/2022index/news/news.jsp?information_id=1930'

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

ninth_table = all_tables[12]

# 用于存储排名信息的列表
rankings = []

# 提取排名信息，并只取前200条数据
rows = ninth_table.find_all('tr')
if len(rows) > 0:
    rows = rows[1:]

# 初始化计数器
counter = 0

for row in rows:
    if counter >= 200:  # 只取前200条数据
        break
    cols = row.find_all('td')
    cols_length = len(cols)
    if cols_length > 0:
        rank_str = cols[0].get_text(strip=True) if cols_length > 0 else ''
        # 处理并列排名
        if '*' in rank_str:
            rank = int(rank_str.split('*')[0])  # 提取数字部分作为排名
        else:
            try:
                rank = int(rank_str)
            except ValueError:
                rank = None  # 如果转换整数失败，则设置为None

        if rank is not None:  # 确保排名是有效的
            school_name = cols[1].get_text(strip=True) if cols_length > 1 else ''
            total_score = cols[2].get_text(strip=True) if cols_length > 2 else ''
            star_rating = cols[3].get_text(strip=True) if cols_length > 3 else ''
            educational_level = cols[4].get_text(strip=True) if cols_length > 4 else ''

            rankings.append({
                '排名1': rank,
                '学校': school_name,
                '总分': total_score,
                '星级': star_rating,
                '办学层次': educational_level,
            })
            counter += 1  # 计数器递增

for i, ranking in enumerate(rankings, start=1):
    ranking['排名'] = i

# 将排名信息保存为CSV文件
with open('../data1/2022校友会中国大学排名.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:  # 使用utf-8-sig编码避免中文乱码问题
    fieldnames = ['排名', '排名1', '学校', '总分', '星级', '办学层次']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()  # 写入表头
    for ranking in rankings:
        writer.writerow(ranking)  # 写入每一行数据

print("CSV文件已保存。")
