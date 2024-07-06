class Point:
    def __init__(self,x,y):
        self.x=x
        self.y=y

class Rectangle:
    def __init__(self,width,height):
        self.point=Point(0,0)
        self.width=width
        self.height=height

    def set_point(self,point:Point):
        self.point=point

    def createData():
        answer=[
            Rectangle(34, 87),
            Rectangle(40, 98),
            Rectangle(56, 43),
            Rectangle(23, 67),
            Rectangle(78, 24),
            Rectangle(12, 55),
            Rectangle(89, 33),
            Rectangle(67, 90),
            Rectangle(6, 23),
            Rectangle(32, 76),
            Rectangle(11, 99),
            Rectangle(98, 88),
            Rectangle(65, 40),
            Rectangle(22, 50),
            Rectangle(37, 94),
            Rectangle(77, 30),
            Rectangle(19, 81),
            Rectangle(44, 63),
            Rectangle(91, 35),
            Rectangle(25, 70),
            Rectangle(33, 60),
            Rectangle(88, 42),
            Rectangle(57, 73),
            Rectangle(66, 28),
            Rectangle(49, 82)
        ]
        return answer

class Cadre:
    def __init__(self,point:Point,width,height):
        self.point=point
        self.width=width
        self.height=height   