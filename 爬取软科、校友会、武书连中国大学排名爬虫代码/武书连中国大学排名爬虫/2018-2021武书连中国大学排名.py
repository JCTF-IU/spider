import requests
from bs4 import BeautifulSoup
import csv


# 封装成一个函数来处理数据抓取和CSV写入
def scrape_and_save_data(urls, csv_filename, max_records=200):
    # 设置计数器
    counter = 0

    # 打开一个CSV文件用于写入
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        # 创建CSV写入器
        csvwriter = csv.writer(csvfile)

        # 写入表头
        headers = ['排名', '学校', '地区']
        csvwriter.writerow(headers)

        # 遍历所有URL
        for url in urls:
            # 如果已经达到max_records条记录，则停止处理
            if counter >= max_records:
                break

                # 使用requests库获取网页内容
            response = requests.get(url)
            response.encoding = 'utf-8'

            # 使用BeautifulSoup解析HTML内容
            soup = BeautifulSoup(response.text, 'html.parser')

            # 找到表格
            table = soup.find('table')

            # 找到所有的<tr>标签
            rows = table.find_all('tr')

            # 遍历表格的每一行
            for row in rows[1:]:  # 跳过表头行
                # 如果已经达到max_records条记录，则停止处理
                if counter >= max_records:
                    break

                    # 找到行内的所有单元格
                cells = row.find_all(['td', 'th'])

                # 提取数据并写入CSV
                if len(cells) >= 3:
                    ranking = cells[0].get_text(strip=True)
                    university_name = cells[1].find('a').get_text(strip=True) if cells[1].find('a') else ''
                    location = cells[2].find('a').get_text(strip=True) if cells[2].find('a') else ''

                    # 写入一行数据
                    csvwriter.writerow([ranking, university_name, location])

                    # 增加计数器
                    counter += 1

    print(f"数据已保存到文件：{csv_filename}。")


urls_2018 = [
    'https://www.zjut.cc/article-164302-1.html',
    'https://www.zjut.cc/article-164302-2.html',
    'https://www.zjut.cc/article-164302-3.html',
    'https://www.zjut.cc/article-164302-4.html'
]
csv_filename_2018 = '../data2/2018武书连中国大学排名.csv'
scrape_and_save_data(urls_2018, csv_filename_2018)

# 2019年的数据
urls_2019 = [
    'https://www.zjut.cc/article-171253-1.html',
    'https://www.zjut.cc/article-171253-2.html',
    'https://www.zjut.cc/article-171253-3.html',
    'https://www.zjut.cc/article-171253-4.html'
]
csv_filename_2019 = '../data2/2019武书连中国大学排名.csv'
scrape_and_save_data(urls_2019, csv_filename_2019)

# 2020年的数据
urls_2020 = [
    'https://www.zjut.cc/article-391273-1.html',
    'https://www.zjut.cc/article-391273-2.html',
    'https://www.zjut.cc/article-391273-3.html',
    'https://www.zjut.cc/article-391273-4.html'
]
csv_filename_2020 = '../data2/2020武书连中国大学排名.csv'
scrape_and_save_data(urls_2020, csv_filename_2020)

# 2021年的数据
urls_2021 = [
    'https://www.zjut.cc/article-391274-1.html',
    'https://www.zjut.cc/article-391274-2.html',
    'https://www.zjut.cc/article-391274-3.html',
    'https://www.zjut.cc/article-391274-4.html'
]
csv_filename_2021 = '../data2/2021武书连中国大学排名.csv'
scrape_and_save_data(urls_2021, csv_filename_2021)