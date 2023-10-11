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


monkey_img = Image.open("apina.png")
monkey_img= monkey_img.resize((40,40))
monkey_img = ImageTk.PhotoImage(monkey_img)

saari_img = Image.open("saari.png")
saari_img= saari_img.resize((180,180))
saari_img = ImageTk.PhotoImage(saari_img)

img2 = tk.PhotoImage()
meri=tk.Label(ikkuna,background="blue",image=img2,width=700,height=700)
meri.place(x=0,y=0)

saari=tk.Label(ikkuna,background="yellow",image=saari_img,borderwidth=0, highlightthickness=0)


ernestin_oja=np.zeros((700,700))

for j in range(700):
     for i in range(700):
         ernestin_oja[j,i]=-10

fig1,ax1=plt.subplots(figsize=(9.1,9.1))
#fig1.subplots_adjust(0,0,1,1,0,0)
ax1m = ax1.matshow(ernestin_oja,cmap=ListedColormap(["blue", "gold","yellow"]),vmin=-17,vmax=10)
ax1.set_axis_off()
fig1.set_facecolor("yellow")
erikois_kanvas=FigureCanvasTkAgg(fig1,master=ikkuna)
erikois_kanvas.get_tk_widget().place(x=-117,y=-110)

erikois_kanvas.draw()


def new_island():
    n=0
    i=150
    j=150
    count=0
    island_x=random.randint(0,519)
    island_y=random.randint(0,519)
    ix=island_x
    iy=island_y+180
    area_empty=0
    while n==0:
            
        if area_empty==0:
            if ernestin_oja[island_x,island_y] == -10:
                island_x+=1
                count+=1
                if count >180: 
                    island_y+=1
                    count=0
                    island_x=ix
                if island_y > iy:
                    island_x-=180
                    island_y-=180
                    area_empty=1

            else:
                island_x=random.randint(0,519)
                island_y=random.randint(0,519)
                ix=island_x
                iy=island_y+180
                print("arvotaan uusi sijainti")

        if area_empty == 1:
            #saari=tk.Label(ikkuna,background="yellow",image=saari_img,borderwidth=0, highlightthickness=0)
            #saari.place(x=island_x,y=island_y)
            ernestin_oja[island_x,island_y]=1
            island_x+=1
            count+=1
            if count >180: 
                island_y+=1
                count=0
                island_x=ix
                print("countissa")
            
            if island_y > iy:
                ax1m.set_data(ernestin_oja)
                fig1.canvas.draw()
                fig1.canvas.flush_events()
                n=1

def new_island_thread():
    t=threading.Thread(target=new_island)
    t.start()

add_island = tk.Button(ikkuna, text ="NEW ISLAND", command = new_island_thread)
add_island.place(x=50,y=50)

ikkuna.mainloop()
