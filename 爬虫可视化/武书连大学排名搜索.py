import pandas as pd


def search_ranking(year, university):
    filename = f"{year}武书连中国大学排名.csv"
    try:
        df = pd.read_csv(filename)
    except FileNotFoundError:
        print(f"文件 {filename} 未找到，请检查年份和文件路径是否正确。")
        return False

    result = df[df['学校'] == university]
    if not result.empty:
        print(f"{university} 在 {year} 年的排名是：{result['排名'].iloc[0]}")
        return True
    else:
        print(f"{university} 在 {year} 年的数据未找到。")
        return False


def main():
    while True:
        year = input("请输出您要搜索的年份（2015-2023）：")
        if not year.isdigit() or int(year) < 2015 or int(year) > 2023:
            print("年份输入错误，请输入2015至2023之间的年份。")
            continue

        university = input("请输出您要搜索的大学：")
        found = search_ranking(year, university)

        while True:
            choice = input("按1继续查找，按0退出程序：")
            if choice == '1':
                break  # 继续查找
            elif choice == '0':
                print("退出程序。")
                return  # 退出程序
            else:
                print("无效输入，请输入1或0。")  # 提示无效输入

        if not found:
            print("未找到相关信息，您可以选择继续查找或退出。")


if __name__ == "__main__":
    main()
