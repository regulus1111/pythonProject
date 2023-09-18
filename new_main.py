import _class
import csv
import os

def Floyed(x: _class.Road, y:_class.Road):

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