# -*- coding: utf-8 -*-
from . import algorithm
from django.shortcuts import render
import os


def search(request):
    return render(request, "search.html")


# 接收POST请求数据
def search_pos_info(request):
    ctx = {'msg': "这里什么都没有", "search_title": "提交了空表单", "show_image": False}
    if request.POST:
        ctx['msg'] = algorithm.adj_node_info(request.POST['pos'])

    return render(request, "search_pos_info.html", ctx)


def search_all_path(request):
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
            message = algorithm.find_multiPath(start, end)
            ctx['msg'] = message
            ctx["search_title"] = "查询两地之间所有路径"
        else:
            ctx['msg'] = "未搜索到相关信息"
            ctx["search_title"] = "查询失败"
    return render(request, "search_all_path.html", ctx)


def find_target_multiPath(request):
    ctx = {'msg': "这里什么也没有"}
    target = []
    ctx["search_title"] = "查询两地之间所有路径"
    if request.POST:
        if request.POST['start'] and request.POST['end']:
            start = request.POST['start']
            end = request.POST['end']
            if "waypoint" in request:
                for p in request.POST['waypoint']:
                    target.append(p)
            ctx['msg'] = algorithm.find_target_multiPath(target, start, end)
            if not ctx['msg']:
                ctx['msg'] = "未查询到相关结果"
                return render(request, "find_target_multiPath.html", ctx)
    return render(request, "find_target_multiPath.html", ctx)


def find_shortest_path(request):
    ctx = {'msg': "这里什么也没有"}
    target = []
    ctx["search_title"] = "查询两地之间所有路径"
    if request.POST:
        if request.POST['start'] and request.POST['end']:
            start = request.POST['start']
            end = request.POST['end']
            if request.POST.getlist('waypoint'):
                waypoints = request.POST.getlist('waypoint')
                for p in waypoints:
                    target.append(p)
            msg = algorithm.find_short_path(target, start, end)
            if not msg:
                ctx['msg'] = "未查询到两地之间的可行路径，请检查输入" + '\n\n'
            else:
                ctx['msg'] = "途径多个地点的最短路径：\n" + algorithm.find_short_path(target, start, end) + '\n\n'

            msg = algorithm.find_safe_path(target, start, end)
            if not msg:
                ctx['msg'] = "未查询到两地之间的可行路径，请检查输入" + '\n\n'
            else:
                ctx['msg'] += "途径多个地点的最安全路径：\n" + algorithm.find_safe_path(target, start, end)

    return render(request, "find_shortest_path.html", ctx)
