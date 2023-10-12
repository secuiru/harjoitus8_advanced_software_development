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
monkey_img= monkey_img.resize((20,20))
monkey_img = ImageTk.PhotoImage(monkey_img)

saari_img = Image.open("saari.png")
saari_img= saari_img.resize((180,180))
saari_img = ImageTk.PhotoImage(saari_img)

img2 = tk.PhotoImage()
meri=tk.Label(ikkuna,background="blue",image=img2,width=700,height=700)
meri.place(x=0,y=0)

saari=tk.Label(ikkuna,background="yellow",image=saari_img,borderwidth=0, highlightthickness=0)


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


def new_island():
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
                    #island_x-=180
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
            #saari=tk.Label(ikkuna,background="yellow",image=saari_img,borderwidth=0, highlightthickness=0)
            #saari.place(x=island_x,y=island_y)
            island_matrix[island_x,island_y]=1
            island_x+=1
            count+=1
            if count >140: 
                island_y+=1
                count=0
                island_x=ix
                #print("countissa")
            
            if island_y >= iy:
                ax1m.set_data(island_matrix)
                fig1.canvas.draw()
                fig1.canvas.flush_events()
                for i in range(10):
                    monkey = tk.Label(ikkuna,image=monkey_img)
                    island_x=100
                    island_y=100
                    monkey.place(x=island_x,y=island_y)
                n=1
    


def new_island_thread():
    t=threading.Thread(target=new_island)
    t.start()

def delete_island():
    global island_matrix
    for j in range(700):
     for i in range(700):
         island_matrix[j,i]=-10
    
    ax1m.set_data(island_matrix)
    fig1.canvas.draw()

def delete_island_thread():
    t=threading.Thread(target=delete_island)
    t.start()

add_island = tk.Button(ikkuna, text ="NEW ISLAND", command = new_island_thread)
add_island.place(x=50,y=50)

delete_island_button = tk.Button(ikkuna, text ="DELETE ISLAND", command = delete_island_thread)
delete_island_button.place(x=50,y=80)

#monkey = tk.Label(ikkuna,image=monkey_img)
#monkey.place(x=200,y=200)


ikkuna.mainloop()
