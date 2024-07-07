from packing import Object1D
from packing import Packing1D

def main():
    objects_1d = [
        Object1D(3.5),
        Object1D(3.25)
    ]
    bac_size=5
    print("Best fit zao no ato")
    packing1d=Packing1D(bac_size,objects_1d)
    packing1d.brute_force()
    # for i in range(len(answer)):
    #     print(f"{i+1} eme bac")
    #     for obj in answer[i].objects:
    #         print(f"\t{obj.size}")
    #     print("------------------")
        

if __name__ == '__main__':
    main()
