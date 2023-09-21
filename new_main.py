import _class
import csv
import os

import csv

def findPath_floyd(pos_start_name, pos_end_name):
    # 读取CSV文件并构建距离字典
    distance_dict = {}
    with open('roads.csv', mode='r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            start_name = row['起始位置']
            end_name = row['目标位置']
            distance = float(row['距离'])

            if start_name not in distance_dict:
                distance_dict[start_name] = {}
            distance_dict[start_name][end_name] = distance
    # 获取所有唯一的位置
    locations = list(distance_dict.keys())
    # 初始化距离矩阵和路由矩阵
    num_locations = len(locations)
    distance_matrix = [[float('inf')] * num_locations for _ in range(num_locations)]
    route_matrix = [[-1] * num_locations for _ in range(num_locations)]

    # 填充距离矩阵
    for i in range(num_locations):
        for j in range(num_locations):
            if i != j:
                pos_start_name_i = locations[i]
                pos_end_name_j = locations[j]
                if pos_end_name_j in distance_dict.get(pos_start_name_i, {}):
                    distance_matrix[i][j] = distance_dict[pos_start_name_i][pos_end_name_j]
                    route_matrix[i][j] = i  # 设置路由矩阵初始值为直接连接的起始位置索引

    # 弗洛伊德算法
    for k in range(num_locations):
        for i in range(num_locations):
            for j in range(num_locations):
                if distance_matrix[i][j] > distance_matrix[i][k] + distance_matrix[k][j]:
                    distance_matrix[i][j] = distance_matrix[i][k] + distance_matrix[k][j]
                    route_matrix[i][j] = route_matrix[k][j]

    # 查找并打印输入参数的最短路径和距离
    start_index = locations.index(pos_start_name)
    end_index = locations.index(pos_end_name)
    shortest_distance = distance_matrix[start_index][end_index]
    # 构建最短路径
    path = [pos_end_name]
    while route_matrix[start_index][end_index] != start_index:
        end_index = route_matrix[start_index][end_index]
        path.append(locations[end_index])
    path.append(pos_start_name)
    # 逆置path列表
    path.reverse()

    print(f"从{pos_start_name}到{pos_end_name}的最短路径为: {' -> '.join(path)}，距离为{shortest_distance}")
    return

def readPosInfo(Posdict: dict, csv_file_path = 'data.csv'):
    # 从CSV文件中读取数据
    with open(csv_file_path, mode='r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            Posdict[row['位置']] = {"口罩": row['口罩'], "药品": row['药品'], "食物": row['食物']}
    return

def readRoadInfo(road_dict: dict, csv_file_path = 'roads.csv'):
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
    return

if __name__ == '__main__':
    pos_dict = {}
    readPosInfo(pos_dict)
    road_dict = {}
    readRoadInfo(road_dict)
    #x = _class.Road("医院", {"口罩": 100})
    #pos_dict[x.name] = x
    # x.insertPos(['启翔湖', '东北', 1])
    # print(x.findPosInfo())
    # print(pos_dict[x.name].obj)
    print(pos_dict)
    print(road_dict)
    findPath_floyd("第一医院", "第一小学")

