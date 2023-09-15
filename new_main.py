class Pos:
    def __init__(self, n: str, o: dict):
        self.name = n
        self.obj = o

class Road(Pos):
    road: dict = {}
    def __init__(self, r_name, r_obj):
        Pos.__init__(self,r_name, r_obj)
    


pos_dict: dict = {}
x = Pos("医院", {"口罩":100})
pos_dict[x.name] = x.obj
print(pos_dict)