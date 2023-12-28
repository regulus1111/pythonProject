# -*- coding: utf-8 -*-
import csv
import os
import sys


# file_path='roads.csv'
def floyd(dm, rm, locations, file_path):
    # 读取CSV文件并构建距离字典
    distance_dict = {}
    with open(file_path, mode='r') as csv_file:
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


def dfs(start: str, end: str, p: list, v: list, ls: list, dm: list, rm: list, rd: dict, ps: dict, dgsum, lensum, file):
    v[ls.index(start)] = 1
    p.append(start)
    dgsum = dgsum + get_pos_danger(start, ps)
    if start == end:
        writer = csv.DictWriter(file, fieldnames=['路径', '长度', '危险系数'])
        # for rows in new:
        #     writer.writerow(rows)
        rows = {'路径': ('-> '.join(p)), '长度': format(float(lensum) * 0.0921, '.3f'), '危险系数': format(dgsum, '.3f')}
        writer.writerow(rows)  # 将路径写入文件
        # file.write('*路径总长度为:' + ' ' + str(format(float(lensum) * 0.0921, '.3f')) + 'KM ' + '*路径危险系数为:' + ' ' + str(format(dgsum, '.3f')) + '\n')  # 路径后依次写入总距离、总危险系数
        v[ls.index(start)] = 0
        p.pop()
        dgsum = dgsum - get_pos_danger(start, ps)
        return
    for i in rd[start]:
        if v[ls.index(i[0])] == 1:
            continue
        else:
            lensum = lensum + i[2]  # 计算路径长度
            dfs(i[0], end, p, v, ls, dm, rm, rd, ps, dgsum, lensum, file)
            lensum = lensum - i[2]  # 回溯
    v[ls.index(start)] = 0
    p.pop()
    dgsum = dgsum - get_pos_danger(start, ps)
    return


def find_multiPath(start, end):
    dm = []
    rm = []
    ls = []
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'roads.csv')
    floyd(dm, rm, ls, file_path)
    path = []  # 存储dfs查找出的路径
    v = []  # 访问过标记1 未访问标记0
    for i in ls:
        v.append(0)
    path_ans = ""  # 以字符串形式存储的路径
    rd = {}  # 读取地图上的路径信息
    ps = {}  # 读取地图上的结点信息
    dgsum = 0  # 路径总危险值
    lensum = 0  # 路径总长度
    read_road_info(rd)
    read_pos_info(ps)

    file_path = os.path.join(script_dir, 'path_ans.csv')
    with open(file_path, mode='w', newline='') as csv_file:
        fieldnames = ['路径', '长度', '危险系数']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()  # 写入表头

    with open(file_path, mode='a') as file:  # 使用with语句打开文件
        dfs(start, end, path, v, ls, dm, rm, rd, ps, dgsum, lensum, file)  # 传入文件对象
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        cnt = 1
        for rows in reader:
            path_ans += "路径" + str(cnt) + "为：" + rows["路径"] + "  路径总长度为：" + rows["长度"] + "   路径总危险系数为：" + rows[
                "危险系数"] + '\n' + '\n '
            cnt += 1
    return path_ans


# 该函数用于find_target_multiPath，用来判断一串字符中包含列表中的所有元素
def contains_all_elements(text, elements):
    for element in elements:
        if element not in text['路径']:
            return False
    return True


def find_target_multiPath(targets: list, start, end):
    ans = []
    targets.append(start)
    targets.append(end)
    if find_multiPath(start, end) == "":
        return False

    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'path_ans.csv')
    cnt = 1
    with open(file_path, 'r+') as file:  # 使用with语句打开文件
        csv_file = csv.DictReader(file)
        for line in csv_file:
            if contains_all_elements(line, targets):
                ans.append("路径{0}:\n".format(cnt) + line['路径'] + targets[0] + '\n')
                cnt += 1
    result = ''.join(ans)
    return result


# csv_file_path='roads.csv'
def read_pos_info(Posdict: dict):
    # 从CSV文件中读取数据
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file_path = os.path.join(script_dir, 'data.csv')
    with open(csv_file_path, mode='r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            position = row['位置']
            Posdict[position] = {
                "口罩": int(row['口罩']),
                "药品": int(row['药品']),
                "食物": int(row['食物']),
                "人流量": int(row['人流量']),
                "高度": int(row['高度']),
                "危险系数": float(row['危险系数'])
            }
    return


# csv_file_path='roads.csv'
def read_road_info(road_dict: dict):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, 'roads.csv')
    with open(file_path, mode='r') as csv_file:
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


def get_pos_danger(pos: str, pos_dict: dict):
    height = pos_dict[pos]["高度"]
    people_traffic = pos_dict[pos]["人流量"]
    danger = pos_dict[pos]["危险系数"]
    result = people_traffic / 10000 + danger

    if height <= 30:
        return result
    elif 30 < height < 100:
        height_difference = height - 30
        height_factor = (height_difference // 10) * 0.025
        return result + height_factor
    else:  # height >= 100
        height_difference = height - 100
        height_factor = (height_difference // 10) * 0.05
        return result + height_factor


# 提示临接结点信息
def adj_node_info(Pos_cur: str):
    # 地图所有结点信息表: 字典
    pos_dict: dict = {}
    read_pos_info(pos_dict)
    if Pos_cur not in pos_dict.keys():
        info = "未搜索到该节点的信息"
        return info

    # 地图所有道路信息表: 字典
    road_dict: dict = {}
    read_road_info(road_dict)
    adj_list: list = road_dict[Pos_cur]  # 临接结点列表: 列表
    # 返回一个提示信息: 字符串
    info: str = '无人机当前位于' + Pos_cur + '\n'
    for nodeInfo in adj_list:
        info += '在无人机当前位置的' + nodeInfo[1] + '方' + str(nodeInfo[2]) + 'km处是' + nodeInfo[0] + ' ' + "人流量" + str(
            pos_dict[nodeInfo[0]]['人流量']) + '\n'
    return info


# 提示最安全路径 txt_file_path='path_ans.csv'
# 返回 最安全路径 危险系数 两个字符串
def find_safe_path(target, start, end):
    dgsum = float('Inf')
    if not find_target_multiPath(target, start, end):
        return False
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, 'path_ans.csv')
    ans = ""
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for rows in reader:
            landmarks = list(rows["路径"].split('-> '))
            if landmarks[0] != start or landmarks[-1] != end or not contains_all_elements(rows, target):
                continue
            if float(rows["危险系数"]) < dgsum:
                dgsum = float(rows["危险系数"])
                ans = rows["路径"]

        return ans + " \n总危险系数为：" + str(dgsum)


# 提示最短路径 txt_file_path='path_ans.csv'
# 返回 最短路径 路径长度 两个字符串
def find_short_path(target, start, end):
    lenth = float('Inf')
    ans = ""
    if not find_target_multiPath(target, start, end):
        return False

    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, "path_ans.csv")
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for rows in reader:
            landmarks = list(rows["路径"].split('-> '))
            if landmarks[0] != start or landmarks[-1] != end or not contains_all_elements(rows, target):
                continue
            if float(rows["长度"]) < lenth:
                lenth = float(rows["长度"])
                ans = rows["路径"]

        return ans + " \n总长度为：" + str(lenth) + "KM\n"


def load_graph_from_csv(filename):
    graph = {}
    with open(filename, mode='r', newline='') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            start = row[0]
            end = row[1]
            distance = float(row[3])
            if start not in graph:
                graph[start] = {}
            graph[start][end] = distance
            if end not in graph:
                graph[end] = {}
            graph[end][start] = distance
    return graph


def dijkstra(graph, start, end):
    visited = set()
    distance = {node: sys.maxsize for node in graph}
    distance[start] = 0
    previous = {}

    while visited != set(graph):
        current_node = None
        for node in graph:
            if node not in visited and (current_node is None or distance[node] < distance[current_node]):
                current_node = node

        visited.add(current_node)

        for neighbor, weight in graph[current_node].items():
            potential = distance[current_node] + weight
            if potential < distance[neighbor]:
                distance[neighbor] = potential
                previous[neighbor] = current_node

    path = []
    while end:
        path.insert(0, end)
        end = previous.get(end)
    return path
#
#
# if __name__ == '__main__':
#     graph = load_graph_from_csv('roads.csv')
#
#     start_point = "西安人才公园"
#     end_point = "陕西大会堂"
#
#     shortest_path = dijkstra(graph, start_point, end_point)
#     print("Shortest Path:", shortest_path)

