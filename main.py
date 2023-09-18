def Floyd():
    # 维护任意地标间的最短路径
    return


def findPath(pos_start_name: str, pos_end_name: str):
    # 路由表中找最短路径
    dis = 0

    return dis


def insertPos(pos_dict: dict, pos_name: str, obj_info: dict):
    # 添加地标
    pos_dict[pos_name] = obj_info


def insertRoad(road_dict: dict, pos_cur: str, road_info: list):
    # 添加路径
    road_dict[pos_cur] = road_info


def findPosInfo():
    # 查找地标信息
    pos_name: str
    pos_name = input("要查找的地标：")
    pos_info = pos_dict[pos_name]
    print(pos_name)
    print(pos_info)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    pos_dict: dict = {}
    road_dict: dict = {}
    # 创建城市地标
    insertPos(pos_dict, '第一医院', {'口罩': 20000, '药品': 10000, '食物': 500})
    insertPos(pos_dict, '第二医院', {'口罩': 20000, '药品': 15000, '食物': 500})
    insertPos(pos_dict, '第一小学', {'口罩': 1000, '药品': 100, '食物': 1000})
    insertPos(pos_dict, '第一中学', {'口罩': 3000, '药品': 100, '食物': 2000})
    insertPos(pos_dict, '启翔湖', {'口罩': -200, '药品': -100, '食物': -50})
    insertPos(pos_dict, '碧桂园一期', {'口罩': 30000, '药品': 2000, '食物': 10000})
    insertPos(pos_dict, '碧桂园二期', {'口罩': 40000, '药品': 3000, '食物': 18000})
    insertPos(pos_dict, '碧桂园三期', {'口罩': 30000, '药品': 1000, '食物': 12000})
    insertPos(pos_dict, '万达', {'口罩': 2000, '药品': 100, '食物': 1000})
    insertPos(pos_dict, '写字楼', {'口罩': 5000, '药品': 100, '食物': 500})
    insertPos(pos_dict, '消防站', {'口罩': 4000, '药品': 500, '食物': 1200})
    insertPos(pos_dict, '警察局', {'口罩': 4000, '药品': 600, '食物': 1500})
    insertPos(pos_dict, '火葬场', {'口罩': 1000, '药品': 200, '食物': 1800})
    insertPos(pos_dict, '大雁塔', {'口罩': -100, '药品': -50, '食物': -20})
    # 创建道路
    insertRoad(road_dict, '第一医院', ['启翔湖', '东北', 1])
    insertRoad(road_dict, '第一医院', ['碧桂园一期', '南', 2])
    insertRoad(road_dict, '第一医院', ['大雁塔', '东北', 3])
    insertRoad(road_dict, '第一医院', ['写字楼', '东南', 4])
    insertRoad(road_dict, '第二医院', ['碧桂园二期', '北', 2])
    insertRoad(road_dict, '第二医院', ['碧桂园三期', '西南', 1])
    insertRoad(road_dict, '第二医院', ['火葬场', '东南', 1.5])
    insertRoad(road_dict, '第一小学', ['启翔湖', '西', 6])
    insertRoad(road_dict, '第一小学', ['写字楼', '西南', 5])
    insertRoad(road_dict, '第一小学', ['万达', '南', 1.5])
    insertRoad(road_dict, '第一小学', ['碧桂园一期', '东北', 0.5])
    insertRoad(road_dict, '第一中学', ['碧桂园二期', '东北', 0.5])
    insertRoad(road_dict, '第一中学', ['消防站', '东', 1])
    insertRoad(road_dict, '碧桂园一期', ['第一医院', '北', 2])
    insertRoad(road_dict, '碧桂园一期', ['第一中学', '西南', 0.5])
    insertRoad(road_dict, '碧桂园二期', ['第二医院', '南', 2])
    insertRoad(road_dict, '碧桂园二期', ['大雁塔', '西', 10])
    insertRoad(road_dict, '碧桂园二期', ['第一小学', '西南', 0.5])
    insertRoad(road_dict, '碧桂园三期', ['万达', '北', 0.5])
    insertRoad(road_dict, '碧桂园三期', ['第二医院', '东北', 1])
    insertRoad(road_dict, '碧桂园三期', ['警察局', '西南', 1])
    insertRoad(road_dict, '万达', ['第一小学', '北', 1.5])
    insertRoad(road_dict, '万达', ['写字楼', '西', 0.5])
    insertRoad(road_dict, '万达', ['碧桂园三期', '南', 0.5])
    insertRoad(road_dict, '写字楼', ['第一小学', '东北', 5])
    insertRoad(road_dict, '写字楼', ['万达', '东', 0.5])
    insertRoad(road_dict, '写字楼', ['警察局', '南', 2])
    insertRoad(road_dict, '写字楼', ['消防站', '西南', 2])
    insertRoad(road_dict, '写字楼', ['第一医院', '西北', 4])
    insertRoad(road_dict, '消防站', ['写字楼', '东北', 2])
    insertRoad(road_dict, '消防站', ['警察局', '东南', 3])
    insertRoad(road_dict, '消防站', ['第一中学', '西', 1])
    insertRoad(road_dict, '警察局', ['消防站', '西北', 3])
    insertRoad(road_dict, '警察局', ['写字楼', '北', 2])
    insertRoad(road_dict, '警察局', ['碧桂园三期', '东北', 1])
    insertRoad(road_dict, '火葬场', ['第二医院', '西北', 1.5])
    insertRoad(road_dict, '大雁塔', ['第一医院', '西南', 3])
    insertRoad(road_dict, '大雁塔', ['碧桂园二期', '东', 10])
    # 查找最小路径
    pos_start_name = ''
    pos_end_name = ''
    pos_start_name = input("起始地标：")
    pos_end_name = input("目的地标：")
    print(findPath())
