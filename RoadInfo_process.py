import csv
import os

road_dict = {
    '第一医院': [
        ['启翔湖', '东北', 1],
        ['碧桂园一期', '南', 2],
        ['大雁塔', '东北', 3],
        ['写字楼', '东南', 4]
    ],
    '第二医院': [
        ['碧桂园二期', '北', 2],
        ['碧桂园三期', '西南', 1],
        ['火葬场', '东南', 1.5]
    ],
    '第一小学': [
        ['启翔湖', '西', 6],
        ['写字楼', '西南', 5],
        ['万达', '南', 1.5],
        ['碧桂园一期', '东北', 0.5]
    ],
    '第一中学': [
        ['碧桂园二期', '东北', 0.5],
        ['消防站', '东', 1]
    ],
    '启翔湖': [
        ['第一医院', '西南', 1],
        ['第一小学', '东', 6],
        # 其他道路数据
    ],
    '碧桂园一期': [
        ['第一医院', '北', 2],
        ['第一小学', '西南', 0.5],
        ['第二医院', '东北', 5],
        # 其他道路数据
    ],
    '碧桂园二期': [
        ['第二医院', '南', 2],
        ['大雁塔', '西', 10],
        ['第一小学', '西南', 0.5],
        # 其他道路数据
    ],
    '碧桂园三期': [
        ['万达', '北', 0.5],
        ['第二医院', '东北', 1],
        ['警察局', '西南', 1],
        # 其他道路数据
    ],
    '万达': [
        ['第一小学', '北', 1.5],
        ['写字楼', '西', 0.5],
        ['碧桂园三期', '南', 0.5],
        # 其他道路数据
    ],
    '写字楼': [
        ['第一小学', '东北', 5],
        ['万达', '东', 0.5],
        ['警察局', '南', 2],
        ['消防站', '西南', 2],
        ['第一医院', '西北', 4],
        # 其他道路数据
    ],
    '消防站': [
        ['写字楼', '东北', 2],
        ['警察局', '东南', 3],
        ['第一中学', '西', 1],
        # 其他道路数据
    ],
    '警察局': [
        ['消防站', '西北', 3],
        ['写字楼', '北', 2],
        ['碧桂园三期', '东北', 1],
        # 其他道路数据
    ],
    '火葬场': [
        ['第二医院', '西北', 1.5],
        # 其他道路数据
    ],
    '大雁塔': [
        ['第一医院', '西南', 3],
        ['碧桂园二期', '东', 10],
        # 其他道路数据
    ]
    # 其他位置的道路数据
}


# 插入道路数据的函数
def insertRoad(road_dict, source, road_data):
    if source not in road_dict:
        road_dict[source] = []
    road_dict[source].append(road_data)


csv_file_path = 'roads.csv'

# 检查CSV文件是否存在，如果不存在则创建文件
if not os.path.exists(csv_file_path):
    with open(csv_file_path, mode='w', newline='') as csv_file:
        fieldnames = ['起始位置', '目标位置', '方向', '距离']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()  # 写入表头

# 写入道路数据到CSV文件
with open(csv_file_path, mode='a', newline='') as csv_file:
    fieldnames = ['起始位置', '目标位置', '方向', '距离']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    for source, road_data_list in road_dict.items():
        for road_data in road_data_list:
            row = {'起始位置': source, '目标位置': road_data[0], '方向': road_data[1], '距离': road_data[2]}
            writer.writerow(row)

# 从CSV文件中读取道路数据
with open(csv_file_path, mode='r') as csv_file:
    reader = csv.DictReader(csv_file)

    for row in reader:
        source = row['起始位置']
        destination = row['目标位置']
        direction = row['方向']
        distance = float(row['距离'])

        if source not in road_dict:
            road_dict[source] = []
        road_dict[source].append([destination, direction, distance])

# 输出读取的道路数据
for source, road_data_list in road_dict.items():
    print(f"从{source}出发的道路:")
    for road_data in road_data_list:
        destination, direction, distance = road_data
        print(f"目标位置: {destination}, 方向: {direction}, 距离: {distance}")