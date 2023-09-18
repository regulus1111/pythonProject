import _class

def Floyed(x: _class.Road, y:_class.Road):

    return

if __name__ == '__main__':
    pos_dict: dict = {}
    x = _class.Road("医院", {"口罩": 100})
    pos_dict[x.name] = x
    x.insertPos(['启翔湖', '东北', 1])
    print(x.findPosInfo())
    print(pos_dict[x.name].obj)