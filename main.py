import _class
import csv
import os

def findPath(pos_start_name, pos_end_name, distance_matrix, route_matrix, locations):
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

def floyd(dm, rm, locations):
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
    ls = list(distance_dict.keys())
    for i in ls:
        locations.append(i)
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
    for i in distance_matrix:
        dm.append(i)
    for i in route_matrix:
        rm.append(i)

    return

# def find_multiPath(roads: list, dm: list, rm: list):
#     start = roads[0]
#     end = roads.reverse()[0]
#     path = []
#     for i in rm:
#     return

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
    # print(pos_dict)
    # print(road_dict)
    locations = [] # 各个结点位置
    distance_matrix = [] # 距离矩阵
    route_matrix = [] # 路由矩阵
    floyd(distance_matrix, route_matrix, locations)
    findPath("第一医院", "火葬场", distance_matrix, route_matrix, locations)
    print(distance_matrix)
    print(route_matrix)
    roads = ["第一医院","碧桂园三期","第二医院","火葬场"]

