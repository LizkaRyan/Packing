from typing import List
from math import inf
import copy

class Object1D:
    def __init__(self, size: float):
        self.size = size


class Bac:
    def __init__(self, size: float):
        self.size = size
        self.objects = []

    def add_object(self, obj: Object1D) -> None:
        self.objects.append(obj)

    def objects_size(self) -> float:
        return sum(obj.size for obj in self.objects)
    
    def may_contain(self, obj: Object1D) -> bool:
        return self.objects_size() + obj.size <= self.size
    
    def space_left(self):
        return self.size - self.objects_size()
    
class Graphe:
    def __init__(self,bacs:List[Bac],enfant:List):
        self.enfants=enfant
        self.bacs=bacs

    def add_enfant(self,enfant):
        self.enfants.append(enfant)

    def add_bac(self,bac):
        self.bacs.append(bac)
    
    def add_object_in_bac(self,bac_index,object):
        self.bacs[bac_index].add_object(object)

class Packing1D:
    def __init__(self,bac_size:float,objects:List[Object1D]):
        max_obj_size=max(objects,key=lambda obj: obj.size).size
        if max_obj_size > bac_size:
            raise ValueError("Bac size cannot be greater than object size")
        self.bac_size=bac_size
        self.objects=objects

    def worst_fit_sort(self) -> List[Bac]:
        bac=Bac(self.bac_size)
        answer=[]
        self.objects.sort(key=lambda o: o.size)
        for obj in self.objects:
            if obj.size+bac.objects_size()<=self.bac_size:
                bac.add_object(obj)
            else:
                answer.append(bac)
                bac=Bac(self.bac_size)
                bac.add_object(obj)
        bac.add_object(obj)
        return answer
    
    def worst_fit(self) -> List[Bac]:
        answer=[Bac(self.bac_size)]
        for obj in self.objects:
            space=0
            bac_used=answer[0]
            fit=False
            for bac in answer:
                if self.bac_size-(obj.size+bac.objects_size())>=space:
                    bac_used=bac
                    space=self.bac_size-(obj.size+bac.objects_size())
                    fit=True
            if not fit:
                bac_used=Bac(self.bac_size)
                answer.append(bac_used)
            bac_used.add_object(obj)
        return answer
    
    def best_fit(self) -> List[Bac]:
        bacs = []
        for obj in self.objects:
            best_bac_index = -1
            best_bac_space_left = inf
            for bac_index in range(len(bacs)):
                bac = bacs[bac_index]
                bac_left_space = bac.space_left() - obj.size
                if bac.may_contain(obj) and bac_left_space < best_bac_space_left:
                    best_bac_index = bac_index
                    best_bac_space_left = bac_left_space
            if best_bac_index == -1:
                bacs.append(Bac(self.bac_size))
            bacs[best_bac_index].add_object(obj)

        return bacs
    
    def brute_force(self)->List[Bac]:
        bacs=[]
        for i in range(len(self.objects)):
            bacs.append(Bac(self.bac_size))
        graphe=Graphe(bacs,[])
        self.brute_force_bac(graphe,self.objects)
        answer=[]
        self.get_last_generation(graphe,answer)
        print(len(answer))
        #for graphes in answer:
            #self.print_bac(graphes.bacs)

    def brute_force_bac(self,graphe:Graphe,objects_1d:List[Object1D])->None:
        print(f"nb = {len(objects_1d)}")
        for e in range(len(objects_1d)):
            for i in range(len(graphe.bacs)):
                if objects_1d[e].size+graphe.bacs[i].objects_size()<=self.bac_size:
                    graphe_copied=copy.deepcopy(graphe)
                    objects_1d_copy=copy.deepcopy(objects_1d)
                    graphe_copied.add_object_in_bac(i,objects_1d[e])
                    objects_1d_copy.pop(e)
                    print(f"\t {e}={objects_1d[e].size}")
                    print("\t\tHere we go again ")
                    if len(objects_1d_copy)!=0:
                        self.brute_force_bac(graphe_copied,objects_1d_copy)
                    graphe.add_enfant(graphe_copied)
        print("----------------")

    def get_last_generation(self,graphe:Graphe,answer:List[Graphe])->None:
        if len(graphe.enfants)!=0:
            for enfant in graphe.enfants:
                self.get_last_generation(enfant,answer)
        else:
            answer.append(graphe)

    def print_bac(self,bacs:List[Bac]):
        for i in range(len(bacs)):
            print(f"{i+1} eme bac")
            for obj in bacs[i].objects:
                print(f"\t{obj.size}")
            print("------------------")