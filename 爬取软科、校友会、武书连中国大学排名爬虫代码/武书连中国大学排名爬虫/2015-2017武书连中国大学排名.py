import csv
import requests
from bs4 import BeautifulSoup


def scrape_and_save(url, filename, encoding, skip_header_rows=1):
    # 发送HTTP请求
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
    }
    response = requests.get(url, headers=headers)
    response.encoding = encoding
    response.raise_for_status()  # 如果请求失败，抛出异常

    # 解析HTML内容
    soup = BeautifulSoup(response.text, 'html.parser')

    target_table = soup.find('table')

    # 用于存储所有排名的列表
    all_rankings = []

    # 提取排名信息
    rows = target_table.find_all('tr')
    rows = rows[skip_header_rows:]

    for row in rows:
        cols = row.find_all('td')
        rank = cols[0].get_text(strip=True) if cols else ''
        school_name = cols[1].get_text(strip=True) if len(cols) > 1 else ''
        comprehensive_score = cols[2].get_text(strip=True) if len(cols) > 2 else ''
        type_ = cols[11].get_text(strip=True) if len(cols) > 11 else ''

        all_rankings.append({
            '排名': rank,
            '学校': school_name,
            '综合得分': comprehensive_score,
            '类型': type_
        })

        # 将排名信息保存为CSV文件
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['排名', '学校', '综合得分', '类型']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()  # 写入表头
        for ranking in all_rankings:
            writer.writerow(ranking)  # 写入每一行数据

    print(f"CSV文件已保存到 {filename}")


# 2015年的数据，跳过二行表头
scrape_and_save(
    'https://edu.sina.com.cn/gaokao/2015-03-18/1010460946.shtml',
    '../data2/2015武书连中国大学排名.csv',
    'gbk',
    skip_header_rows=2
)

# 2016年的数据，跳过二行表头
scrape_and_save(
    'https://edu.sina.com.cn/gaokao/2016-04-06/doc-ifxqxcnr5380588.shtml',
    '../data2/2016武书连中国大学排名.csv',
    'utf-8',
    skip_header_rows=2
)

# 2017年的数据，跳过一行表头
scrape_and_save(
    'https://edu.sina.com.cn/gaokao/2016-12-26/doc-ifxyxury8701224.shtml',
    '../data2/2017武书连中国大学排名.csv',
    'utf-8',
    skip_header_rows=1
)