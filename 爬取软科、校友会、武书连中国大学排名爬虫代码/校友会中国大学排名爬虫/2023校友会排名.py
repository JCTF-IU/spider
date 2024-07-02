import requests
from bs4 import BeautifulSoup
import pandas as pd


# 获取网页信息
def gethtml():
    try:
        url = 'http://www.jdxzz.com/paiming/2023/0407/9876956.html'
        response = requests.get(url)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return response.text
    except:
        return None

    # 解析网页内容


def htmlsoup(txt):
    if txt is None:
        return []
    soup = BeautifulSoup(txt, 'html.parser')
    tables = soup.find_all('table')
    college_data = []
    count = 0
    for table in tables:
        rows = table.find_all('tr')
        for row in rows[1:]:  # 跳过表头
            if count >= 200:
                return college_data  # 达到200条数据后直接返回
            cells = row.find_all('td')
            college_info = [cell.get_text(strip=True) for i, cell in enumerate(cells) if i != 2]
            college_data.append(college_info)
            count += 1
    return college_data


# 主函数
def run():
    html_content = gethtml()
    if html_content is None:
        print("获取网页内容失败！")
        return
    college_data = htmlsoup(html_content)

    # 创建DataFrame
    df = pd.DataFrame(college_data, columns=['排名1', '学校', '总分', '星级', '办学层次'])

    df.insert(0, '排名', range(1, len(df) + 1))

    # 如果数据超过200条，则截取前200条
    df = df.head(200)

    # 保存到CSV
    df.to_csv('../data1/2023校友会中国大学排名.csv', index=False, encoding='utf-8-sig')
    print("数据已保存到文件中。")


if __name__ == '__main__':
    run()
