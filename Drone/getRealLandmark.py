import json
import os
import requests
import csv
from math import sqrt
from .Astar import create_roads_csv
from . import PosInfo_process
from django.shortcuts import render


# 地标 CSV 文件路径
current_directory = os.path.dirname(os.path.abspath(__file__))
LANDMARK_FILE_PATH = os.path.join(current_directory, 'landmarks.csv')
csv_file_path = os.path.join(current_directory, 'roads.csv')
data_file_path = os.path.join(current_directory, 'data.csv')


def create_or_open_landmark_file(filename):
    if not os.path.exists(filename):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'X', 'Y', 'Width', 'Height'])


def add_landmark_to_file(file, name, x, y, width, height):
    landmarks = {'Name': name, 'X': x, 'Y': y, 'Width': width, 'Height': height}
    new = [landmarks]
    with open(file, mode='r') as csv_file:
        reader = csv.DictReader(csv_file)
        for rows in reader:
            if landmarks['Name'] == rows['Name']:
                continue
            new.append(rows)

    landmark_clear()
    create_or_open_landmark_file(LANDMARK_FILE_PATH)
    with open(file, mode='a') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=['Name', 'X', 'Y', 'Width', 'Height'])
        for rows in new:
            writer.writerow(rows)


def landmark_clear():
    try:
        os.remove(LANDMARK_FILE_PATH)
        # print(f"Landmark file '{LANDMARK_FILE_PATH}' has been deleted.")
    except FileNotFoundError:
        return
        # print(f"Landmark file '{LANDMARK_FILE_PATH}' does not exist.")


min_x, max_x = 108.813, 109.058  # 根据西安市雁塔区实际经纬度设置
min_y, max_y = 34.171, 34.259  # 根据西安市雁塔区实际经纬度设置
matrix_width, matrix_height = 245, 88


def get_landmark_info(city, landmark_name):
    # 使用百度地图API进行地点搜索
    baidu_api_url = "http://api.map.baidu.com/place/v2/search"
    ak = "oieDykNvNYpiu7xe3tIuvFZmdfQQB4pt"  # 请替换为您的百度地图API密钥
    query = f"{landmark_name} {city}"
    params = {
        "query": query,
        "region": city,
        "output": "json",
        "ak": 'oieDykNvNYpiu7xe3tIuvFZmdfQQB4pt',
    }

    response = requests.get(baidu_api_url, params=params)
    data = json.loads(response.text)

    if data.get("status") == 0 and data.get("results"):
        # 获取第一个搜索结果的经纬度坐标
        location = data["results"][0]["location"]
        latitude, longitude = location["lat"], location["lng"]
        return latitude, longitude
    else:
        print("Search failed. Landmark not found.")
        return None


def map_location(city, landmark_name, matrix_width, matrix_height):
    y, x = get_landmark_info(city, landmark_name)

    if x is not None and y is not None:
        # 将坐标映射到矩阵坐标
        x_matrix = int((x - min_x) / (max_x - min_x) * matrix_width)
        y_matrix = int((y - min_y) / (max_y - min_y) * matrix_height)
        return x_matrix, y_matrix
    else:
        return None


def add_new_pos(request):
    city = "西安"
    ctx = {'show_image': False}
    x_matrix = y_matrix = None
    if request.POST:
        if request.POST['pos'] != "":
            landmark_name = request.POST['pos']
            x_matrix, y_matrix = map_location(city, landmark_name, matrix_width, matrix_height)
        if x_matrix is not None and y_matrix is not None:
            create_or_open_landmark_file(LANDMARK_FILE_PATH)
            add_landmark_to_file(LANDMARK_FILE_PATH, landmark_name, x_matrix, y_matrix, 1, 1)
            ctx['msg'] = "成功添加节点！！"
            ctx["search_title"] = "输出结果："
            ctx['show_image'] = True
            create_roads_csv()
            process_roads_csv()
            PosInfo_process.add_data_csv(landmark_name, request.POST['mask'], request.POST['medicine'],
                request.POST['food'], request.POST['flood'], request.POST['height'], request.POST['danger'])
            return render(request, "add_new_pos.html", ctx)
        else:
            create_roads_csv()
            process_roads_csv()
            ctx['msg'] = "添加节点失败"
            ctx["search_title"] = "输出结果："
            return render(request, "add_new_pos.html", ctx)

    else:
        create_roads_csv()
        process_roads_csv()
        ctx['msg'] = ""
        ctx["search_title"] = "输出结果："
        return render(request, "add_new_pos.html", ctx)


def get_landmarks():
    landmarks: dict = {}
    # 从csv文件中读取数据
    current_directory = os.path.dirname(os.path.abspath(__file__))
    LANDMARK_FILE_PATH = os.path.join(current_directory, 'landmarks.csv')
    with open(LANDMARK_FILE_PATH, mode='r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            pos = row['Name']
            pos_x = int(row['X'])
            pos_y = int(row['Y'])
            pos_width = int(row['Width'])
            pos_height = int(row['Height'])

            if pos not in landmarks:
                landmarks[pos] = []
            landmarks[pos] = [[pos_x, pos_y], [pos_width, pos_height]]
    # print(landmarks)
    return landmarks


def process_roads_csv():
    road_dict = get_landmarks()
    with open(csv_file_path, mode='w', newline='') as csv_file:
        fieldnames = ['起始位置', '目标位置', '方向', '距离']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()  # 写入表头
        for pos1, pos1_info in road_dict.items():
            for pos2, pos2_info in road_dict.items():
                if pos1 == pos2:
                    continue
                else:
                    direct = ""
                    delta_x = pos2_info[0][0] - pos1_info[0][0]
                    delta_y = pos2_info[0][1] - pos1_info[0][1]
                    if abs(delta_x) >= abs(sqrt(3) * delta_y):
                        if delta_x >= 0: direct = "东"
                        else: direct = "西"
                    elif abs(delta_y) >= abs(sqrt(3) * delta_x):
                        if delta_y >= 0: direct = "北"
                        else: direct = "南"
                    else:
                        if (delta_x > 0) & (delta_y > 0): direct = "东北"
                        if (delta_x > 0) & (delta_y < 0): direct = "东南"
                        if (delta_x < 0) & (delta_y > 0): direct = "西北"
                        if (delta_x < 0) & (delta_y < 0): direct = "西南"
                    dist = format(sqrt(abs(delta_x) ** 2 + abs(delta_y) ** 2), '.3f')
                    if float(dist) <= 27.0:
                        row = {'起始位置': pos1, '目标位置': pos2, '方向': direct, '距离': dist}
                        writer.writerow(row)


def delete_pos(request):
    ctx = {'show_image': False}
    x_matrix = y_matrix = None
    if request.POST:
        if request.POST['pos'] != "":
            landmark_name = request.POST['pos']
            new = []
            with open(LANDMARK_FILE_PATH, mode='r') as csv_file:
                reader = csv.DictReader(csv_file)
                for rows in reader:
                    if landmark_name == rows['Name']:
                        continue
                    new.append(rows)

            landmark_clear()
            create_or_open_landmark_file(LANDMARK_FILE_PATH)
            with open(LANDMARK_FILE_PATH, mode='a') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=['Name', 'X', 'Y', 'Width', 'Height'])
                for rows in new:
                    writer.writerow(rows)

            new.clear()
            with open(data_file_path, mode='r') as csv_file:
                reader = csv.DictReader(csv_file)
                for rows in reader:
                    if landmark_name == rows['位置']:
                        continue
                    new.append(rows)

            os.remove(data_file_path)
            with open(data_file_path, mode='w') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=['位置', '口罩', '药品', '食物', '人流量', '高度', '危险系数'])
                writer.writeheader()
                for rows in new:
                    writer.writerow(rows)

            ctx['msg'] = "成功删除节点！！"
            ctx["search_title"] = "输出结果："
            ctx['show_image'] = True
            create_roads_csv()
            process_roads_csv()
            return render(request, "delete_pos.html", ctx)

        else:
            create_roads_csv()
            process_roads_csv()
            ctx['msg'] = "删除节点失败"
            ctx["search_title"] = "输出结果："
            return render(request, "delete_pos.html", ctx)

    else:
        create_roads_csv()
        process_roads_csv()
        ctx['msg'] = ""
        ctx["search_title"] = "输出结果："
        return render(request, "delete_pos.html", ctx)





