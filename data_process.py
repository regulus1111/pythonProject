import csv
import os

# 示例数据
pos_dict = {
    '第一医院': {'口罩': 20000, '药品': 10000, '食物': 500},
    '第二医院': {'口罩': 20000, '药品': 15000, '食物': 500},
    '第一小学': {'口罩': 1000, '药品': 100, '食物': 1000},
    '第一中学': {'口罩': 3000, '药品': 100, '食物': 2000},
    '启翔湖': {'口罩': -200, '药品': -100, '食物': -50},
    '碧桂园一期': {'口罩': 30000, '药品': 2000, '食物': 10000},
    '碧桂园二期': {'口罩': 40000, '药品': 3000, '食物': 18000},
    '碧桂园三期': {'口罩': 30000, '药品': 1000, '食物': 12000},
    '万达': {'口罩': 2000, '药品': 100, '食物': 1000},
    '写字楼': {'口罩': 5000, '药品': 100, '食物': 500},
    '消防站': {'口罩': 4000, '药品': 500, '食物': 1200},
    '警察局': {'口罩': 4000, '药品': 600, '食物': 1500},
    '火葬场': {'口罩': 1000, '药品': 200, '食物': 1800},
    '大雁塔': {'口罩': -100, '药品': -50, '食物': -20}
}

csv_file_path = 'data.csv'

# 检查CSV文件是否存在，如果不存在则创建文件
if not os.path.exists(csv_file_path):
    with open(csv_file_path, mode='w', newline='') as csv_file:
        fieldnames = ['位置', '口罩', '药品', '食物']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()  # 写入表头

# 写入CSV文件
with open(csv_file_path, mode='a', newline='') as csv_file:
    fieldnames = ['位置', '口罩', '药品', '食物']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    for position, data in pos_dict.items():
        row = {'位置': position, '口罩': data['口罩'], '药品': data['药品'], '食物': data['食物']}
        writer.writerow(row)

# 从CSV文件中读取数据
with open(csv_file_path, mode='r') as csv_file:
    reader = csv.DictReader(csv_file)

    for row in reader:
        print(row['位置'], row['口罩'], row['药品'], row['食物'])
