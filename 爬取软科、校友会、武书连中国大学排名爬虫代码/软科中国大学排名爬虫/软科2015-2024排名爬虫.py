import os
import pandas as pd
import requests

if not os.path.exists('data'):
    os.makedirs('data')


def fetch_and_save_data(year, max_rank=200):
    url = f'https://www.shanghairanking.cn/api/pub/v1/bcur?bcur_type=11&year={year}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        print(f'{year}年数据获取成功')
    except requests.exceptions.RequestException as e:
        print(f'{year}年数据获取失败: {e}')
        return

    if data and 'data' in data and 'rankings' in data['data']:
        rankings_data = data['data']['rankings']
        uniname, uniprov, unicate, unirank, unizf = [], [], [], [], []

        for i, item in enumerate(rankings_data):
            if i >= max_rank:
                break
            uniname.append(item['univNameCn'])
            uniprov.append(item['province'])
            unicate.append(item['univCategory'])
            unirank.append(item['ranking'])
            unizf.append(float(item['score']))

        df = pd.DataFrame({
            '学校': uniname,
            '省份': uniprov,
            '类别': unicate,
            '排名': unirank,
            '总分': unizf
        })

        data_dir = '../data'
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        df.to_csv(f'data/{year}年软科中国大学排名.csv', index=False, encoding='utf-8-sig')
        print(f'{year}年数据已保存')


for year in range(2015, 2025):
    fetch_and_save_data(year)
