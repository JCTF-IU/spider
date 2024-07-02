import csv
import requests
from bs4 import BeautifulSoup

url = 'https://www.phb123.com/jiaoyu/gx/64182.html'

# 发送HTTP请求获取网页内容
response = requests.get(url)
response.encoding = 'utf-8'  # 根据网页的实际编码设置
response.raise_for_status()  # 确保请求成功

# 使用BeautifulSoup解析HTML内容
soup = BeautifulSoup(response.text, 'html.parser')

# 找到包含排名数据的表格
table = soup.find('table')

# 准备CSV文件并写入表头
csv_file_path = '../data2/2023武书连中国大学排名.csv'
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['排名', '学校', '综合得分', '地区'])  # 写入表头

    # 初始化计数器
    count = 0

    # 遍历表格的每一行（跳过表头行）
    for row in table.find_all('tr')[1:]:  # 假设第一行是表头，所以从第二行开始遍历
        if count >= 200:  # 当爬取到200条数据时停止
            break

        cols = row.find_all('td')  # 获取当前行的所有列

        # 提取所需列的数据：排名、学校名称、综合得分、地区
        rank = cols[0].get_text(strip=True)
        university_name = cols[1].get_text(strip=True)
        total_score = cols[2].get_text(strip=True)
        region = cols[5].get_text(strip=True)

        # 将数据写入CSV文件
        csvwriter.writerow([rank, university_name, total_score, region])

        # 增加计数器
        count += 1

print(f"数据已成功保存到文件：{csv_file_path}中。")