import pandas as pd
import matplotlib.pyplot as plt
import os

# 设置Matplotlib的全局字体为黑体
plt.rcParams['font.sans-serif'] = ['SimHei']  # SimHei是黑体字体
plt.rcParams['axes.unicode_minus'] = False  # 确保负号显示正常

university_rankings = {}  # 用于存储各个大学的历年排名
province_rankings = {}  # 用于存储各省份的排名前200的大学数量


def load_data():
    global university_rankings, province_rankings
    for year in range(2015, 2025):
        file_name = f"{year}年软科中国大学排名.csv"
        if os.path.exists(file_name):
            df = pd.read_csv(file_name)
            # 更新university_rankings字典
            for index, row in df.iterrows():
                university_category = row['类别']
                if row['学校'] not in university_rankings:
                    university_rankings[row['学校']] = {'rankings': {}, 'category': university_category}
                university_rankings[row['学校']]['rankings'][year] = row['排名']
                # 更新province_rankings字典
            df_top200 = df[df['排名'] <= 200]
            for province in df_top200['省份'].unique():
                if province not in province_rankings:
                    province_rankings[province] = {}
                province_rankings[province][year] = df_top200[df_top200['省份'] == province].shape[0]


def plot_province_pie_chart():
    # 绘制饼状图的函数
    year = int(input("请输入查询年份（2015-2024）："))
    if year not in range(2015, 2025):
        print("输入的年份不在范围内，请重新输入。")
        return

    data = []
    labels = []
    sizes = []
    for province, counts in province_rankings.items():
        if year in counts:
            data.append(counts[year])
            labels.append(province)
            sizes.append(counts[year])

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')
    plt.title(f"{year}年各省份排名前200大学占比", fontsize=16)  # 设置标题字体大小
    for text in ax1.texts:  # 设置饼图中标签的字体大小
        text.set_fontsize(4)
    plt.show()


def plot_university_ranking_line_chart(university_name):
    # 绘制指定大学2015-2024排名折线图
    if university_name in university_rankings:
        rankings_data = university_rankings[university_name]['rankings']
        years = sorted(rankings_data.keys())
        ranks = [rankings_data[year] for year in years]
        plt.figure(figsize=(10, 6))
        plt.plot(years, ranks, marker='o')
        plt.title(f"{university_name} 2015-2024排名变化折线图", fontsize=16)
        plt.xlabel('年份', fontsize=14)
        plt.ylabel('排名', fontsize=14)
        plt.tick_params(labelsize=12)
        plt.grid(True)
        plt.show()
    else:
        print(f"未找到{university_name}的排名数据。")


def plot_province_university_count_bar_chart():
    year = int(input("请输入查询年份（2015-2024）："))
    if year not in range(2015, 2025):
        print("输入的年份不在范围内，请重新输入。")
        return

        # 准备数据
    province_counts = []
    for province, years_data in province_rankings.items():
        if year in years_data:
            province_counts.append((province, years_data[year]))

            # 对数据进行排序，以便柱状图按照大学数量排序
    province_counts.sort(key=lambda x: x[1], reverse=True)

    # 分离省份名称和对应的大学数量
    provinces, counts = zip(*province_counts)

    # 绘制柱状图
    plt.figure(figsize=(12, 6))
    plt.bar(provinces, counts, width=0.5)  # 设置柱子宽度为0.5，使其更细
    plt.title(f"{year}年各省份排名前200的大学数量", fontsize=12)  # 设置标题和字体大小
    plt.xlabel('省份', fontsize=10)  # 设置X轴标签和字体大小
    plt.ylabel('大学数量', fontsize=10)  # 设置Y轴标签和字体大小
    plt.tick_params(axis='both', labelsize=8)  # 设置坐标轴刻度标签字体大小
    plt.xticks(rotation=90)  # 旋转X轴标签以便于阅读
    plt.tight_layout()  # 调整布局以避免标签重叠
    plt.show()


def plot_university_category_proportion_chart():
    categories = ['理工', '综合', '师范', '农业', '医药', '林业', '财经', '民族']
    years = list(range(2015, 2025))
    category_proportions = {category: {year: 0 for year in years} for category in categories}
    total_universities_per_year = {year: 0 for year in years}

    for uni, data in university_rankings.items():
        if data['category'] in categories:
            for year in years:
                if year in data['rankings']:
                    category_proportions[data['category']][year] += 1
                    total_universities_per_year[year] += 1

    for category in categories:
        for year in years:
            if total_universities_per_year[year] > 0:
                category_proportions[category][year] = (category_proportions[category][year] /
                                                        total_universities_per_year[year]) * 100

    fig, ax = plt.subplots()
    for category in categories:
        ax.plot(years, [category_proportions[category][year] for year in years], marker='o', label=category)
    ax.legend(loc='upper left')
    plt.title('各年份各类别的大学占比', fontsize=16)
    plt.xlabel('年份', fontsize=14)
    plt.ylabel('占比 (%)', fontsize=14)
    plt.grid(True)
    plt.show()


# 主程序


load_data()  # 加载数据
while True:
    print("""    
请选择要查看的内容：    
1. 各省份2015-2024排名前200大学占比饼状图    
2. 各大学2015-2024排名折线图    
3. 各省份大学数量柱状图  
4. 各大学2015-2024分类折线图  
5. 退出程序    
""")
    choice = input("请输入选项（1/2/3/4/5）：")
    if choice == '1':
        plot_province_pie_chart()
    elif choice == '2':
        university_name = input("请输入要查看排名折线图的大学名称：")
        plot_university_ranking_line_chart(university_name)
    elif choice == '3':
        plot_province_university_count_bar_chart()  # 调用新函数
    elif choice == '4':
        plot_university_category_proportion_chart()  # 调用新添加的函数
    elif choice == '5':
        print("程序已退出。")
        break
    else:
        print("无效的输入，请重新输入。")
