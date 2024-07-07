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
        self.rectangles_in_card=List[Rectangle]
        self.canvas = tk.Canvas(self.fenetre, width=width,height=height)

        # Ajouter un label en haut du canvas
        self.label_area_left = tk.Label(self.fenetre, text="Surface restant: ")
        self.label_area_left.pack(pady=10)

        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        #Listner
        btnNFDH = ttk.Button(self.canvas, text="NFDH", command= lambda : self.nfdb())
        btnNFDH.place(x=self.cadre.point.x  , y=self.cadre.point.y+self.cadre.height+10, anchor="n")

        btnFFDH = ttk.Button(self.canvas, text="FFDH", command= lambda : self.ffdh())
        btnFFDH.place(x=self.cadre.point.x+(width // 5), y=self.cadre.point.y+self.cadre.height+10, anchor="n")

        btnBF = ttk.Button(self.canvas, text="Best Fit", command= lambda :self.bf())
        btnBF.place(x=self.cadre.point.x+2*(width // 5), y=self.cadre.point.y+self.cadre.height+10, anchor="n")

    def get_area_left(self):
        area=self.get_area_used()
        return (self.cadre.height*self.cadre.width)-area
    
    def get_area_used(self):
        area=0
        for rectangle in self.rectangles_in_card:
            area+=rectangle.supeficie()
        return area
    
    def bf(self):
        self.deleteCanvas()
        free_rectangles=self.best_fit()
        self.label_area_left.config(text="Surface restant: "+str(self.get_area_left())+" Surface utilisé: "+str(self.get_area_used()))
        # print(len(free_rectangles))
        # self.put_free_space(free_rectangles)

    def get_rectangle_height(self,free_rectangle:Rectangle):
        free_rectangle.height=1
        free_rectangle.width=1
        break_height=False
        break_width=False
        while not break_height or not break_width:
            for rectangle in self.rectangles_in_card:
                if rectangle.contains_point(Point(free_rectangle.point.x+0.00001,free_rectangle.point.y+free_rectangle.height+0.000001)) and not break_height:
                    break_height=True
                    break
                if rectangle.contains_point(Point(free_rectangle.point.x+free_rectangle.width,free_rectangle.point.y+0.00001)) and not break_width:
                    break_width=True
                    break
            if not break_height:
                if 1+free_rectangle.point.y+free_rectangle.height<self.cadre.height:
                    free_rectangle.height+=1
                else:
                    break_height=True
            if not break_width:
                if 1+free_rectangle.point.x+free_rectangle.width<self.cadre.width:
                    free_rectangle.width+=1
                else:
                    break_width=True
            if break_width and break_height:
                break

        break_width=False

        while free_rectangle.point.x>0:
            
            free_rectangle.point.x-=1
            free_rectangle.width+=1
            for rectangle in self.rectangles_in_card:
                if rectangle.contains_point(Point(free_rectangle.point.x,free_rectangle.point.y)):
                    free_rectangle.point.x+=1
                    free_rectangle.width-=1
                    break_width=True
                    break

            if break_width:
                break

    def best_fit(self):
        free_rectangles=[Rectangle(self.cadre.width,self.cadre.height)]
        self.rectangles.sort(key=lambda rectangle: rectangle.height,reverse=True)
        num=1
        for rectangle in self.rectangles:
            index_rectangle_fit=-1
            min_space_left=float('inf')
            
            for i,free_rectangle in enumerate(free_rectangles):
                rectangle.set_point(free_rectangle.point)
                if free_rectangle.contains(rectangle):
                    space_left=free_rectangle.supeficie()-rectangle.supeficie()
                    if space_left<min_space_left:
                        index_rectangle_fit=i
                        min_space_left=space_left
            
            if index_rectangle_fit!=-1:
                rectangle.set_point(free_rectangles[index_rectangle_fit].point)
                new_free_rectangle=Rectangle(free_rectangles[index_rectangle_fit].width-rectangle.width,rectangle.height)
                new_free_rectangle.set_point(Point(rectangle.point.x+rectangle.width,rectangle.point.y))
                if rectangle.point.x+rectangle.width<self.cadre.width:
                    free_rectangles.append(new_free_rectangle)
                self.rectangles_in_card.append(rectangle)
                self.get_rectangle_height(new_free_rectangle)
                self.putRectangle(rectangle,num)
                free_rectangles[index_rectangle_fit].set_point(Point(rectangle.point.x,rectangle.point.y+rectangle.height))
                free_rectangles[index_rectangle_fit].height=free_rectangles[index_rectangle_fit].height-rectangle.height
                self.delete_free_space(free_rectangles)

            num+=1
        
        return free_rectangles

    def delete_free_space(self,free_rectangles):
        for rectangle in free_rectangles:
            self.get_rectangle_height(rectangle)

    
    def launch(self):
        self.bf()
        self.fenetre.mainloop()

    def deleteCanvas(self):
        self.rectangles_in_card=[]
        self.canvas.delete('all')
        position_x,position_y=self.cadre.point.x,self.cadre.point.y
        self.canvas.create_rectangle(position_x, position_y, self.cadre.width+position_x, self.cadre.height+position_y,width=5,outline="red",fill="black")


    def on_canvas_click(self,event):
        print(f"Clique à la position : ({event.x}, {event.y})")

    def nfdb(self):
        self.deleteCanvas()
        rectangles=sorted(self.rectangles, key=lambda rect: rect.height,reverse=True)
        band_height=rectangles[0].height
        new_point=Point(0,0)
        i=0
        for rectangle in rectangles:
            i+=1

            if rectangle.width+new_point.x<=self.cadre.width:
                rectangle.set_point(new_point)
                self.putRectangle(rectangle,i)
                self.rectangles_in_card.append(rectangle)
                new_point.x=rectangle.width+new_point.x

            else:
                if band_height+rectangle.height>self.cadre.height:
                    continue
                new_point.x=0
                new_point.y=band_height
                band_height+=rectangle.height
                rectangle.set_point(new_point)
                self.putRectangle(rectangle,i)
                self.rectangles_in_card.append(rectangle)
                new_point.x=rectangle.width+new_point.x
        self.label_area_left.config(text="Surface restant: "+str(self.get_area_left())+" Surface utilisé: "+str(self.get_area_used()))


    def ffdh(self):
        self.deleteCanvas()
        rectangles=sorted(self.rectangles, key=lambda rect: rect.height,reverse=True)
        bands_point=[Point(0,0)]
        new_band_point=Point(0,rectangles[0].height)
        i=0
        for rectangle in rectangles:
            i+=1
            fit=False
            for band_point in bands_point:
                if rectangle.width+band_point.x<=self.cadre.width:
                    rectangle.set_point(band_point)
                    self.putRectangle(rectangle,i)
                    self.rectangles_in_card.append(rectangle)
                    band_point.x=rectangle.width+band_point.x
                    fit=True
                    break
            
            if not fit:
                if new_band_point.y+rectangle.height>self.cadre.height:
                    continue
                bands_point.append(new_band_point)
                rectangle.set_point(bands_point[len(bands_point)-1])
                self.putRectangle(rectangle,i)
                self.rectangles_in_card.append(rectangle)
                bands_point[len(bands_point)-1].x=rectangle.width
                new_band_point=Point(0,rectangle.height+new_band_point.y)
        self.label_area_left.config(text="Surface restant: "+str(self.get_area_left())+" Surface utilisé: "+str(self.get_area_used()))

            

    def putRectangle(self,rectangle:Rectangle,numero:int):
        position_x,position_y=self.cadre.point.x+rectangle.point.x,self.cadre.point.y+rectangle.point.y
        self.canvas.create_rectangle(position_x,position_y,position_x+rectangle.width,position_y+rectangle.height,fill="blue")
        center_x = position_x + rectangle.width / 2
        center_y = position_y + rectangle.height / 2
        self.canvas.create_text(center_x, center_y, text=str(numero), fill="white", font=("Arial", 12))

    def put_free_space(self,free_rectangles:List[Rectangle]):
        for rectangle in free_rectangles:
            position_x,position_y=self.cadre.point.x+rectangle.point.x,self.cadre.point.y+rectangle.point.y
            self.canvas.create_rectangle(position_x,position_y,position_x+rectangle.width,position_y+rectangle.height,outline="yellow")