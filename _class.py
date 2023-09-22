class Pos:
    def __init__(self, n: str, o: dict):
        self.name = n
        self.obj = o

class Road(Pos):
    roadInfo: list = []
    def __init__(self, r_name: str, r_obj: dict):
        Pos.__init__(self,r_name, r_obj)
    def insertPos(self, r_info: list):
        self.roadInfo.append(r_info)
    def findPosInfo(self):
        return self.roadInfo
