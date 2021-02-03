import cv2
import numpy as np
import math
import time
import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter.ttk import Combobox
from tkinter.ttk import Progressbar
from tkinter import ttk
from PIL import Image
from PIL import ImageTk

def I_found(img, M, R, x, y):
    height, width = img.shape[:2]
    mass = 0
    for i in range(0, width):
        for j in range(0, height):
            mass += img[i][j]
    m0 = M/mass
    r0 = (2*R)/width
    I = 0
    mi = 0
    ri = 0
    for i in range(0, width):
        for j in range(0, height):
            mi = m0*img[i][j]
            xi = r0*(math.fabs(x - i))
            yi = r0*(math.fabs(y - j))
            ri = xi**2 + yi**2

            I += mi*ri
    return I

def clicked_help():
     messagebox.showinfo('справка', 'инструкция')

root = Tk()
root.geometry('800x600')
root.title("Нахождение момента инерции произвольного плоского тела. Преин 10-2")
root.resizable(width=False, height=False)

def clicked1():
    global c2, c1, image_obj,image_obj0, image_obj_1, image_obj_2, image_1, image_2, width, height

    way2img = filedialog.askopenfilename()
    if way2img != '':
        #try:
            image_obj0 = Image.open(way2img)

            image_obj = image_obj0.resize((220, 220), Image.ANTIALIAS)

            image_obj_1 = ImageTk.PhotoImage(image_obj)
            image_1 = c1.create_image(110,110, image=image_obj_1)

            image_obj_2 = image_obj.convert('L')
            image_obj_2 = ImageTk.PhotoImage(image_obj_2)
            image_2 = c2.create_image(110,110, image=image_obj_2)

            (width, height) = image_obj0.size
        #except:
            #messagebox.showinfo('ошибка', 'некорректный файл\nнеподдерживаемое\nрасширение файла')

#lbl = Label(root, text="Путь к файлу:", font = 32)
#lbl.place(x = 32, y = 0, height = 32)

#txt = Entry(root, font = 32)
#txt.place(x = 32, y = 32, height = 32, width = 440-32)

image_ent = ImageTk.PhotoImage(file = r"C:\Users\Дмитрий\Documents\ent.png")
btn = Button(root, text="Открыть файл", command = clicked1, font = 32)
btn.place(x = 32, y = 32, height = 32)

lbl1 = Label(root, text="Исходное изображение:", font = 32)
lbl1.place(x = 32, y = 64, height = 32)
c1=Canvas(root, width=220, height=220, bg = 'white')
c1.place(x = 32, y = 32*3)

lbl2 = Label(root, text="Рабочее изображение:", font = 32)  
lbl2.place(x = 32, y = 98+220, height = 32)
c2=Canvas(root, width=220, height=220, bg='white')
c2.place(x = 32, y = 32*4+220)

btn_help = Button(root, text="справка", command = clicked_help, font = 32)
btn_help.place(y = 32, height = 32, width = 96, x = 800-32-96)

uniformity = BooleanVar()  
uniformity.set(False)  
uniformity_btn = Checkbutton(root, text='Однородность', var=uniformity, font = 32)  
uniformity_btn.place(height = 32, y = 64+30, relx = 1, x = -32, anchor = NE)

Mass_lbl = Label(root, text="Масса(кг):", font = 32)  
Mass_lbl.place(y = 96+32, x = 800-32-96 -96 )
Mass_btn = Spinbox(from_=0, increment = 0.000001, to = 1989*10**27, font = 32)
Mass_btn.place(x = 800-32-96, y = 96+30, height = 32, width = 96)

ratio = BooleanVar()  
ratio.set(True)

Y_lbl = Label(root, text="Y:", font = 32)  
Y_btn = Spinbox(from_=0, increment = 0.001, to = 1989*10**27, font = 32)
if ratio.get() == False:
    Y_btn.place(width = 96, height = 32, y = 32*6+60, relx = 1, x = -160, anchor = NE)
    Y_lbl.place(width = 96, height = 32, y = 32*6+60, relx = 1, x = -160-96, anchor = NE)

def ratio_func():
    if ratio.get() == False:
         Y_btn.place(width = 96, height = 32, y = 32*6+60, relx = 1, x = -160, anchor = NE)
         Y_lbl.place( height = 32, y = 32*6+60, relx = 1, x = -160-96, anchor = NE)
        
    else:
        Y_lbl.place_forget()
        Y_btn.place_forget()

lbl_1 = Label(root, text="Размеры по осям(м):", font = 32)  
lbl_1.place(y = 32*4+60, relx = 1, x = -32, anchor = NE, height = 32)

ratio_btn = Checkbutton(root, text='сохраниить соотношение сторон', var=ratio, command = ratio_func, font = 32)
ratio_btn.place(y = 32*5+60, relx = 1, x = -32, anchor = NE)

X_lbl = Label(root, text="X:", font = 32)  
X_lbl.place(y = 32*6+60, relx = 1, x = -32-96, anchor = NE, height = 32)
X_btn = Spinbox(from_=0, increment = 0.001, to = 1989*10**27, font = 32)
X_btn.place(width = 96, height = 32, y = 32*6+60, relx = 1, x = -32, anchor = NE)

O_lbl = Label(root, text="Координаты оси вращения:", font = 32)
O_lbl.place(height = 32,  y = 32*7+90, relx = 1, x = -32-96-32, anchor = NE)
combo = Combobox(root, font = 32)  
combo['values'] = ('метры', 'пиксели')  
combo.current(1) 
combo.place(height = 32, width = 96, y = 32*7+90, relx = 1, x = -32-32, anchor = NE)

X0 = IntVar()
X0.set(0)
X0_lbl = Label(root, text="X0:", font = 32)  
X0_lbl.place(height = 32, y = 32*8+90, relx = 1, x = -32-96, anchor = NE)
X0_btn = Spinbox(from_=0, increment = 1, to = 1989*10**27, font = 32, textvariable =X0)
X0_btn.place(height = 32, width = 96, y = 32*8+90, relx = 1, x = -32, anchor = NE)

Y0 = IntVar()
Y0.set(0)
Y0_lbl = Label(root, text="Y0:", font = 32)  
Y0_lbl.place(height = 32, y = 32*8+90, relx = 1, x = -160-96, anchor = NE)
Y0_btn = Spinbox(from_=0, increment = 1, to = 1989*10**27, font = 32,textvariable =Y0)
Y0_btn.place(height = 32, width = 96, y = 32*8+90, relx = 1, x = -160, anchor = NE)

def combo_func():
    global X0_lbl
    global X0_btn
    global Y0_lbl
    global Y0_btn
    
    if X0_btn['increment'] == 1 and combo.get() == 'метры':
        
        X0_lbl.place_forget()
        X0_lbl = Label(root, text="X0:", font = 32)  
        X0_lbl.place(height = 32, y = 32*8+90, relx = 1, x = -32-96, anchor = NE)
        X0_btn.place_forget()
        X0_btn = Spinbox(from_=0, increment = 0.001, to = 1989*10**27, font = 32)
        X0_btn.place(height = 32, width = 96, y = 32*8+90, relx = 1, x = -32, anchor = NE)

        Y0_lbl.place_forget()
        Y0_lbl = Label(root, text="Y0:", font = 32)  
        Y0_lbl.place(height = 32, y = 32*8+90, relx = 1, x = -160-96, anchor = NE)
        Y0_btn.place_forget()
        Y0_btn = Spinbox(from_=0, increment = 0.001, to = 1989*10**27, font = 32)
        Y0_btn.place(height = 32, width = 96, y = 32*8+90, relx = 1, x = -160, anchor = NE)

    elif X0_btn['increment'] == 0.001 and combo.get() == 'пиксели':
        
        X0_lbl.place_forget()
        X0_lbl = Label(root, text="X0:", font = 32)  
        X0_lbl.place(height = 32, y = 32*8+90, relx = 1, x = -32-96, anchor = NE)
        X0_btn.place_forget()
        X0_btn = Spinbox(from_=0, increment = 1, to = 1989*10**27, font = 32)
        X0_btn.place(height = 32, width = 96, y = 32*8+90, relx = 1, x = -32, anchor = NE)

        Y0_lbl.place_forget()
        Y0_lbl = Label(root, text="Y0:", font = 32)  
        Y0_lbl.place(height = 32, y = 32*8+90, relx = 1, x = -160-96, anchor = NE)
        Y0_btn.place_forget()
        Y0_btn = Spinbox(from_=0, increment = 1, to = 1989*10**27, font = 32)
        Y0_btn.place(height = 32, width = 96, y = 32*8+90, relx = 1, x = -160, anchor = NE)

O_btn = Button(root, text="     ", command = combo_func, image = image_ent)
O_btn.place(y = 32*7+90,height = 32, width = 32, relx = 1, x = -32, anchor = NE)

def f7():
    Y0.set(0)
    X0.set(0)
image7 = ImageTk.PhotoImage(file = r"C:\Users\Дмитрий\Documents\7.png" )
btn7 = Button(root,image = image7, text="     ", command = f7)
btn7.place(height = 32, width = 32, x=800-96-32, y=536-64-32-32)

def f8():
    Y0.set(0)
    if X0_btn['increment'] == 1:
        X0.set(str(X_btn.get())/2)
    else:
        X0.set(width/2)
image8 = ImageTk.PhotoImage(file = r"C:\Users\Дмитрий\Documents\8.png" )
btn8 = Button(root,image = image8, text="     ", command = f8)
btn8.place(height = 32, width = 32, x=800-96, y=536-64-32-32)

image9 = ImageTk.PhotoImage(file = r"C:\Users\Дмитрий\Documents\9.png" )
btn9 = Button(root,image = image9, text="     ")
btn9.place(height = 32, width = 32, x=800-96+32, y=536-64-32-32)

image4 = ImageTk.PhotoImage(file = r"C:\Users\Дмитрий\Documents\4.png" )
btn4 = Button(root,image = image4, text="     ")
btn4.place(height = 32, width = 32, x=800-96-32, y=536-64-32)

image5 = ImageTk.PhotoImage(file = r"C:\Users\Дмитрий\Documents\5.png" )
btn5 = Button(root,image = image5, text="     ")
btn5.place(height = 32, width = 32, x=800-96, y=536-64-32)

image6 = ImageTk.PhotoImage(file = r"C:\Users\Дмитрий\Documents\6.png" )
btn6 = Button(root,image = image6, text="     ")
btn6.place(height = 32, width = 32, x=800-96+32, y=536-64-32)

image1 = ImageTk.PhotoImage(file = r"C:\Users\Дмитрий\Documents\1.png" )
btn1 = Button(root, image = image1, text="     ")
btn1.place(height = 32, width = 32, x=800-96-32, y=536-32-32)

image2 = ImageTk.PhotoImage(file = r"C:\Users\Дмитрий\Documents\2.png" )
btn2 = Button(root,image = image2, text="     ")
btn2.place(height = 32, width = 32, x=800-96, y=536-32-32)

image3 = ImageTk.PhotoImage(file = r"C:\Users\Дмитрий\Documents\3.png" )
btn3 = Button(root,image = image3, text="     ")
btn3.place(height = 32, width = 32, x=800-96+32, y=536-32-32)

btn_str = Button(root, text="СТАРТ", font = 32)
btn_str.place(height = 32, width = 96, x=800-96-32, y = 536)

pb = ttk.Progressbar(root, value = 70)
pb.place(x = 284, y = 600-64-64,  height = 32, width = 356)

ans = Text(root, font = 32, state='disabled')
ans.place(x = 284, y = 600-64, height = 32, width = 356)

"""
way2img = r'E:/8-point-star.jpg'
image = cv2.imdecode(np.fromfile(way2img, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
notgray = cv2.bitwise_not(gray)
height, width = notgray.shape[:2]


centre = True
if centre:
    y = height/2 
    x = width/2
    
M = 1
mass = 0
for i in range(0, width):
    for j in range(0, height):
        mass += notgray[i][j]
m0 = M/mass

R = 1
r0 = (2*R)/width

I = 0
mi = 0
ri = 0
bar = IncrementalBar('Countdown', max = height*width)
for i in range(0, width):
    for j in range(0, height):
        mi = m0*notgray[i][j]
        xi = r0*(math.fabs(x - i))
        yi = r0*(math.fabs(y - j))
        ri = xi**2 + yi**2

        I += mi*ri
        bar.next()
bar.finish()

cv2.imshow('1', notgray)
cv2.waitKey(0)
cv2.destroyAllWindows()
"""

root.mainloop()