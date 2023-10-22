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


img2 = tk.PhotoImage()
meri=tk.Label(ikkuna,background="black",image=img2,width=700,height=700)
meri.place(x=0,y=0)

#saari=tk.Label(ikkuna,background="yellow",image=saari_img,borderwidth=0, highlightthickness=0)


global island_matrix
island_matrix=np.zeros((700,700))

for j in range(700):
     for i in range(700):
         island_matrix[j,i]=-10



fig1,ax1=plt.subplots(figsize=(9.1,9.1))

ax1m = ax1.matshow(island_matrix,cmap=ListedColormap(["blue", "gold","yellow"]),vmin=-17,vmax=10)
ax1.set_axis_off()
fig1.set_facecolor("blue")
erikois_kanvas=FigureCanvasTkAgg(fig1,master=ikkuna)
erikois_kanvas.get_tk_widget().place(x=-117,y=-110)
point_button=[]
points=0
for i in range(4):
    points+=5
    button_temp=tk.Button(ikkuna,text="Points: "+str(points),padx=40)
    button_temp.grid(row=0,column=i+1)
    point_button.append(button_temp)
def i_suppose_i_have_earned_so_much_points(amount_of_points):
    for i in range(4):
        point_button[i].configure(bg='gray')
       
    for i in range(amount_of_points):
        point_button[i].configure(bg='green')
        winsound.Beep(440+i*100,500)
i_suppose_i_have_earned_so_much_points(3)

erikois_kanvas.draw()
global monkeylist
monkeylist=[]
class Monkey_object:
  def __init__(self,monkey,island):
    self.monkey=monkey
    self.island = island
    self.alive = 1

global islandlist
islandlist=[]
class Island_object:
  def __init__(self,x,y,occupant_amount,travelling,name,island_location_list):
    self.x=x
    self.y = y
    self.name=name
    self.occupant_amount = occupant_amount
    self.travelling =travelling
    self.island_location_list =island_location_list

global island_number
island_number=1
def new_island():
    global monkeylist
    global islandlist
    n=0
    count=0
    island_x=random.randint(0,519)
    island_y=random.randint(0,559)
    ix=island_x
    iy=island_y+140
    area_empty=0
    exit_count=0

    island_location_list=[]
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
       

        if area_empty == 1:
            global island_number
            travelling=0
            if island_number==1:
                travelling=1
                
            
            island_matrix[island_x,island_y]=1
            island_location_list.append((island_x,island_y))

           
            island_x+=1
            count+=1
            if count >140: 
                island_y+=1
                count=0
                island_x=ix
              
            
            if island_y >= iy:
                ax1m.set_data(island_matrix)
                fig1.canvas.draw()
                fig1.canvas.flush_events()
                island_x=island_y-20
                island_y=ix
                print(island_number)
                name="S%d"%(island_number)
                occupant_amount=tk.StringVar(value=10)
                #occupant_amount=10
                island_number+=1
                island =Island_object(x=island_x,y=island_y,name=tk.Label(ikkuna,text=name,background="yellow"),travelling=travelling,occupant_amount=tk.Label(textvariable=occupant_amount,background="yellow"),island_location_list=island_location_list)
                islandlist.append(island)
                for i in range(10):
                    m = Monkey_object(monkey = tk.Label(ikkuna,image=monkey_img),island=1)
                    monkeylist.append(m)

                island_y+=40
                island_x-=80
                island.name.place(x=island_x,y=island_y)
                island_x+=40
                island.occupant_amount.place(x=island_x,y=island_y)
                n=1
    

def new_island_thread():
    t=threading.Thread(target=new_island)
    t.start()

def monkey_checks():
    global monkeylist
    n=0
    global soundlist
    soundlist=[]

    ####################################### apinoiden yksilölliset äänet
    while n==0:
        length = len(monkeylist)
        length-=1
        count=0
        for i in range(length):
            if monkeylist[i].alive==1:
                count+=1
        for i in range(count):
            if soundlist.__len__() <count:
                soundlist.append(random.randint(200,1000))
            if soundlist.__len__() >count:
                soundlist.pop()

        for i in range(count):
            winsound.Beep(soundlist[i],20)
    ###################################################### kuolema 
        for i in range(length):
            if monkeylist[i].alive==1:
                luckynumber=random.randint(0,100)
                if luckynumber==1:
                    monkeylist[i].alive=0
                    if monkeylist[i].island==1:
                        winsound.PlaySound("nauru.wav",winsound.SND_ASYNC)
                        k=0
                        i=0
                        length=islandlist.__len__() -1
                        while k==0:
                            i = random.randint(0,length)
 
                            value1 = islandlist[i].occupant_amount["textvariable"]
                            value2=islandlist[i].occupant_amount.getvar(value1)
                            value2= int(value2)
                            if value2 > 0:
                                value2-=1
                                value2 =str(value2)
                                ikkuna.setvar(name=value1, value=value2)
                                k=1

                    if monkeylist[i].island==0:
                        winsound.PlaySound("eat.wav",winsound.SND_ASYNC)
                        monkeylist[i].monkey.destroy()

        
    ############################################# lähetetään apinat uimaan saarilta jotka ovat tietoisia matkailusta
        length=islandlist.__len__()
        for i in range(length):
            if islandlist[i].travelling==2:
                monkey_swim_thread(i)

        time.sleep(10)    


def monkey_checks_thread():
    t=threading.Thread(target=monkey_checks)
    t.start()   

def travel_checks():
    global monkeylist
    n=0
    global islandlist
    ############################################## lisätään laiturit saarille jotka ovat tietoisia matkailusta
    while n==0:
        length=islandlist.__len__()
        for i in range(length):
            if islandlist[i].travelling==1:
                laituri_img = Image.open("laituri2.png")
                laituri_img= laituri_img.resize((20,20))
                img1=laituri_img
                img2=laituri_img.rotate(90)
                img3=laituri_img.rotate(180)
                img4=laituri_img.rotate(270)
                #pohjoinen laituri
                x=islandlist[i].x - 60
                y=islandlist[i].y - 22

                
                img1 = ImageTk.PhotoImage(img1)
                laituri = tk.Label(ikkuna,image=img1,background="grey")
                laituri.place(x=x,y=y)

                #länsi
                x=islandlist[i].x - 142
                y=islandlist[i].y + 50

                img2 = ImageTk.PhotoImage(img2)
                laituri2 = tk.Label(ikkuna,image=img2,background="grey")
                laituri2.place(x=x,y=y)

                #etelä
                x=islandlist[i].x - 60
                y=islandlist[i].y + 140

                img3 = ImageTk.PhotoImage(img3)
                laituri3 = tk.Label(ikkuna,image=img3,background="grey")
                laituri3.place(x=x,y=y)

                #itä
                x=islandlist[i].x +18
                y=islandlist[i].y + 50

                img4 = ImageTk.PhotoImage(img4)
                laituri4 = tk.Label(ikkuna,image=img4,background="grey")
                laituri4.place(x=x,y=y)
                islandlist[i].travelling=2

                monkey_swim_thread(i)
  
        time.sleep(1)    


def travel_checks_thread():
    t=threading.Thread(target=travel_checks)
    t.start()   

def monkey_swim(island_number):
    global monkeylist
    i=island_number
    n=0
    value1 = islandlist[island_number].occupant_amount["textvariable"]
    value2=islandlist[island_number].occupant_amount.getvar(value1)
    value2= int(value2)
    if value2 > 0:
        value2-=1
        value2 =str(value2)
        ikkuna.setvar(name=value1, value=value2)
    else:
        n=1
    print(value2)
    direction=random.randint(0,3)
    while n==0:
        #pohjoinen
        if direction ==0:
            x=islandlist[i].x - 60
            y=islandlist[i].y 
            m = Monkey_object(monkey = tk.Label(ikkuna,image=monkey_img),island=0)
            m.monkey.place(x=x,y=y)
            monkeylist.append(m)
            while n==0:
                if m.alive==1:
                    y-=1
                    m.monkey.place(x=x,y=y)
                    winsound.Beep(200,30)
                    
                    if island_matrix[y,x]==1:
                        print("saari löytyi")

                        length=islandlist.__len__()
                        for i in range(length):
                            length2=islandlist[i].island_location_list.__len__()
                            for j in range(length2):
                                if islandlist[i].island_location_list[j] == (y,x):
                                    print(islandlist[i].name["text"])
                                    value1 = islandlist[i].occupant_amount["textvariable"]
                                    value2=islandlist[i].occupant_amount.getvar(value1)
                                    value2= int(value2)
                                    value2+=1
                                    value2 =str(value2)
                                    ikkuna.setvar(name=value1, value=value2)
                                    islandlist[i].travelling=1
                                    m.monkey.destroy()
                                    m.island=1


                        n=1

                    time.sleep(0.1)
                else:
                    n=1

        #länsi
        if direction ==1:
            x=islandlist[i].x - 142
            y=islandlist[i].y + 50
            m = Monkey_object(monkey = tk.Label(ikkuna,image=monkey_img),island=0)
            m.monkey.place(x=x,y=y)
            monkeylist.append(m)
            while n==0:
                if m.alive==1:
                    x-=1
                    m.monkey.place(x=x,y=y)
                    
                    winsound.Beep(200,30)
                    
                    
                    if island_matrix[y,x]==1:
                        print("saari löytyi")

                        length=islandlist.__len__()
                        for i in range(length):
                            length2=islandlist[i].island_location_list.__len__()
                            for j in range(length2):
                                if islandlist[i].island_location_list[j] == (y,x):
                                    print(islandlist[i].name["text"])
                                    value1 = islandlist[i].occupant_amount["textvariable"]
                                    value2=islandlist[i].occupant_amount.getvar(value1)
                                    value2= int(value2)
                                    value2+=1
                                    value2 =str(value2)
                                    ikkuna.setvar(name=value1, value=value2)
                                    islandlist[i].travelling=1
                                    m.monkey.destroy()
                                    m.island=1


                        n=1

                    time.sleep(0.1)
                else:
                    n=1

        #etelä
        if direction ==2:
            x=islandlist[i].x - 60
            y=islandlist[i].y + 140
            m = Monkey_object(monkey = tk.Label(ikkuna,image=monkey_img),island=0)
            m.monkey.place(x=x,y=y)
            monkeylist.append(m)
            while n==0:
                
                
                
                try:
                    time.sleep(0.1)
                    y+=1
                    m.monkey.place(x=x,y=y)
                    winsound.Beep(200,30)
                    
                    if island_matrix[y,x]==1:
                        print("saari löytyi")

                        length=islandlist.__len__()
                        for i in range(length):
                            length2=islandlist[i].island_location_list.__len__()
                            for j in range(length2):
                                if islandlist[i].island_location_list[j] == (y,x):
                                    print(islandlist[i].name["text"])
                                    value1 = islandlist[i].occupant_amount["textvariable"]
                                    value2=islandlist[i].occupant_amount.getvar(value1)
                                    value2= int(value2)
                                    value2+=1
                                    value2 =str(value2)
                                    ikkuna.setvar(name=value1, value=value2)
                                    islandlist[i].travelling=1
                                    m.monkey.destroy()
                                    m.island=1
                        n=1
                
                except:
                    print("apina ajelehi avomerelle")
                    m.monkey.destroy()
                    n=1

                
        #itä
        if direction ==3:
            x=islandlist[i].x +18
            y=islandlist[i].y + 50
            m = Monkey_object(monkey = tk.Label(ikkuna,image=monkey_img),island=0)
            m.monkey.place(x=x,y=y)
            monkeylist.append(m)
            while n==0:
                x+=1
                m.monkey.place(x=x,y=y)
                winsound.Beep(200,30)
                
                if island_matrix[y,x]==1:
                    print("saari löytyi")

                    length=islandlist.__len__()
                    for i in range(length):
                        length2=islandlist[i].island_location_list.__len__()
                        for j in range(length2):
                            if islandlist[i].island_location_list[j] == (y,x):
                                print(islandlist[i].name["text"])
                                value1 = islandlist[i].occupant_amount["textvariable"]
                                value2=islandlist[i].occupant_amount.getvar(value1)
                                value2= int(value2)
                                value2+=1
                                value2 =str(value2)
                                ikkuna.setvar(name=value1, value=value2)
                                islandlist[i].travelling=1
                                m.monkey.destroy()
                                m.island=1
                    n=1
    
                time.sleep(0.1)
 
           
    
    
def monkey_swim_thread(island_number):
    t=threading.Thread(target=monkey_swim,args=(island_number,))
    t.start()       

def delete_island():
    global monkeylist
    global island_matrix
    global soundlist
    global islandlist
    global island_number
    island_number=1
    for j in range(700):
     for i in range(700):
         island_matrix[j,i]=-10
    
    length = len(monkeylist)
  
    for i in range(length):
        monkeylist[i].monkey.destroy()
        
    monkeylist.clear()    
    soundlist.clear()

    length = len(islandlist)
  
    for i in range(length):
        islandlist[i].name.destroy()
        
    islandlist.clear()    
    

    ax1m.set_data(island_matrix)
    fig1.canvas.draw()

def delete_island_thread():
    t=threading.Thread(target=delete_island)
    t.start()

def onnittelu():
    viesti = tk.Label(ikkuna,image="",text="Wau minä tein sen")
    viesti.place(x=350,y=350)
    i_suppose_i_have_earned_so_much_points(4)

add_island = tk.Button(ikkuna, text ="NEW ISLAND", command = new_island_thread)
add_island.place(x=50,y=50)

delete_island_button = tk.Button(ikkuna, text ="DELETE ISLAND", command = delete_island_thread)
delete_island_button.place(x=50,y=80)


delete_monkey_button = tk.Button(ikkuna, text ="SWIM", command = monkey_swim_thread)
delete_monkey_button.place(x=120,y=50)

delete_monkey_button = tk.Button(ikkuna, text ="onnittelu", command = onnittelu)
delete_monkey_button.place(x=120,y=80)


monkey_checks_thread()
travel_checks_thread()

ikkuna.mainloop()
