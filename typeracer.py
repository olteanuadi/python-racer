import tkinter as tk
import threading
import multiprocessing
import time
import random
from tkinter.constants import ANCHOR
import cx_Oracle

# Creating database connection
# lib_dir = r"ORACLE_CLIENT"

cx_Oracle.init_oracle_client(lib_dir=lib_dir)

# connection = cx_Oracle.connect('DATABASE_DETAILS')
cursor = connection.cursor()
############################# Functions ##############################

text_dictionary = {1:"You clearly don't know who you're talking to, so let me clue you in. I am not in danger, Skyler. I am the danger. A guy opens his door and gets shot and you think that of me? No. I am the one who knocks!",

2:"Sometimes she did not know what she feared, what she desired: whether she feared or desired what had been or what would be, and precisely what she desired, she did not know.",

3:"Kid, I've flown from one side of this galaxy to the other, and I've seen a lot of strange stuff. But I've never seen anything to make me believe that there's one all-powerful Force controlling everything. There's no mystical energy field that controls MY destiny.",

4:"With all six stones, I could simply snap my fingers, they would all cease to exist and I call that... mercy. And then what? I finally rest, and watch the sun rise on a grateful universe. The hardest choices require the strongest wills.",

5:"The capacity to love is determined by the fact that man is ready to seek the good consciously with others, to subordinate himself to this good because of others, or to subordinate himself to others because of this good.",

6:"He said that if culture is a house, then language was the key to the front door; to all the rooms inside. Without it, he said, you ended up wayward, without a proper home or a legitimate identity.",

7:"Whoever could make two ears of corn, or two blades of grass, to grow upon a spot of ground where only one grew before, would deserve better of mankind, and do more essential service to his country, than the whole race of politicians put together.",

8:r"Every night you cry yourself to sleep, thinking 'Why does this happen to me?' Why does every moment have to be so hard? Hard to believe that it's not over tonight, just give me one more chance to make it right. I may not make it through the night, I won't go home without you.",

9:"I learned to write because I am one of those people who somehow cannot manage the common communications of smiles and gestures, but must use words to get across things that other people would never need to say.",

10:"After removal from the oven, the pizza is sliced and plated quickly in a flat cardboard box, which is immediately closed and often taped shut. There is no physical separation after the slicing, so that edge can be ignored and we can treat the pizza, for thermal purposes, as an infinite plane.",}

chosen_text = text_dictionary.get(random.randrange(1, 10))

initial_time = 75
show_time = 0
index = 0
characters = 0
right_characters = 0
accuracy = 0
wpm = 0
points = 0
words = 0
name = "Unknown"
go_home = False
menu_index = 0
def play_game():
    start_time = time.time()
    global initial_time, show_time

    # Countdown function
    def countdown():
        show_time = initial_time
        while show_time > -1:
            # Coloring the timer red when it goes under 10 sec
            if show_time <= 10:
                timer_lbl.config(fg="red")
            # Ending thread when time is 0
            if show_time == 0:
                set_end_screen()
                timer_lbl.destroy()
                text_txt.pack(padx=30, pady=(60,20), anchor=tk.W)
                try:
                    t1.join()
                except:
                    print("T1 problem")
            timer_lbl["text"] = show_time
            show_time -= 1
            time.sleep(1)

    def set_end_screen():
            
        # Getting the stats and name to update the db
        def get_name():
            name = enter_name_ent.get()
            print(name)

            # Sending the stats to the database
            try:
                send_wpm = int(wpm)
                send_acc = int(accuracy)
                cursor.execute(f'insert into useri values(0,\'{name}\',{send_wpm},{send_acc},{points})')
                connection.commit()
            except cx_Oracle.Error as error:
                print(error)
            finally:
                # release the connection
                if cursor:
                    cursor.close()
                if connection:
                    connection.close()

            root.destroy()

        points = int((wpm * 2) + (accuracy * 1.5) + (90 - int(time.time() - start_time) * 1.5))
        points_lbl["text"] = f"Points : {points}"

        # Submitting your name screen
        text_ent_frm.destroy()
        name_frm = tk.Frame(mid_frm, bg="#424242")
        name_frm.rowconfigure(0, minsize = 70)
        name_frm.columnconfigure(0, minsize = 300)
        name_frm.columnconfigure(1, minsize = 300)
        name_frm.columnconfigure(2, minsize = 100)
        enter_name_lbl = tk.Label(name_frm, text="Submit your name : ", bg="#424242", fg="white", font=("",30))
        enter_name_ent = tk.Entry(name_frm, bg="#424242", fg="white", font=("",30))
        submit_name = tk.Button(name_frm, bg="#424242", fg="white", text="\u2713", font=("",30), command=get_name)
        enter_name_lbl.grid(row=0, column=0, sticky="nsew")
        enter_name_ent.grid(row=0, column=1, sticky="nsew")
        submit_name.grid(row=0, column=2, sticky="nsew", padx=15)
        name_frm.pack(padx=20, pady=10, anchor=tk.W)


    def check_letters():
        global index, characters, right_characters, accuracy, wpm, points, words, name, go_home

        # Counting the characters in a text
        for i in range(int(len(chosen_text))):
            characters += 1

        while True:

            # When the player has finished typing
            try:
                if chosen_text[index] == None:
                    print("You have finished")
            except:
                set_end_screen()
                timer_lbl.destroy()
                text_txt.pack(padx=30, pady=(60,20), anchor=tk.W)

            try:
                # Accuracy label changing in real time
                accuracy = int((100 * right_characters)/index)
                accur_lbl["text"] = f"Accuracy : {accuracy}%"

                # WPM label changing in real time
                compare_time = time.time()-start_time
                wpm = (words * 60) / compare_time
                wpm_lbl["text"] = f"WPM : {int(wpm)}"

            except:
                print("Division by 0")
            if show_time == 1:
                try:
                    t2.join()
                except:
                    print("Thread 2 caught")
            written = text_ent.get()
            # If nothing is written at the beggining
            while len(written) == 0:
                written = text_ent.get()
                time.sleep(0.01)

            try:
                # If a correct character was inputed
                if written[index] == chosen_text[index]:
                    if chosen_text[index] == " ":
                        words += 1
                        print(words)
                    # Hilighting correct characters
                    text_txt.tag_add("right", "1.0", f"1.{index + 1}")
                    text_txt.tag_config("right", background="green", foreground="white")
                    # For accuracy
                    right_characters += 1
                    initial_characters = right_characters
                    time.sleep(0.01)
                    
                # If a wrong character was inputed
                else:
                    #Hilighting wrong characters
                    text_txt.tag_add("wrong", f"1.{index}", f"1.{index + 1}")
                    text_txt.tag_config("wrong", background="black", foreground="red")
                    time.sleep(0.01)

                    # For accuracy
                    if initial_characters == right_characters:
                        right_characters -= 1
                    index -= 1
            except:
                time.sleep(0.1)
                index -= 1
                pass
            index += 1

    play_frm.destroy()
    ldb_frm.destroy()

    # The timer label
    timer_lbl = tk.Label(mid_frm, bg="#424242", fg="white", font=("", 40))
    t1 = threading.Thread(target=countdown, name="t1")
    t1.start()
    timer_lbl.pack(pady=20, padx = 900)

    # What we have to type
    text_txt = tk.Text(mid_frm, height=5, width=47, bg="#424242", fg="white", font=("", 27), wrap=tk.WORD)
    text_txt.insert(0.0, chosen_text)
    text_txt["state"] = tk.DISABLED
    text_txt.pack(padx=30, pady=(0,20), anchor=tk.W)

    # The entry where we type
    text_ent_frm = tk.Frame(mid_frm, bg="#424242")
    text_ent_frm.columnconfigure(0, minsize = 900)
    text_ent_frm.rowconfigure(0, minsize = 80)
    text_ent = tk.Entry(text_ent_frm, bg="#424242", fg="white", font=("", 25))
    text_ent.grid(row=0, column=0, sticky="nsew")
    text_ent_frm.pack(padx=45, pady=45, anchor=tk.W)

    # The frame that shows the stats as WPM, ACCURACY, POINTS
    stats_frm = tk.Frame(mid_frm, bg="#424242")
    stats_frm.columnconfigure([0,1,2], minsize=290)
    stats_frm.rowconfigure(0, minsize=100)
    # The stats themselves
    wpm_lbl = tk.Label(stats_frm, bg="#424242", fg="white", text="WPM : -", font=("",25))
    accur_lbl = tk.Label(stats_frm, bg="#424242", fg="white", text="Accuracy : -", font=("",25))
    points_lbl = tk.Label(stats_frm, bg="#424242", fg="white", text="Points : -", font=("",25))
    wpm_lbl.grid(row=0, column=0, sticky="nsew")
    accur_lbl.grid(row=0, column=1, sticky="nsew")
    points_lbl.grid(row=0, column=2, sticky="nsew")
    stats_frm.pack(padx=40, pady=5, anchor=tk.W)


    t2 = threading.Thread(target=check_letters, name="t2")
    t2.start()

# Method for ldb tab
def ldb_window():
    global menu_index

    ldb_lbox_frm = tk.Frame(mid_frm, bg="#424242")
    ldb_lbox_frm.columnconfigure(0, minsize=970)
    ldb_lbox_frm.columnconfigure(1, minsize=30)
    ldb_lbox_frm.rowconfigure(0, minsize=600)
    listbox = tk.Listbox(ldb_lbox_frm, bg = "#424242", fg = "white", font=("",25))
    scrollbar = tk.Scrollbar(ldb_lbox_frm)
    scrollbar.config(command = listbox.yview)
    listbox.config(yscrollcommand = scrollbar.set)
 
    cursor.execute("select trim(nume), round(wpm), accuracy, round(points) from useri order by points desc , accuracy desc, wpm desc")
    list = cursor.fetchall()
    index = 0
    # Adding players to the ldb tab
    for element in list:
        spaces_len = 50
        spaces = ""
        for i in range(len(element[0])):
            spaces_len -= 1
        for i in range(spaces_len):
            spaces += " "
        # Header and first player of the list
        if index == 0:
            string = "Name :" + spaces[:len(spaces) - 16] + "Points :       " + "WPM :     " + "Accuracy : "
            listbox.insert(tk.END, string)
            string = f"{index + 1}    {element[0]}" + spaces[(len(element[0]) + 10):] + f"{element[3]}              " + f"{element[1]}               " + f"{element[2]}%"
            listbox.insert(tk.END, string)
        # The rest of the players
        else:
            string = f"{index + 1}    {element[0]}" + spaces[len(element[0]) + 10:] + f"{element[3]}              " + f"{element[1]}               " + f"{element[2]}%"
            listbox.insert(tk.END, string)
        index += 1
        listbox.itemconfig("end", bg = "#1e1e1e" if index % 2 == 0 else "#191919")

    menu_index += 1
    if menu_index % 2 == 1:
        play_frm.destroy()
        ldb_frm.destroy()

        listbox.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="nsew")
        ldb_lbox_frm.pack(anchor=tk.W)
    else:
        ldb_lbox_frm.destroy()
        scrollbar.destroy()
        listbox.destroy()
        print("Finally you see me!")

#######################################################################

# Creating new window
root = tk.Tk()
root.title("TypeRacer")
root.resizable(False, False)
root.geometry("1000x900")
root.rowconfigure(0, minsize=150)
root.rowconfigure(1, minsize=600)
root.rowconfigure(2, minsize=150)
root.columnconfigure(0, minsize=1500)

############################# TOP Frame ###############################

top_frm = tk.Frame(root, bg="#c64552", height=150, width=1500)

home_btn = tk.Button(top_frm, bg="#c64552", highlightthickness = 0, bd = 0)
home_icon = tk.PhotoImage(file="C:/Users/adiso/Desktop/#PROJECTS/PythonStuff/typeracer/home_icon.png")
home_btn.config(image=home_icon)
home_btn.grid(row=0, column=0, padx=(100,0), sticky="ew")

title_lbl = tk.Label(top_frm, text="TypeRacer", bg="#c64552", 
fg="white", font=("",70))
title_lbl.grid(row=0, column=1, padx=130, pady=20, sticky="nsew")

ldb_btn = tk.Button(top_frm, bg="#c64552", highlightthickness = 0, bd = 0, command=ldb_window)
ldb_icon = tk.PhotoImage(file="C:/Users/adiso/Desktop/#PROJECTS/PythonStuff/typeracer/ldb_icon.png")
ldb_btn.config(image=ldb_icon)
ldb_btn.grid(row=0, column=2, padx=(0,100), sticky="ew")

top_frm.grid(row=0, column=0, sticky="nsew")
#######################################################################





############################# Mid Frame ###############################

mid_frm = tk.Frame(root, bg="#424242")
mid_frm.rowconfigure(0, minsize=200)
mid_frm.rowconfigure(1, minsize=420)
mid_frm.columnconfigure(0, minsize=1000)

play_frm = tk.Frame(mid_frm, bg="#424242")
play_frm.rowconfigure(0, minsize=200)
play_frm.columnconfigure(0, minsize=400)
play_btn = tk.Button(play_frm, bg = "#00b5dd", fg="#e5faff", text="Play", font=("",40), command=play_game)
play_btn.grid(row=0, column=0, sticky="ew")
play_frm.grid(row=0, column=0, padx=300, sticky="nsew")

ldb_frm = tk.Frame(mid_frm, bg="black")
ldb_frm.columnconfigure([0, 1, 2, 3], minsize=230)
for i in range(4):
    categ_list = ["Name", "WPM", "Accuracy", "Points"]
    ldb_element = tk.Label(ldb_frm, text=categ_list[i], bg="black", fg="white", font=("", 20))
    ldb_element.grid(row=0, column=i, pady=(20,0), sticky="nsew")

# Getting top players and theirs stast from db
cursor.execute("select trim(nume), round(wpm), accuracy, round(points) from useri order by points desc , accuracy desc, wpm desc")
list = cursor.fetchall()
index = 0

# Printing top players in the ldb box in home
for element in list:
    tk.Label(ldb_frm, text=element[0], bg="black", fg="white", font=("", 20)).grid(row=index + 1, column=0, pady=15, sticky="nsew")
    tk.Label(ldb_frm, text=element[1], bg="black", fg="white", font=("", 20)).grid(row=index + 1, column=1, pady=15, sticky="nsew")
    tk.Label(ldb_frm, text=element[2], bg="black", fg="white", font=("", 20)).grid(row=index + 1, column=2, pady=15, sticky="nsew")
    tk.Label(ldb_frm, text=element[3], bg="black", fg="white", font=("", 20)).grid(row=index + 1, column=3, pady=15, sticky="nsew")
    if index == 0:
        tk.Label(ldb_frm, text=element[0], bg="black", fg="#ffee00", font=("", 20)).grid(row=index + 1, column=0, pady=15, sticky="nsew")
        tk.Label(ldb_frm, text=element[1], bg="black", fg="#ffee00", font=("", 20)).grid(row=index + 1, column=1, pady=15, sticky="nsew")
        tk.Label(ldb_frm, text=element[2], bg="black", fg="#ffee00", font=("", 20)).grid(row=index + 1, column=2, pady=15, sticky="nsew")
        tk.Label(ldb_frm, text=element[3], bg="black", fg="#ffee00", font=("", 20)).grid(row=index + 1, column=3, pady=15, sticky="nsew")
    index += 1
    if index == 4:
        break

ldb_frm.grid(row=1, column=0, pady=20, padx=10, sticky="nsew")
mid_frm.grid(row=1, column=0, sticky="nsew")
#######################################################################





############################# Bot Frame ###############################
bot_frm = tk.Frame(root, bg="#282828", height=90, width=1500)
bot_frm.grid(row=2, column=0, sticky="nsew")
#######################################################################

root.mainloop()