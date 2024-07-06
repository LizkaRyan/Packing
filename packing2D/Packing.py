import tkinter as tk
from tkinter import ttk
from typing import List
from Component import Cadre
from Component import Rectangle
from Component import Point

class Fenetre:
    def __init__(self,cadre:Cadre,rectangles:List[Rectangle],width,height):
        self.fenetre = tk.Tk()
        self.fenetre.title("2D Packing")
        self.cadre=cadre
        self.rectangles=rectangles
        self.canvas = tk.Canvas(self.fenetre, width=width,height=height)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        #Listner
        btnNFDH = ttk.Button(self.canvas, text="NFDH", command= lambda : self.nfdb())
        btnNFDH.place(x=self.cadre.point.x  , y=self.cadre.point.y+self.cadre.height+10, anchor="n")

        btnFFDH = ttk.Button(self.canvas, text="FFDH", command= lambda : self.ffdh())
        btnFFDH.place(x=self.cadre.point.x+(width // 5), y=self.cadre.point.y+self.cadre.height+10, anchor="n")

        btnBF = ttk.Button(self.canvas, text="Best Fit", command= lambda :self.bf())
        btnBF.place(x=self.cadre.point.x+2*(width // 5), y=self.cadre.point.y+self.cadre.height+10, anchor="n")

    def bf(self):
        print("Mbola tsy vita")

    def launch(self):
        #self.ffdh()
        self.fenetre.mainloop()

    def deleteCanvas(self):
        self.canvas.delete('all')
        position_x,position_y=self.cadre.point.x,self.cadre.point.y
        self.canvas.create_rectangle(position_x, position_y, self.cadre.width+position_x, self.cadre.height+position_y,outline="red")


    def on_canvas_click(self,event):
        print(f"Clique à la position : ({event.x}, {event.y})")

    def nfdb(self):
        self.deleteCanvas()
        self.rectangles.sort(key=lambda rectangle: rectangle.height,reverse=True)
        band_height=self.rectangles[0].height
        new_point=Point(0,0)
        i=0
        for rectangle in self.rectangles:
            i+=1

            if rectangle.width+new_point.x<=self.cadre.width:
                rectangle.set_point(new_point)
                self.putRectangle(rectangle,i)
                new_point.x=rectangle.width+new_point.x

            else:
                if band_height+rectangle.height>self.cadre.height:
                    continue
                new_point.x=0
                new_point.y=band_height
                band_height+=rectangle.height
                rectangle.set_point(new_point)
                self.putRectangle(rectangle,i)
                new_point.x=rectangle.width+new_point.x

    def ffdh(self):
        self.deleteCanvas()
        self.rectangles.sort(key=lambda rectangle: rectangle.height,reverse=True)
        bands_point=[Point(0,0)]
        new_band_point=Point(0,self.rectangles[0].height)
        i=0
        for rectangle in self.rectangles:
            i+=1
            fit=False
            for band_point in bands_point:
                if rectangle.width+band_point.x<=self.cadre.width:
                    rectangle.set_point(band_point)
                    self.putRectangle(rectangle,i)
                    band_point.x=rectangle.width+band_point.x
                    fit=True
                    break
            
            if not fit:
                if new_band_point.y+rectangle.height>self.cadre.height:
                    continue
                bands_point.append(new_band_point)
                rectangle.set_point(bands_point[len(bands_point)-1])
                self.putRectangle(rectangle,i)
                bands_point[len(bands_point)-1].x=rectangle.width
                new_band_point=Point(0,rectangle.height+new_band_point.y)

            

    def putRectangle(self,rectangle:Rectangle,numero:int):
        position_x,position_y=self.cadre.point.x+rectangle.point.x,self.cadre.point.y+rectangle.point.y
        self.canvas.create_rectangle(position_x,position_y,position_x+rectangle.width,position_y+rectangle.height,fill="blue")
        center_x = position_x + rectangle.width / 2
        center_y = position_y + rectangle.height / 2
        self.canvas.create_text(center_x, center_y, text=str(numero), fill="white", font=("Arial", 12))