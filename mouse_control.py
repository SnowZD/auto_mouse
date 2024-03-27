import threading
import time
import tkinter
from tkinter import messagebox
from tkinter import filedialog
import pyautogui as pg
import pyautogui
import tkinter as tk
from tkinter import *
import tkinter.ttk as ttk
import tkinter.font as tkFont
from pynput import mouse
from pynput import keyboard

window = Tk()
window.title("ABC")
fontStyle = tkFont.Font(size=18)
fontStyle2 = tkFont.Font(size=14)

w = 730
h = 650
x = 300
y = 200
window.geometry('%dx%d+%d+%d' % (w, h, x, y))
window.resizable(False, False)

E1 = tk.Spinbox(window, from_=1, to=100, increment=1, width=5)
E1.place(x=460, y=35)

a1 = StringVar()
b1 = StringVar()
c1 = StringVar()
title = ('Axis', 'hex：RGB')

AN1 = Label(window, textvariable=a1, font=fontStyle)
AN1.place(x=180, y=25)
AN2 = Label(window, textvariable=c1, font=fontStyle)
AN2.place(x=15, y=25)

tree = ttk.Treeview(window, columns=title)
tree.place(x=150, y=90, height=550)

treescrollbar = Scrollbar(window)
treescrollbar.place(x=443, y=90, height=550)
tree.config(yscrollcommand=treescrollbar.set,)
treescrollbar.config(command=tree.yview)

style = ttk.Style()
style.configure('Treeview', rowheight=45)

tree.column('#0', width=0, stretch='no')
tree.column('Axis', anchor='center', width=150)
tree.column('hex：RGB', anchor='center', width=140)
tree.heading('Axis', text='Axis', anchor='center')
tree.heading('hex：RGB', text='hex：RGB', anchor='center')


def treeviewLdoubleclick(event):
    try:
        e = event.widget
        selectiid = e.identify('item', event.x, event.y)
        selectaxis = e.item(selectiid, 'values')[0]
        selectcolor = e.item(selectiid, 'values')[1]
        if comlistbox.get(comlistbox.size()-1) == 'If':
            addlistbox(selectaxis)
            isbutton.config(state=NORMAL)
        elif comlistbox.get(comlistbox.size()-1) == 'is':
            addlistbox(selectcolor)
            thenbutton.config(state=NORMAL)
        elif comlistbox.get(comlistbox.size()-1) == 'goto':
            addlistbox(selectaxis)
            clickbutton.config(state=NORMAL)
    except:
        time.sleep(0.000001)


# def treeviewRdoubleclick(event):
#     try:
#         e = event.widget
#         selectiid = e.identify('item', event.x, event.y)
#         selectcolor = e.item(selectiid, 'values')[1]
#         addlistbox(selectcolor)
#     except:
#         time.sleep(0.000001)


tree.bind('<Double-1>', treeviewLdoubleclick)
# tree.bind('<Double-3>', treeviewRdoubleclick)


def on_move(curx, cury):
    global rgb
    try:
        if c1.get() == 'Pause(F2)':
            a1.set('%d,%d' % (curx, cury))
            rgb = pg.screenshot().getpixel((curx, cury))
            if rgb[0]+rgb[1]+rgb[2] > 400:
                AN1.configure(fg='#000000')
            elif rgb[0]+rgb[1]+rgb[2] < 300:
                AN1.configure(fg='#ffffff')
            hexRGB = '#'+f'{rgb[0]:02x}'+f'{rgb[1]:02x}'+f'{rgb[2]:02x}'
            AN1.configure(bg=hexRGB)
        time.sleep(0.000001)
    except:
        # print('Over the screen.')
        time.sleep(0.000001)


def on_press(key):
    try:
        if key == keyboard.Key.f2:
            if c1.get() == 'Scan(F2)':
                c1.set('Pause(F2)')
                start_mouse_hook()
            elif c1.get() == 'Pause(F2)':
                c1.set('Scan(F2)')
                stop_mouse_hook(mouse_hook)
        if c1.get() == 'Pause(F2)':
            if key == keyboard.Key.f1:
                # print('press', key)
                hexRGB = '#'+f'{rgb[0]:02x}'+f'{rgb[1]:02x}'+f'{rgb[2]:02x}'
                tree.insert('', 'end', iid=len(tree.get_children()), tags=hexRGB,
                            values=(a1.get(), hexRGB))
                if rgb[0]+rgb[1]+rgb[2] > 400:
                    tree.tag_configure(hexRGB, background=hexRGB,
                                       font=fontStyle2, foreground='#000000')
                elif rgb[0]+rgb[1]+rgb[2] < 300:
                    tree.tag_configure(hexRGB, background=hexRGB,
                                       font=fontStyle2, foreground='#ffffff')
        if key == keyboard.Key.f3:
            Running('<1>')
        if key == keyboard.Key.esc:
            comlistbox.delete(0, "end")
            buttondisable()
            ifbutton.config(state=NORMAL)
    except:
        time.sleep(0.0000001)


def start_mouse_hook():
    global mouse_hook
    mouse_hook = mouse.Listener(on_move=on_move)
    mouse_hook.start()
    return mouse_hook

# Stop the mouse hook


def stop_mouse_hook(mouse_hook):
    mouse_hook.stop()


ketboard_hook = keyboard.Listener(on_press=on_press)
ketboard_hook.start()


c1.set('Scan(F2)')


def buttondisable():
    ifbutton.config(state=DISABLED)
    isbutton.config(state=DISABLED)
    thenbutton.config(state=DISABLED)
    gotobutton.config(state=DISABLED)
    clickbutton.config(state=DISABLED)


def addlistbox(com):
    # try:
    comlistbox.insert(tk.END, com)  # comlistbox.curselection()[0]+1
    buttondisable()
    if com == 'Then':
        gotobutton.config(state=NORMAL)
    elif com == 'click':
        ifbutton.config(state=NORMAL)
        # comlistbox.selection_set(comlistbox.curselection()[0]+1)
    # except:
    #     comlistbox.insert(0, com)
    #     comlistbox.selection_set(0)
    #     buttondisable()


def COM_start(event):
    global times
    times = 0
    while b1.get() == 'Stop(F3)':
        if times == int(E1.get()) and checkvalue.get() == False:
            b1.set('Run(F3)')
            return
        global checklist, actionlist
        checkaxis = []
        checkcolor = []
        actionlist = []
        send = 0
        i = 0
        while i < comlistbox.size():
            if comlistbox.get(i) == 'Then':
                send = 1
            elif send == 0:
                if comlistbox.get(i) == ('If' or 'or'):
                    checkaxis.append(comlistbox.get(i+1))
                elif comlistbox.get(i) == 'is':
                    checkcolor.append(comlistbox.get(i+1))
            elif send == 1:
                actionlist.append(comlistbox.get(i))
            i = i+1
        try:
            check(checkaxis, checkcolor, actionlist)
        except:
            b1.set('Run(F3)')
            messagebox.showinfo('Error', 'Fail')


def check(checkaxis, checkcolor, actioncom):
    acceptaction = 1
    i = 0
    try:
        while i < len(checkaxis):
            tarposi = checkaxis[i].split(',')
            rgb = pg.screenshot().getpixel((int(tarposi[0]), int(tarposi[1])))
            hexRGB = '#'+f'{rgb[0]:02x}'+f'{rgb[1]:02x}'+f'{rgb[2]:02x}'
            if hexRGB != checkcolor[i]:
                acceptaction = 0
            i = i+1
        if acceptaction == 1:
            mouseaction(actioncom)

    except:
        time.sleep(0.0000001)


def mouseaction(move):
    global times
    i = 0
    while i < len(move):
        if move[i] == 'goto':
            tarposi = move[i+1].split(',')
            pyautogui.moveTo((tarposi[0], tarposi[1]))
            if move[i+2] == 'click':
                pyautogui.click(clicks=1, button='left')
                if i+2 == len(move)-1:
                    times = times+1
        i = i+1


def Running(event):
    if b1.get() == 'Run(F3)':
        b1.set('Stop(F3)')
        COM = threading.Thread(target=COM_start, args=(event,))
        COM.start()
    elif b1.get() == 'Stop(F3)':
        b1.set('Run(F3)')


Runbutton = tk.Button(
    window, textvariable=b1,  width=7, font=fontStyle)
b1.set('Run(F3)')

Runbutton.bind("<1>", Running)
Runbutton.pack()

Runbutton.place(x=555, y=10)

comlistbox = tk.Listbox(window, font=fontStyle, selectmode=BROWSE)

comlistbox.place(x=470, y=90, height=550, width=220)
listscrollbar = Scrollbar(window)
listscrollbar.place(x=690, y=90, height=550)
comlistbox.config(yscrollcommand=listscrollbar.set)
listscrollbar.config(command=comlistbox.yview)


def listbox_Doubleclick(event):
    try:
        comlistbox.delete(comlistbox.curselection()[0])
        buttondisable()
        if comlistbox.get(comlistbox.size()-1) == 'Then':
            gotobutton.config(state=NORMAL)
        if comlistbox.get(comlistbox.size()-1) == ('click' or ''):
            ifbutton.config(state=NORMAL)
        if comlistbox.size() == 0:
            ifbutton.config(state=NORMAL)
    except:
        time.sleep(0.000001)


# def com_on_select(event):
#     buttondisable()
#     widget = event.widget
#     value = widget.get(widget.curselection()[0])
#     if value == 'Then':
#         gotobutton.config(state=NORMAL)
#     elif value == 'click':
#         ifbutton.config(state=NORMAL)


comlistbox.bind('<Double-1>', listbox_Doubleclick)
# comlistbox.bind('<<ListboxSelect>>', com_on_select)

ifbutton = tk.Button(
    window, text='If', command=lambda: addlistbox('If'), width=6, font=fontStyle)
isbutton = tk.Button(
    window, text='is', command=lambda: addlistbox('is'), width=6, font=fontStyle)
thenbutton = tk.Button(
    window, text='Then', command=lambda: addlistbox('Then'), width=6, font=fontStyle)
gotobutton = tk.Button(
    window, text='goto', command=lambda: addlistbox('goto'), width=6, font=fontStyle)
clickbutton = tk.Button(
    window, text='click', command=lambda: addlistbox('click'), width=6, font=fontStyle)
# elsebutton = tk.Button(
#     window, text='Else', command=lambda: addlistbox('Else'), width=6, font=fontStyle)
# andbutton = tk.Button(
#     window, text='and', command=lambda: addlistbox('and'), width=6, font=fontStyle)
# orbutton = tk.Button(
#     window, text='or', command=lambda: addlistbox('or'), width=6, font=fontStyle)
buttondisable()
ifbutton.config(state=NORMAL)

ifbutton.place(x=15, y=90)
isbutton.place(x=15, y=160)
thenbutton.place(x=15, y=230)
gotobutton.place(x=15, y=300)
clickbutton.place(x=15, y=370)
# elsebutton.place(x=15, y=510)
# andbutton.place(x=15, y=440)
# orbutton.place(x=15, y=580)


def input():
    inputfile = filedialog.askopenfilenames(title='Select the .txt file.',
                                            filetypes=(("txt Files", "*.txt"), ("All", "*.*")))
    try:
        with open(inputfile[0], 'r', encoding='utf-8') as f:
            n = f.read().split('\n')
            for i in n:
                comlistbox.insert(tk.END, i)
    except:
        messagebox.showinfo(
            'Error', 'Input fail. Please select the .txt file.')


def output():
    i = 0
    putputfile = filedialog.askdirectory(
        title='Select the folder to export.')
    try:
        with open(putputfile+'/save.txt', 'w', encoding='utf-8')as s:
            while i < comlistbox.size():
                s.write(comlistbox.get(i)+'\n')
                i = i+1
    except:
        messagebox.showinfo(
            'Error', 'Export fail. Please select the folder.')


inputbutton = tk.Button(
    window, text='input', command=input, width=6, font=fontStyle)
outputbutton = tk.Button(
    window, text='output', command=output, width=6, font=fontStyle)
inputbutton.place(x=15, y=500)
outputbutton.place(x=15, y=570)


def infcheck():
    if checkvalue.get() == True:
        E1.config(state=DISABLED)
    else:
        E1.config(state=NORMAL)


checkvalue = tk.BooleanVar()
chb = tkinter.Checkbutton(window, text='INFINITY',
                          command=infcheck, variable=checkvalue)
chb.place(x=355, y=30)


def QuitWindow():
    try:
        stop_mouse_hook(mouse_hook)
        ketboard_hook.stop()
        window.destroy()
    except:
        window.destroy()


window.protocol('WM_DELETE_WINDOW', QuitWindow)

window.mainloop()
