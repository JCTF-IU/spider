import os

import requests
from bs4 import BeautifulSoup
import pandas as pd


# 获取并解析指定URL的网页内容
def fetch_and_parse(url, table_index, filename):
    try:
        response = requests.get(url)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        html_content = response.text
        college_data = html_soup(html_content, table_index)

        # 如果没有数据，则直接返回
        if not college_data:
            print(f"在URL {url} 中没有找到数据！")
            return

            # 创建DataFrame
        df = pd.DataFrame(college_data, columns=['排名1', '学校', '总分', '办学类型', '星级', '办学层次'])

        # 保存到CSV
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"数据已保存到文件 {filename} 中。")

    except Exception as e:
        print(f"处理URL {url} 时发生错误: {e}")

    # 解析网页内容并提取指定索引的表格数据


def html_soup(txt, table_index):
    if not txt:
        return []
    soup = BeautifulSoup(txt, 'html.parser')
    tables = soup.find_all('table')

    # 确保表格索引有效
    if table_index >= len(tables):
        return []

    target_table = tables[table_index]
    rows = target_table.find_all('tr')
    college_data = []
    for row in rows[1:]:  # 跳过表头
        cells = row.find_all('td')
        college_info = [cells[i].get_text(strip=True) for i in range(6)]
        college_data.append(college_info)
    return college_data


# 主函数
def run():
    url1 = 'http://www.chinaxy.com/2022index/news/news.jsp?information_id=1238'
    fetch_and_parse(url1, 10, '2018_1校友会中国大学排名.csv')

    url2 = 'http://www.chinaxy.com/2022index/news/news.jsp?information_id=1239'
    fetch_and_parse(url2, 1, '2018_2校友会中国大学排名.csv')

    # 读取两个CSV文件
    df1 = pd.read_csv('2018_1校友会中国大学排名.csv')
    df2 = pd.read_csv('2018_2校友会中国大学排名.csv')

    # 合并两个DataFrame
    combined_df = pd.concat([df1, df2], ignore_index=True)

    combined_df = combined_df.reset_index(drop=False)
    combined_df.rename(columns={'index': '排名'}, inplace=True)
    combined_df['排名'] += 1  # 将序号从1开始

    # 保存合并后的DataFrame到新的CSV文件
    combined_df.to_csv('../data1/2018校友会中国大学排名.csv', index=False, encoding='utf-8-sig')
    print("合并后的CSV文件已保存。")

    # 删除原始的CSV文件
    try:
        os.remove('2018_1校友会中国大学排名.csv')
        os.remove('2018_2校友会中国大学排名.csv')
        print("原始的CSV文件已被删除。")
    except OSError as e:
        print(f"删除文件时出错: {e}")


if __name__ == '__main__':
    run()