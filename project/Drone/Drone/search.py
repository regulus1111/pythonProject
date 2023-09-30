# -*- coding: utf-8 -*-
from . import algorithm
from django.shortcuts import render
import os, csv

def search(request):
    ctx = {}
    current_directory = os.path.dirname(os.path.abspath(__file__))
    ctx['msg'] = "这里什么都没有"
    ctx["search_title"] = "芝士查询结果栏"
    return render(request, "post.html", ctx)

# 接收POST请求数据
def search_pos_info(request):
    ctx = {}
    current_directory = os.path.dirname(os.path.abspath(__file__))
    # 构建文件的完整路径
    file_path = os.path.join(current_directory, 'data.csv')
    with open(file_path, mode='r') as csv_file:
        reader = csv.DictReader(csv_file)
        road_dict = {}
        for row in reader:
            position = row['位置']
            mask = row['口罩']
            medicine = row['药品']
            food = float(row['食物'])

            if position not in road_dict:
                road_dict[position] = []
                road_dict[position].append("口罩数量：" + str(mask))
                road_dict[position].append("药品数量:" + str(medicine))
                road_dict[position].append("食物数量:" + str(food))
    if request.POST:
        if request.POST['q'] in road_dict:
            message = '你搜索的内容为: ' + request.POST['q'] + "\n"
            for i in road_dict[request.POST['q']]:
                message += str(i) + " "
            ctx['msg'] = message
            ctx["search_title"] = "查询地标处信息"
        else:
            ctx['msg'] = "未搜索到相关信息"
            ctx["search_title"] = "查询失败"
    else:
        ctx['msg'] = "这里什么都没有"
        ctx["search_title"] = "提交了空表单"
    return render(request, "post.html", ctx)

def search_path(request):
    ctx = {}
    dm = []
    rm = []
    locations = []
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, 'roads.csv')
    algorithm.floyd(dm, rm, locations, file_path)
    if request.POST:
        if request.POST['start'] in locations and request.POST['end'] in locations:
            start = request.POST['start']
            end = request.POST['end']
            message = algorithm.findPath(start, end, dm, rm, locations)
            ctx['msg'] = message
            ctx["search_title"] = "查询地标处信息"
        else:
            ctx['msg'] = "未搜索到相关信息"
            ctx["search_title"] = "查询失败"
    return render(request, "post.html", ctx)