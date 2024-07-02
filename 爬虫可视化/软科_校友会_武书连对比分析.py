import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号


def plot_rankings(university, year):
    # 假设你的数据存储在CSV文件中
    df_soft = pd.read_csv(f'{year}年软科中国大学排名.csv')
    df_alumni = pd.read_csv(f'{year}校友会中国大学排名.csv')
    df_wushulian = pd.read_csv(f'{year}武书连中国大学排名.csv')

    soft_rank = df_soft.loc[df_soft['学校'] == university, '排名'].iloc[0]
    alumni_rank = df_alumni.loc[df_alumni['学校'] == university, '排名'].iloc[0]
    wushulian_rank = df_wushulian.loc[df_wushulian['学校'] == university, '排名'].iloc[0]

    # 设置数据
    ranks = [soft_rank, alumni_rank, wushulian_rank]
    labels = ['软科', '校友会', '武书连']
    x = range(len(labels))

    # 绘制柱状图
    plt.bar(x, ranks, tick_label=labels)
    plt.title(f'{university} 在 {year} 年的不同数据源排名')
    plt.xlabel('排名来源')
    plt.ylabel('排名')
    plt.xticks(rotation=45)  # 倾斜x轴标签以便于阅读
    plt.tight_layout()  # 调整布局以避免标签重叠
    plt.show()  # 显示图表


# 用户输入大学名称和年份
university = input("请输入大学名称：")
year = input("请输入年份(2015-2023)：")

# 绘制柱状图
plot_rankings(university, year)
