from Packing import Fenetre
from Component import Cadre
from Component import Rectangle
from Component import Point

def main():
    fenetre=Fenetre(Cadre(Point(200,150),305,200),Rectangle.createData(),800,800)
    fenetre.launch()

main()