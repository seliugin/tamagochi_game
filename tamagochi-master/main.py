# -*- coding: utf-8 -*-
import tkinter
import os
from tkinter import messagebox as mb

try:
    f = open("save.txt", 'x')
    hunger = 100
    year = 0
    energy = 100
    happy = 100
    result = 0

except FileExistsError:
    f = open("save.txt")
    args = f.readlines()
    hunger = int(args[0])
    year = int(args[1])
    energy = int(args[2])
    happy = int(args[3])
    result = str(args[4])

f.close()

pressforstart = True
feedflag = 0
playflag = 0
sleepflag = 0
deathflag = 0


class CustomDialog(object):
    def __init__(self, parent, prompt="", default=""):
        self.popup = tkinter.Toplevel(parent)
        self.popup.title(prompt)
        self.popup.transient(parent)

        self.var = tkinter.StringVar(value=default)

        label = tkinter.Label(self.popup, text=prompt)
        entry = tkinter.Entry(self.popup, textvariable=self.var)
        buttons = tkinter.Frame(self.popup)

        buttons.pack(side="bottom", fill="x")
        label.pack(side="top", fill="x", padx=20, pady=10)
        entry.pack(side="top", fill="x", padx=20, pady=10)

        ok = tkinter.Button(buttons, text="Ok",
                            command=self.popup.destroy)
        ok.pack(side="top")

        self.entry = entry

    def show(self):
        self.entry.focus_force()
        root.wait_window(self.popup)
        return self.var.get()


def cancel():
    answer = mb.askyesno(title="Начать сначала",
                         message="Ты уверен, что хочешь начать сначала?")
    if answer is True:
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                            'save.txt')
        os.remove(path)
        exit()


def exitgame():
    answer = mb.askyesno(title="Выход из игры",
                         message="Ты меня покидаешь?(")
    if answer is True:
        root.quit()


def info():
    file = open('info.txt', encoding="utf8")
    mb.showinfo("О программе", file.read())


def help():
    file = open('help.txt', encoding="utf8")
    mb.showinfo("Помощь", file.read())


def start_game(start):
    global pressforstart

    if pressforstart is False:
        pass

    else:
        startLabel.config(text="")
        update_hunger()
        update_year()
        update_energy()
        update_happy()
        update_display()

        pressforstart = False


def update_display():
    global year
    global hunger
    global feedflag
    global playflag
    global sleepflag

    if deathflag == 1:
        Picture.config(image=death)
        Picture.after(100, update_display)

    elif feedflag == 1:
        Picture.config(image=iameating)
    elif playflag == 1:
        Picture.config(image=iamplaying)
    elif sleepflag == 1:
        Picture.config(image=iamsleeping)
    else:
        if hunger >= 80 and energy >= 70 and happy >= 70:
            Picture.config(image=happyphoto)
        elif hunger < 50 and energy < 50 and happy < 50:
            Picture.config(image=iamill)
        elif hunger >= 50 and energy >= 50 and happy >= 50:
            Picture.config(image=normalphoto)
        elif hunger < 50:
            Picture.config(image=iwanttoeat)
        elif energy < 50:
            Picture.config(image=iwanttosleep)
        elif happy < 50:
            Picture.config(image=sad)

    hungerLabel.config(text="Я сыт на " + str(hunger) + " %")
    yearLabel.config(text="Мне уже " + str(year) + year_end())
    energyLabel.config(text="Бодрость: " + str(energy) + " %")
    happyLabel.config(text="Счастье: " + str(happy) + " %")

    if feedflag == 1:
        Picture.after(1000, update_display)
        feedflag = 0
    elif playflag == 1:
        Picture.after(1000, update_display)
        playflag = 0
    elif sleepflag == 1:
        Picture.after(2500, update_display)
        sleepflag = 0
    else:
        Picture.after(300, update_display)


def update_hunger():

    global hunger

    if hunger > 0:
        hunger -= 1

    if is_alive():
        hungerLabel.after(1000, update_hunger)


def update_year():

    global year
    year += 1

    if is_alive():
        yearLabel.after(80000, update_year)


def update_energy():

    global energy

    if energy > 0:
        energy -= 1

    if is_alive():
        energyLabel.after(2000, update_energy)


def update_happy():

    global happy

    if happy > 0:
        happy -= 1

    if is_alive():
        happyLabel.after(1000, update_happy)


def feed():
    global hunger
    global feedflag

    feedflag = 1

    if is_alive():
        global hunger
        if hunger <= 93:
            hunger += 7


def sleep():
    global energy
    global sleepflag

    if is_alive():
        if energy <= 80:
            energy += 20

    sleepflag = 1


def play():
    global happy
    global playflag

    if is_alive():
        if happy <= 90:
            happy += 10

    playflag = 1


def is_alive():
    global hunger
    global deathflag

    if hunger <= 0:
        deathflag = 1
        startLabel.config(text=(str(result).title()) + " погиб...")
        return False
    else:
        return True


def year_end():
    global year

    if str(year)[len(str(year)) - 1] == '1':
        return " год!"
    if ord(str(year)[len(str(year)) - 1]) in range(ord('2'), ord('5')):
        return " года!"
    else:
        return " лет!"


root = tkinter.Tk()
root.title("Заечка")
root.geometry("800x800")

startLabel = tkinter.Label(root, text="Нажмите enter;)",
                           font=('Times New Roman', 20))
startLabel.pack()

hungerLabel = tkinter.Label(root, text="Я сыт на "
                                       + str(hunger) + " %",
                            font=('Times New Roman', 25))
hungerLabel.pack()

yearLabel = tkinter.Label(root, text="Мне уже "
                                     + str(year) + year_end(),
                          font=('Times New Roman', 25))
yearLabel.pack()

energyLabel = tkinter.Label(root, text="Бодрость: "
                                       + str(energy) + " %",
                            font=('Times New Roman', 25))
energyLabel.pack()

happyLabel = tkinter.Label(root, text="Счастье: "
                                      + str(happy) + " %",
                           font=('Times New Roman', 25))
happyLabel.pack()

happyphoto = tkinter.PhotoImage(file="happy.gif")
normalphoto = tkinter.PhotoImage(file="normal.gif")
iamill = tkinter.PhotoImage(file="iamill.gif")
sad = tkinter.PhotoImage(file="sad.gif")
iwanttoeat = tkinter.PhotoImage(file="iwanttoeat.gif")
iwanttosleep = tkinter.PhotoImage(file="iwanttosleep.gif")
iameating = tkinter.PhotoImage(file="iameating.gif")
iamplaying = tkinter.PhotoImage(file="iamplaying.gif")
iamsleeping = tkinter.PhotoImage(file="iamsleeping.gif")
death = tkinter.PhotoImage(file="death.gif")

Picture = tkinter.Label(root, image=normalphoto)
Picture.pack()

btnFeed = tkinter.Button(root, text="Покорми меня!", command=feed,
                         font=('Times New Roman', 20))
btnFeed.place(x=10, y=250)

btnSleep = tkinter.Button(root, text="Уложи меня спать!",
                          command=sleep, font=('Times New Roman', 20))
btnSleep.place(x=10, y=350)

btnPlay = tkinter.Button(root, text="Поиграй со мной!",
                         command=play, font=('Times New Roman', 20))
btnPlay.place(x=10, y=450)

mainmenu = tkinter.Menu(root)
root.config(menu=mainmenu)

filemenu = tkinter.Menu(mainmenu, tearoff=0)
filemenu.add_command(label="Сбросить и начать сначала",
                     command=cancel)
filemenu.add_command(label="Выход (автоматическое сохранение)",
                     command=exitgame)

helpmenu = tkinter.Menu(mainmenu, tearoff=0)
helpmenu.add_command(label="Помощь", command=help)
helpmenu.add_command(label="О программе", command=info)

mainmenu.add_cascade(label="Меню", menu=filemenu)
mainmenu.add_cascade(label="Справка", menu=helpmenu)

if result == 0:
    dialog = CustomDialog(root, prompt="Как ты меня назовёшь?")
    result = dialog.show()


nameLabel = tkinter.Label(root, text="Меня зовут " + str(result),
                          font=('Times New Roman', 25))
nameLabel.pack()

root.bind('<Return>', start_game)
root.mainloop()

f = open("save.txt", 'w')
args = [hunger, year, energy, happy, result]
f.writelines("%s\n" % i for i in args)
f.close()
