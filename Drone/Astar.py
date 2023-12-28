# -*- coding: utf-8 -*-

import math
import os
import csv
from pylab import *
import matplotlib.pyplot as plt
from django.shortcuts import render
import random
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from .algorithm import dijkstra, load_graph_from_csv

# 图像上显示中文
mpl.rcParams['font.sans-serif'] = ['SimHei']

# 随机生成全地图人流量
width = 245
height = 88
people = {}  # {(x, y):500}
max_people = 0
for x in range(width):
    for y in range(height):
        people[(x, y)] = random.randint(0, 1000)

# 更新地标周围人流量
num_dict: dict = {}
current_directory = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_directory, 'data.csv')
with open(file_path, mode='r') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        pos = row['位置']
        num = row['人流量']
        num_dict[pos] = int(num)

current_directory = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_directory, 'landmarks.csv')
with open(file_path, mode='r') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        pos = row['Name']
        pos_x = int(row['X'])
        pos_y = int(row['Y'])
        for x in range(pos_x - 5, pos_x + 5):
            for y in range(pos_y - 5, pos_y + 5):
                people[(x, y)] = num_dict[pos] + random.randint(0, 500)
                max_people = max(max_people, people[(x, y)])


class AStar:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[""] * height for _ in range(width)]

    def set_obstacle(self, x, y, obstacle_width, obstacle_height, obstacle_name):
        for i in range(x, x + obstacle_width):
            for j in range(y, y + obstacle_height):
                self.grid[i][j] = obstacle_name

    def heuristic(self, x, y, end_x, end_y):
        dx = abs(x - end_x)
        dy = abs(y - end_y)
        return dx + dy

    def astar(self, start, end):
        open_set = [(0, start)]
        came_from = {}
        g_score = {pos: float('inf') for pos in self.all_positions()}
        g_score[start] = 0
        f_score = {pos: float('inf') for pos in self.all_positions()}
        f_score[start] = self.heuristic(*start, *end)

        while open_set:
            current = min(open_set, key=lambda x: f_score[x[1]])
            if current[1] == end:
                return self.reconstruct_path(came_from, end)
            open_set.remove(current)
            for neighbor in self.neighbors(current[1]):
                tentative_g_score = g_score[current[1]] + self.heuristic(*current[1], *neighbor) + people[
                    current[1]] / 3000
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current[1]
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + self.heuristic(*neighbor, *end)
                    if neighbor not in [pos for (_, pos) in open_set]:
                        open_set.append((f_score[neighbor], neighbor))

    def all_positions(self):
        return [(x, y) for x in range(self.width) for y in range(self.height)]

    def neighbors(self, pos):
        x, y = pos
        candidates = [
            (x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
            (x - 1, y), (x + 1, y),
            (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)
        ]
        return [p for p in candidates if self.valid_position(p)]

    def valid_position(self, pos):
        x, y = pos
        return 0 <= x < self.width and 0 <= y < self.height and not self.grid[x][y]

    def reconstruct_path(self, came_from, current):
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path


def show_map(a_star, path_res):
    print(path_res)
    fig, ax = plt.subplots(figsize=(18, 12))
    ax.set_aspect('equal')
    ax.set_xlim(0, a_star.width)
    ax.set_ylim(0, a_star.height)
    # 全地图色彩
    ax.add_patch(plt.Rectangle((0, 0), 245, 88, color='floralwhite'))

    colors = ["w", "r"]
    color_map = LinearSegmentedColormap.from_list("my_color_map", colors, N=1000)
    color = [plt.get_cmap(color_map, 2000)(i) for i in range(0, max_people // 10 + 1)]

    # 读取人流量画图显示
    for x in range(width):
        for y in range(height):
            ax.add_patch(plt.Rectangle((x, y), 1, 1, color=color[people[(x, y)] // 10]))

    # 画固定地标
    for x in range(a_star.width):
        for y in range(a_star.height):
            if a_star.grid[x][y] != "":
                ax.add_patch(plt.Rectangle((x, y), 1, 1, color='g'))
                ax.text(x, y - 2, a_star.grid[x][y], ha='center', va='center', fontsize=8, color='black')

    # 画起点和终点
    for p in path_res:
        ax.add_patch(plt.Rectangle(p, 1, 1, color='green'))
        # ax.add_patch(plt.Rectangle(end, 1, 1, color='blue'))

    script_dir = os.path.dirname(os.path.abspath(__file__))
    save_path = os.path.join(script_dir, '../static', 'img', 'result1.png')

    # 绘制路径
    for i in range(0, len(path_res)-1):
        start = path_res[i]
        end = path_res[i+1]
        path = a_star.astar(start, end)
        if path:
            path_x, path_y = zip(*path)
            plt.plot(path_x, path_y, 'k-')  # 黑色实线路径

    plt.grid(True, color='black', linewidth=0.5)
    plt.savefig(save_path, bbox_inches='tight')
    # plt.show()
    return


def search_path(request):
    ctx = {'show_image': 0}
    width, height = 245, 88
    astar = AStar(width, height)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file = os.path.join(script_dir, 'landmarks.csv')
    obstacles = []
    path_res = []
    if request.POST:
        start_pos = request.POST['start']
        end_pos = request.POST['end']
        file = os.path.join(script_dir, 'roads.csv')
        graph = load_graph_from_csv(file)
        res = dijkstra(graph, start_pos, end_pos)
        path_res = [(0, 0)] * len(res)
        with open(csv_file, mode='r') as csv_read_file:
            reader = csv.DictReader(csv_read_file)
            for row in reader:
                if row['Name'] in res:
                    path_res[res.index(row['Name'])] = (int(row['X']), int(row['Y']))
                else:
                    obstacles.append((int(row['X']), int(row['Y']), int(row['Width']), int(row['Height']), row['Name']))

    if len(path_res) <= 1:
        ctx['msg'] = "未搜索到相关信息"
        ctx["search_title"] = "查询失败"
        return render(request, "search_path.html", ctx)

    elif len(path_res) >= 2:
        ctx['show_image'] = True
        ctx['msg'] = "搜索到从" + start_pos + "到" + end_pos + "的最短路径\n" + '-> '.join(res)
        ctx['search_title'] = "查询成功"
        for obstacle in obstacles:
            x_pos, y_pos, obstacle_width, obstacle_height, obstacle_name = obstacle
            astar.set_obstacle(x_pos, y_pos, obstacle_width, obstacle_height, obstacle_name)
        show_map(astar, path_res)
        return render(request, "search_path.html", ctx)

    else:
        ctx['show_image'] = False
        ctx['msg'] = "未找到从" + start_pos + "到" + end_pos + "的最短路径\n"
        ctx['search_title'] = "查询失败"
        return render(request, "search_path.html", ctx)


def create_roads_csv():
    width, height = 245, 88
    astar = AStar(width, height)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file = os.path.join(script_dir, 'landmarks.csv')
    obstacles = []
    with open(file, mode='r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            obstacles.append((int(row['X']), int(row['Y']), int(row['Width']), int(row['Height']), row['Name']))

    # 创建图像
    fig, ax = plt.subplots(figsize=(24, 16))  # 设置宽度为12，高度为8
    ax.set_aspect('equal')
    ax.set_xlim(0, astar.width)
    ax.set_ylim(0, astar.height)

    # 绘制路径
    for obstacle in obstacles:
        x, y, _, _, _ = obstacle
        for other_obstacle in obstacles:
            if obstacle == other_obstacle:
                continue
            ox, oy, _, _, _ = other_obstacle
            distance = math.sqrt((ox - x) ** 2 + (oy - y) ** 2)
            if distance <= 27:  # 连接范围小于等于20的障碍物
                plt.plot([x, ox], [y, oy], 'b-')  # 使用蓝色实线连接

    # 显示障碍物
    for obstacle in obstacles:
        x, y, width, height, name = obstacle
        ax.add_patch(plt.Rectangle((x, y), width, height, color='red'))
        ax.text(x, y - 2, name, ha='center', va='center', fontsize=8, color='black')

    # 显示图像
    plt.grid(True, color='black', linewidth=0.5)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    save_path = os.path.join(script_dir, '../static', 'img', 'map.png')
    plt.savefig(save_path, bbox_inches='tight')
    # plt.show()

