import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号


def read_data(years):
    rankings = {}
    for year in years:
        filename = f"{year}武书连中国大学排名.csv"
        df = pd.read_csv(filename)
        rankings[year] = df
    return rankings


def plot_ranking(university, rankings, years):
    university_ranks = {}
    for year in years:
        rank_df = rankings[year]
        rank = rank_df[rank_df['学校'] == university]['排名']
        if not rank.empty:
            university_ranks[year] = rank.iloc[0]
        else:
            university_ranks[year] = None

    plt.figure(figsize=(10, 6))
    valid_ranks = [rank for rank in university_ranks.values() if rank is not None]
    valid_years = [year for year, rank in university_ranks.items() if rank is not None]
    plt.plot(valid_years, valid_ranks, marker='o', linestyle='-', color='b')
    plt.title(f'{university} 的排名变化')
    plt.xlabel('年份')
    plt.ylabel('排名')
    plt.grid(True)
    plt.show()


def main():
    years = list(range(2015, 2024))
    while True:
        rankings = read_data(years)
        print("请输入大学名称（输入0退出）：")
        university = input()
        if university == '0':
            break
        plot_ranking(university, rankings, years)
        print("按1重新开始，按0退出：")
        choice = input()
        if choice != '1':
            break


if __name__ == "__main__":
    main()
