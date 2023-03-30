# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 16:38:08 2021

@author: Kekros,këina,jeremy

Premièrement l'organisation du labyrinth est sous la forme d'une matrice
donc la position de chaque sommet dans le laby est de forme [0,0] puis [0,1]
"""
import threading
import tkinter
import math
import time
import random
class graph_laby:
    
    def __init__(self,w,h):
        self.w = w
        self.h = h
        self.datas = {}
        self.mat = []
        self.generatelab(w, h)
    def linksbysucc(self,lst=[]):
        self.clearlinks()
        nlst=[]
        nlst = lst
        for y in range(self.h):
            
            for i in range(self.w):
                
                if len(nlst)!=0 and nlst[0]!= []:
                    
                    self.datas[self.mat[i][y]].links = [self.mat[z[0]-1][z[1]-1] for z in nlst[0]]
                    
                elif len(lst)==0:
                    return "done"
                nlst.remove(nlst[0])
    def clearlinks(self):
        """supprime les liens en doublons des sommets"""
        for i in self.datas.values():
            back = []
            for y in i.links:
                if not y in back:
                    back.append(y)
            i.links = back
                    
    def generatelab(self,w,h):
        """crée les sommets du labyrinth en fonction de sa taille"""
        val = 0
        for i in range(w):
            self.mat.append([])
            for y in range(h):
                val+=1
                self.datas[val] = somm(val,i,y)
                self.mat[i].append(val)
    def resetlinks(self):
        """reinitialise tout les liens entre les sommets du labyrinth"""
        for i in self.datas.values():
            i.links = []
    def allmark(self):
        """renvoi true si tout les sommets du labyrinth sont marqués"""
        l=0
        for i in self.datas.values():
            if i.mark:
                l+=1
        return (l== len(self.datas.values())-1)
    
    def isborderpoint(self,p):
         if (p[0] == self.w-1) or (p[1]==self.h-1) or (p[0]==0 or p[1]==0):
             return True
         else:
             return False
         
            
    def createways(self):
       self.startpoint = self.getrealpoint(randomvar(1, self.w-1,self.h-1))
       nbofjump = randomnbs(random.randint(int(self.w), int(self.w*3)),int(self.w*5),int(self.w*10))
       print("creating")
       co = 0
       self.endpoint = []
       self.tries=0
       while co !=1:
           self.tries+=1
           w = self.way(self.startpoint,self.startpoint,True,[])
           if dist(w[0],self.startpoint)>=(self.w)  and self.isborderpoint(w[0]):
               
               self.endpoint = w[0]
               self.realways = w[1]
               co=1
           else:
               self.startpoint = self.getrealpoint(randomvar(1, self.w-1,self.h-1))
               self.resetlinks()
               self.resetmarks()
       self.randresetmarks(0,2)
       for i in range(len(nbofjump)):
           c=0
           p=[]
           tries=0
           while c!=1:
               tries+=1
               p = [random.randint(0, self.w-1),random.randint(0, self.h-1)]
               if not self.datas[self.mat[p[0]][p[1]]].mark:
                   c=1
               elif self.allmark() or tries>self.w*self.h/2:
                   break
           self.randresetmarks(300,500)
           self.oways(p,p,nbofjump[i])
       self.clearlinks()
       self.resetmarks()
    def _isIn_(self,p):
        """renvoi True si le point est dans le labyrinth"""
        return (p[0]>=0 and p[1]>=0 and p[0]<=self.w-1 and p[1]<=self.h-1)
    def getposfromid(self,idds):
        return [[self.datas[i].x,self.datas[i].y] for i in idds ]
    def getaroundpoints(self,p):
        """renvoi tout les points autour d'un points"""
        arp = []
        l = [[1,0],[-1,0],[0,1],[0,-1]]
        for i in l:
            p2 = somme(p, i)
            if self._isIn_(p2):
                arp.append(p2)
        return arp
    
    def randresetmarks(self,mini,rate):
        """reinitialise des marques aléatoire"""
        for i in self.datas.values():
            co = random.randint(mini,rate)
            if co ==1:
                i.mark = False
        
    def resetmarks(self):
        """reinitialise les marques"""
        for i in self.datas.values():
            i.mark = False
        
    def oways(self,lastpos,pos,jumpsleft):
        """crée des chemin factices aléatoire"""
        self.datas[self.mat[pos[0]][pos[1]]].links.append(self.mat[lastpos[0]][lastpos[1]])
        self.datas[self.mat[lastpos[0]][lastpos[1]]].links.append(self.mat[pos[0]][pos[1]])
        if jumpsleft == 0:
            return None
        else:
            self.datas[self.mat[pos[0]][pos[1]]].mark = True
            w = randomvar2(1, 1,1)
            npos = [pos[0]+w[0],pos[1]+w[1]]
            tries = 0
            while npos==lastpos  or (npos[0] <0 or npos[1]<0) or (npos[0]>self.w-1 or npos[1]>self.h-1) or self.datas[self.mat[npos[0]][npos[1]]].mark:
                tries+=1;
                w = randomvar2(1, 1,1)
                npos = [pos[0]+w[0],pos[1]+w[1]]
                if tries ==100:
                    return None
                
            return self.oways(pos, npos, jumpsleft-1)
    def dispopt(self,p):
        return (len(self.datas[self.mat[p[0]][p[1]]].links)!=0)
    def way(self,pos,lastpos,first,ways):
        """crée un chemin aléatoire"""
        self.datas[self.mat[pos[0]][pos[1]]].links.append(self.mat[lastpos[0]][lastpos[1]])
        self.datas[self.mat[lastpos[0]][lastpos[1]]].links.append(self.mat[pos[0]][pos[1]])
        ways.append(pos)
        if (not first) and self.isborderpoint(pos) and dist(pos,self.startpoint)>=self.w:
            return pos,ways
        else:
            self.datas[self.mat[pos[0]][pos[1]]].mark = True
            lastpos = pos
            w = randomvar2(1, 1,1)
            npos = [pos[0]+w[0],pos[1]+w[1]]
            tries=0
            while npos==lastpos or (npos[0] <0 or npos[1]<0) or (npos[0]>self.w-1 or npos[1]>self.h-1) or self.datas[self.mat[npos[0]][npos[1]]].mark:
                w = randomvar2(1, 1,1)
                npos = [pos[0]+w[0],pos[1]+w[1]]
                tries+=1
                if tries==100:
                    return pos,ways
            return self.way(npos, lastpos,False,ways)
    
    def getrealpoint(self,p):
       """donne les vrais coordonnées d'un point"""
       if p[0] ==-1:
           return [self.w-1,p[1]]
       elif p[1]==-1:
           return [p[0],self.h-1]
       else:
           return p
        
def randomnbs(number,minimum,maximum):
    """renvoie une liste de sauts aléatoire"""
    nbs= []
    for i in range(number):  
        nbs.append(random.randint(minimum,maximum))
    return nbs    

def dist(p1,p2):
    """distance entre 2 points"""
    return math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)


def opposite(nb):
    """int between -1 and 0"""
    if nb == -1:
        return 0
    else:
        return -1
    
def occur(x, lst):
    """nb d'occurence dans une liste"""
    occurrence = 0
    for i in range(len(lst)):
        if x == lst[i]:
            occurrence += 1
    return occurrence    

def randomvar(occ,*args):
    """couple de variable aléatoire"""
    var =[]
    for i in args:
        if len(var) == 0 or  occur(-1,var)+occur(0,var)>=len(args)-occ :
            var.append(random.randint(-1,i))
        else:    
            var.append(random.randint(-1,0))
    return var 
  
def randomvar2(occ,*args):
    """couples de variables aléatoire"""
    var =[]
    for i in args:
        if len(var) == 0 or  occur(0,var)>=len(args)-occ :
            var.append(random.randint(-1,i))
        else:    
            var.append(0)
    return va

def ranged(nmber):
    """renvoi une variable entre -1 et 1"""
    rs = 1
    for i in range(nmber):
        if rs==1:
            rs-=2
        else:
            rs+=2
    return rs       

def createrandomiterator(maximum):
    """crée une liste d'itération"""
    tot = 0
    it = []
    while tot < maximum:
        cond =random.randint(0, 2)
        v1 = ranged(random.randint(1, 2))
        v2 = ranged(random.randint(1, 3))
        if cond==1:
            it.append((v1,v2))
            tot+=2
        elif cond==2:
            it.append((0,v2))
            tot+=1
        elif cond==3:
            it.append((v1,0))
            tot+=1
        else:
            it.append((0,0))
            tot+=0
    return it    
         
class somm:
    """classe sommet"""
    def __init__(self,idd,x,y):
        self.v=idd
        self.mark = False
        self.links= []
        self.x=x
        self.y=y
def getindice(lst,p):
    """recupère l'indice d'un element d'une liste"""
    for i in range(len(lst)):
        if lst[i]==p:
            return i
    return None    

def chemin(laby,entrée=None,sortie=None):
    """trouve une solution au labyrinth, de manière aveugle sur une base de backtracking"""
    pointmarqued= []
    ways = []
    def parcours(p,laby,back,sortie):
        acts = laby.datas[laby.mat[p[0]][p[1]]]
        acts.mark=True
        pointmarqued.append(p)
        if p == sortie:  
            ways.append(p)
            return True
        acts.links = randlist(acts.links)
        pos = laby.getposfromid(acts.links)
        if sortie in pos:
            rp = getindice(pos, sortie)
            po= parcours(pos[rp], laby, acts.v,sortie)
            ways.append(p)
            return po
        for i in acts.links:
            
            if i != back and not laby.datas[i].mark:
                po = parcours([laby.datas[i].x,laby.datas[i].y], laby, acts.v,sortie)
                if po:
                    ways.append(p)
                    return po
        return False   
    if entrée!=None and sortie==None:
        sortie = laby.endpoint
        return parcours(entrée,laby,laby.mat[entrée[0]][entrée[1]],laby.endpoint),ways,entrée,laby.endpoint,pointmarqued
    elif entrée!=None and sortie!=None:
        
        return parcours(entrée, laby, laby.mat[entrée[0]][entrée[1]], sortie),ways,entrée,sortie,pointmarqued
    elif entrée==None and sortie!=None: 
        entrée = laby.startpoint
        sortie = laby.endpoint
        return parcours(laby.startpoint, laby, laby.mat[laby.startpoint[0]][laby.startpoint[1]], sortie),ways,laby.startpoint,laby.endpoint,pointmarqued
    elif "endpoint" in laby.__dir__() and "startpoint" in laby.__dir__():
        return parcours(laby.startpoint, laby, laby.mat[laby.startpoint[0]][laby.startpoint[1]], laby.endpoint),ways,laby.startpoint,laby.endpoint,pointmarqued
        
    return parcours([0,0],laby,laby.mat[0][0],[laby.w-1,laby.h-1]),ways,[0,0],[laby.w-1,laby.h-1],pointmarqued

def somme(p1,p2):
    """somme de deux points"""
    return [p1[0]+p2[0],p1[1]+p2[1]]
def diff(p1,p2):
    """différence entre deux points"""
    return [p1[0]-p2[0],p1[1]-p2[1]]

def randlist(lst):
    """positionne aléatoirement les données d'une liste"""
    nlist = []
    while len(lst)>0:
        nlist.append(lst.pop(random.randint(0,len(lst)-1)))
    return nlist    

def copylst(lst):
    lst=[]




#le paramètre size permet de définir la taille du labyrinth 
size=[25,25]
#instanciation de la classe graph_laby

g =graph_laby(size[0],size[1])
g.createways()

#creation du labyrinth  2       3         4                             5           6              7                8          9             10                 11            12             13           14                           15          16         17    18         19       20         21            22                   23                   24      25     26          27       28           29          30          31       
#g.linksbysucc([[[1,2]],[],[[3,2],[4,1]],[[5,1],[4,2],[3,2],[3,1]],[[5,2],[4,1]],[[7,1],[6,2]],[[6,1],[8,1]],[[7,1],[8,2]],[[1,1],[2,2]],[[1,2],[3,2],[2,3]],[[2,2],[3,1]],[[4,1],[4,3]],[[5,1],[6,2]],[[5,2],[6,1],[7,2],[6,3]],[[6,2],[7,3]],[[8,1],[8,3]],[],[[2,4],[2,2]],[],[[4,2],[5,3]],[[4,3],[6,3]],[[5,3],[6,2],[7,3],[6,4]],[[6,3],[7,2],[7,4]],[[8,2],[8,4]],[],[[2,3],[3,4]],[[4,4],[2,4]],[[3,4]],[[6,4]],[[5,4],[6,3]],[[7,3],[8,4]],[[7,4],[8,3]]])
#recherche d'un chemin entre un point 1 et un point2
"""si un point est indisponible c'est parce que celui ci n'est conneté avec aucun autre sommet"""

#code pour afficher le labyrinth
#instanciation de la fenetre tkinter
root = tkinter.Tk()
root.geometry("1200x1000")
decal = 60
ca = tkinter.Canvas(root, width=size[0]*20+decal*2, height=size[1]*20+decal*2,bg="white")


for i in range(g.w):
    ca.create_text(i*10+decal+2,decal-5,text=str(i))
    

    
for i in range(g.h):
    ca.create_text(decal-5,i*10+decal+5,text=str(i))
for i in range(len(g.mat)):
    """premier dessin du labyrinth"""
    for y in range(len(g.mat[i])):
        p = [i,y]
        arp = g.getaroundpoints(p)
        ca.create_rectangle(i*10+decal,y*10+decal,i*10+10+decal,y*10+10+decal)
        for z in g.datas[g.mat[i][y]].links:
            ca.create_line(i*10+5+decal,y*10+5+decal,g.datas[z].x*10+5+decal,g.datas[z].y*10+5+decal,fill="white",width="9")
        if g.datas[g.mat[i][y]].links==[]:
            ca.create_rectangle(i*10+decal,y*10+decal,i*10+10+decal,y*10+10+decal,fill="black")
t =ca.create_text(int(size[0]*10/2),10,text="gardez un oeil sur la console :)")
ca.pack()
root.update()
root.update_idletasks()

#for i in range(len(g.realways)): 
    
#    if i-1>=0:
#        ca.create_line(g.realways[i-1][0]*10+5+decal,g.realways[i-1][1]*10+5+decal,g.realways[i][0]*10+5+decal,g.realways[i][1]*10+5+decal,fill="green",width="1m")
"""points initiaux de forme [x,y] avec p1 point de départ et p2 point d'arrivée
   
"""

p1=None
p2=None
usable = False
sol=None
sol = chemin(g)
while not usable:
    """choix des points de début et de fin si les choix initiaux sont indisponibles"""    
    root.update()
    root.update_idletasks() 
    if sol!=None:
        break
    elif  p1==None and p2 ==None or p1[0]>g.w-1 or p1[1]> g.h-1 or p2[0]>g.w-1 or p2[1]>g.h-1:
    
        root.update()
        root.update_idletasks()
        print("les points choisis ne sont pas dans le laby","\n","p entrée est dans le laby :",g._isIn_(p1),"\n","p sortie est dans le laby",g._isIn_(p2))
        P11 = int(input("abscisse du point d'entrée :"))
        P12 = int(input("ordonnée du point d'entrée :"))
        P21 = int(input("abscisse du point d'sortie :"))
        P22 = int(input("ordonnée du point d'sortie :"))
        print()
        print()
        p1= [P11,P12]
        p2= [P21,P22]
        
    elif p1==None and p2 ==None or g.dispopt(p1) and g.dispopt(p2):
        sol = chemin(g,p1,p2)
        usable = True
        root.update()
        root.update_idletasks()
    else:
        root.update()
        root.update_idletasks()
        print("les points choisis sont isolés","p1:",not g.dispopt(p1),"p2",not g.dispopt(p2))
        P11 = int(input("abscisse du point d'entrée :"))
        P12 = int(input("ordonnée du point d'entrée :"))
        P21 = int(input("abscisse du point d'sortie :"))
        P22 = int(input("ordonnée du point d'sortie :"))
        print()
        print()
        p1= [P11,P12]
        p2= [P21,P22]
ca.delete(t)

print("re clickez sur la fenetre du laby")

if not sol[0]:
    print("il n'y a pas de chemin entre le point",sol[2],sol[3])
    ca.create_text(int(size[0]*10+decal/2),int(size[1]*10+decal+20),text="il n'y pas de chemin")
for w in range(len(sol[-1])):
    """dessin de toutes les cases parcourus par l'algorithme"""
    ca.create_rectangle(sol[-1][w][0]*10+decal+1,sol[-1][w][1]*10+decal+1,sol[-1][w][0]*10+8+decal,sol[-1][w][1]*10+8+decal,fill="lightgrey",outline="lightgrey")
for i in range(len(sol[1])):
    """dessin du chemin trouvé parl'algorithme"""
    if i-1>=0 :
        ca.create_line(sol[1][i-1][0]*10+5+decal,sol[1][i-1][1]*10+5+decal,sol[1][i][0]*10+5+decal,sol[1][i][1]*10+5+decal,fill="blue",width="1m")        



"""actualisation de l'affichage"""

ca.create_rectangle(sol[3][0]*10+decal+1,sol[3][1]*10+decal+1,sol[3][0]*10+8+decal,sol[3][1]*10+8+decal,fill="red",outline="red")
ca.create_rectangle(sol[2][0]*10+decal+1,sol[2][1]*10+decal+1,sol[2][0]*10+8+decal,sol[2][1]*10+8+decal,fill="green",outline="green")
ca.create_text(100,20,text="le carré rouge est la case de sortie")
ca.create_text(100,30,text="le carré vert est la case d'entrée")
ca.create_text(150,10,text="le carré gris sont les case parcourus par l'algorithme")
ca.pack()

root.focus_force()
#affichage final du labyrinth
root.mainloop()   