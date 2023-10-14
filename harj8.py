import tkinter as tk
import winsound
import time
import threading 
from matplotlib.colors import ListedColormap
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import ImageTk, Image

ikkuna=tk.Tk()
ikkuna.title("Exercise 8")
ikkuna.geometry("700x700")


monkey_img = Image.open("apina2.png")
monkey_img= monkey_img.resize((20,20))
monkey_img = ImageTk.PhotoImage(monkey_img)

#saari_img = Image.open("saari.png")
#saari_img= saari_img.resize((180,180))
#saari_img = ImageTk.PhotoImage(saari_img)

img2 = tk.PhotoImage()
meri=tk.Label(ikkuna,background="blue",image=img2,width=700,height=700)
meri.place(x=0,y=0)

#saari=tk.Label(ikkuna,background="yellow",image=saari_img,borderwidth=0, highlightthickness=0)


global island_matrix
island_matrix=np.zeros((700,700))

for j in range(700):
     for i in range(700):
         island_matrix[j,i]=-10

fig1,ax1=plt.subplots(figsize=(9.1,9.1))
#fig1.subplots_adjust(0,0,1,1,0,0)
ax1m = ax1.matshow(island_matrix,cmap=ListedColormap(["blue", "gold","yellow"]),vmin=-17,vmax=10)
ax1.set_axis_off()
fig1.set_facecolor("yellow")
erikois_kanvas=FigureCanvasTkAgg(fig1,master=ikkuna)
erikois_kanvas.get_tk_widget().place(x=-117,y=-110)

erikois_kanvas.draw()
global monkeylist
monkeylist=[]
class Monkey_object:
  def __init__(self,monkey,island):
    self.monkey=monkey
    self.island = island

def new_island():
    global monkeylist
    n=0
    count=0
    island_x=random.randint(0,519)
    island_y=random.randint(0,559)
    ix=island_x
    iy=island_y+140
    area_empty=0
    exit_count=0
    while n==0:
            
        if area_empty==0:
            if island_matrix[island_x,island_y] == -10:
                island_x+=1
                count+=1
                if count >140: 
                    island_y+=1
                    count=0
                    island_x=ix
                if island_y > iy:
                    island_y-=140
                    area_empty=1

            else:
                island_x=random.randint(0,519)
                island_y=random.randint(0,559)
                ix=island_x
                iy=island_y+140
                exit_count+=1
                if exit_count > 3000:
                    print("tilaa ei löytynyt")
                    n=1
                #print("arvotaan uusi sijainti")

        if area_empty == 1:
            island_matrix[island_x,island_y]=1
            island_x+=1
            count+=1
            if count >140: 
                island_y+=1
                count=0
                island_x=ix
                print("x= ",island_x,"y= ",island_y)
            
            if island_y >= iy:
                ax1m.set_data(island_matrix)
                fig1.canvas.draw()
                fig1.canvas.flush_events()
                island_x=island_y-20
                island_y=ix
                for i in range(10):
                    m = Monkey_object(monkey = tk.Label(ikkuna,image=monkey_img),island=1)
                    island_x-=20
                    count+=1
                    monkeylist.append(m)
                    if count > 5:
                        island_x+=100
                        island_y+=40
                        count=0
                    
                    print("apina x= ",island_x,"y= ",island_y)
                    m.monkey.place(x=island_x,y=island_y)
                n=1
    

def new_island_thread():
    t=threading.Thread(target=new_island)
    t.start()

def monkey_checks():
    global monkeylist
    n=0
    global soundlist
    soundlist=[]
    while n==0:
        length = len(monkeylist)

        for i in range(length):
            if soundlist.__len__() <length:
                    soundlist.append(random.randint(200,1000))
            winsound.Beep(soundlist[i],50)

        for i in range(length):
            luckynumber=random.randint(0,10)
            if luckynumber==1:
                
                if monkeylist[i].island==1:
                    winsound.PlaySound("nauru.wav",winsound.SND_ASYNC)
                if monkeylist[i].island==0:
                    winsound.PlaySound("eat.wav",winsound.SND_ASYNC)
                monkeylist[i].monkey.destroy()
                monkeylist.pop(i)
                soundlist.pop(i)
        time.sleep(10)

def monkey_checks_thread():
    t=threading.Thread(target=monkey_checks)
    t.start()   

def monkey_swim():
    max=monkeylist.__len__()-1
    i=random.randint(0,max)
    monkeylist[i].island=0
    x=monkeylist[i].monkey.place_info().get("x")
    y=monkeylist[i].monkey.place_info().get("y")
    count=0
    x=int(x)
    y=int(y) 
    for j in range(18):
        count+=1
        if count < 10:
            x+=10
        if count >= 10:
            x-=10
        time.sleep(0.5)
        try:
            monkeylist[i].monkey.place(x=x,y=y)
        except:
            print("apina menehtyi merellä")
            break
            
    monkeylist[i].island=1
def monkey_swim_thread():
    t=threading.Thread(target=monkey_swim)
    t.start()       

def delete_island():
    global monkeylist
    global island_matrix
    global soundlist
    for j in range(700):
     for i in range(700):
         island_matrix[j,i]=-10
    
    length = len(monkeylist)
  
    for i in range(length):
        monkeylist[i].monkey.destroy()
        
    monkeylist.clear()    
    soundlist.clear()

    ax1m.set_data(island_matrix)
    fig1.canvas.draw()

def delete_island_thread():
    t=threading.Thread(target=delete_island)
    t.start()

add_island = tk.Button(ikkuna, text ="NEW ISLAND", command = new_island_thread)
add_island.place(x=50,y=50)

delete_island_button = tk.Button(ikkuna, text ="DELETE ISLAND", command = delete_island_thread)
delete_island_button.place(x=50,y=80)

delete_monkey_button = tk.Button(ikkuna, text ="DELETE MONKEY", command = monkey_checks_thread)
delete_monkey_button.place(x=120,y=80)

delete_monkey_button = tk.Button(ikkuna, text ="SWIM", command = monkey_swim_thread)
delete_monkey_button.place(x=120,y=50)

#monkey = tk.Label(ikkuna,image=monkey_img)
#monkey.place(x=200,y=200)
monkey_checks_thread()


ikkuna.mainloop()
