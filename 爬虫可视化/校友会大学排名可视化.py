import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号


# 排名变化折线图函数
def plot_university_ranking(university_name, start_year, end_year):
    # 初始化一个空字典来存储每年的排名数据
    rankings = {}

    # 遍历所有年份的CSV文件
    for year in range(start_year, end_year + 1):
        filename = f"{year}校友会中国大学排名.csv"  # 假设文件名格式如此
        try:
            df = pd.read_csv(filename)

            # 查找用户指定的大学在该年的排名
            university_rank = df[df['学校'] == university_name]['排名'].values
            if university_rank.size > 0:
                rankings[year] = university_rank[0]
        except FileNotFoundError:
            print(f"文件 {filename} 未找到。")

            # 检查是否找到了排名数据
    if rankings:
        # 绘制折线图
        plt.figure(figsize=(10, 6))
        plt.plot(list(rankings.keys()), list(rankings.values()), marker='o')
        plt.title(f"{university_name} 在 {start_year}-{end_year} 年的排名变化")
        plt.xlabel('年份')
        plt.ylabel('排名')
        plt.grid(True)
        plt.show()
    else:
        print(f"未找到 {university_name} 在 {start_year}-{end_year} 年的排名数据。")

    # 总分变化折线图函数


def plot_university_score(university_name, start_year, end_year):
    scores = {}
    for year in range(start_year, end_year + 1):
        filename = f"{year}校友会中国大学排名.csv"
        try:
            df = pd.read_csv(filename)
            university_score = df[df['学校'] == university_name]['总分'].values
            if university_score.size > 0:
                scores[year] = university_score[0]
        except FileNotFoundError:
            print(f"文件 {filename} 未找到。")

    if scores:
        plt.figure(figsize=(10, 6))
        plt.plot(list(scores.keys()), list(scores.values()), marker='o')
        plt.title(f"{university_name} 在 {start_year}-{end_year} 年的总分变化")
        plt.xlabel('年份')
        plt.ylabel('总分')
        plt.grid(True)
        plt.show()
    else:
        print(f"未找到 {university_name} 在 {start_year}-{end_year} 年的总分数据。")

    # 主界面循环


while True:
    choice = input("请选择操作：\n1. 各大学排名折线图\n2. 各大学总分变化折线图\n0. 退出程序\n")
    if choice == '1':
        university_name = input("请输入大学名称（输入'退出'结束）：")
        if university_name.lower() == '退出':
            break
        start_year = int(input("请输入开始年份："))
        end_year = int(input("请输入结束年份："))
        plot_university_ranking(university_name, start_year, end_year)
    elif choice == '2':
        university_name = input("请输入大学名称（输入'退出'结束）：")
        if university_name.lower() == '退出':
            break
        start_year = int(input("请输入开始年份："))
        end_year = int(input("请输入结束年份："))
        plot_university_score(university_name, start_year, end_year)
    elif choice == '0':
        break
    else:
        print("无效的选择，请重新输入。")