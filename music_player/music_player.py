from tkinter import *
from tkinter import ttk
import mysql.connector
from tkinter import messagebox

window=Tk()
window.title("MUSIC PLAYER")

screen_width=window.winfo_screenwidth()
screen_height=window.winfo_screenheight()
window.geometry(f"{screen_width}x{screen_height}")


login_frame=Frame(window,bg="light blue")
login_frame.pack(fill=BOTH,expand=True)

title_label=Label(login_frame,text="Login page",bg="light blue",fg="black",font=("arial",24))
title_label.place(x=600,y=10)

username_label=Label(login_frame,text="username :",bg="light blue",fg="black",font=("arial",20))
username_label.place(x=500,y=60)

username_entry=Entry(login_frame,font=("arial",20))
username_entry.place(x=650,y=65)
username_entry.focus()

password_label=Label(login_frame,text='password :',bg="light blue",fg="black",font=("arial",20))
password_label.place(x=500,y=130)

password_entry=Entry(login_frame,font=("arial",20),show="*")
password_entry.place(x=650,y=133)

#function for login button command
def get_data():
    conn=mysql.connector.connect(host="localhost",database="registration",user="root",password="")
    cur=conn.cursor()
    username=username_entry.get()
    password=password_entry.get()

    sql_query="select * from users where Email_id=%s and confirm_password=%s"
    cur.execute(sql_query,[(username),(password)])
    result=cur.fetchall()

    if result:
        messagebox.showinfo("success","login successfull")
        register_frame.pack_forget()
        music_frame.pack(fill=BOTH,expand=True)

    else:
        messagebox.showerror("error","Invalid data")

login_button=Button(login_frame,text="Login",bg="light blue",font=("arial",20),command=get_data)
login_button.place(x=600,y=210)

def show_details():
    login_frame.pack_forget
    register_frame.pack(fill=BOTH,expand=True)

register_button=Button(login_frame,text="register",bg="light blue",font=("arial",20),command=show_details)
register_button.place(x=750,y=210)

#-----------registration details----

register_frame=Frame(login_frame,bg="light green")

title_register_label=Label(register_frame,text="Registration page",bg="light green",font=("arial",24))
title_register_label.pack()

username_register_label=Label(register_frame,text="username",bg="light green",font=("arial",20))
username_register_label.pack()

username_register_entry=Entry(register_frame,font=("arial",20))
username_register_entry.pack()

gender=Label(register_frame,text="gender",bg="light green",font=("arial",20))
gender.pack()

temp_var=StringVar()
gender=ttk.Combobox(register_frame,textvariable=temp_var,values=("male","female"),font=("arial",20))
gender.bind("<<ComboboxSelected>>")
gender.pack()

mail_id=Label(register_frame,text="Email-id",bg="light green",font=("arial",20))
mail_id.pack()

mail_id_entry=Entry(register_frame,font=("arial",20))
mail_id_entry.pack()

password_register_label=Label(register_frame,text="password",bg="light green",font=("arial",20))
password_register_label.pack()

password_register_entry=Entry(register_frame,font=("arial",20))
password_register_entry.pack()

confirm_password_label=Label(register_frame,text="confirm password",bg="light green",font=("arial",20))
confirm_password_label.pack()

confirm_password_entry=Entry(register_frame,font=("arial",20))
confirm_password_entry.pack()

def submit_data():
    input_username=username_register_entry.get()
    input_gender=gender.get()
    input_email=mail_id_entry.get()
    input_password=password_register_entry.get()
    input_confirm_password=confirm_password_entry.get()

    db_connection=mysql.connector.connect(host="localhost",database="registration",user="root",password="")
    cursor=db_connection.cursor()

    sql="insert into users (username,gender,Email_id,password,confirm_password)values(%s,%s,%s,%s,%s)"
    data=(input_username,input_gender,input_email,input_password,input_confirm_password)
    result=cursor.execute(sql,data)
    db_connection.commit()

    if result is None:
        messagebox.showinfo("success","sucessfully registered")
        cursor.close()
        db_connection.close()

    register_frame.pack_forget()
    login_frame.pack()

submit_button=Button(register_frame,text="submit",bg="light green",font=("arial",20),command=submit_data)
submit_button.pack()

#------------------music player system-----------
music_frame=Frame(login_frame,width=False,height=False)

from pygame import mixer
import pygame
from PIL import ImageTk,Image
import os
from tkinter import filedialog

music_frame.winfo_geometry()
music_frame.configure(bg="light pink")

pygame.init()
pygame.mixer.init()

left_frame=Frame(music_frame,width=300,height=300,bg="white")
left_frame.grid(row=0,column=0,padx=1,pady=1)

right_frame=Frame(music_frame,width=500,height=300,bg="black")
right_frame.grid(row=0,column=1,padx=0)

down_frame=Frame(music_frame,width=800,height=200,bg="gray")
down_frame.grid(row=1,column=0,columnspan=3,padx=0,pady=1)

list_box=Listbox(right_frame,selectmode=SINGLE,font=('Arial 18 bold'),width=44,bg='black',fg='white')
list_box.grid(row=0,column=0)

listbox_scrollbar=Scrollbar(right_frame)
listbox_scrollbar.grid(row=0,column=1)

list_box.config(yscrollcommand=listbox_scrollbar.set)
listbox_scrollbar.config(command=list_box.yview)

img_1=Image.open('img1.png')
img_1=img_1.resize((200,200))
img_1=ImageTk.PhotoImage(img_1)
app_image=Label(left_frame,height=210,image=img_1,padx=10,bg='white')
app_image.place(x=50,y=40)

def play_music():
    selected_song=list_box.get(ACTIVE)
    running_song['text']=selected_song
    pygame.mixer.music.load(selected_song)
    pygame.mixer.music.play()

img_2=Image.open('img.2.png')
img_2=img_2.resize((80,80))
img_2=ImageTk.PhotoImage(img_2)
play_button=Button(down_frame,width=80,height=80,image=img_2,padx=10,bg='white',font=('Ivy 10'),command=play_music)
play_button.place(x=112+28,y=35)

def previous_music():
    playing_song=running_song['text']
    index=songs.index(playing_song)
    new_index=index - 1
    playing=songs[new_index]
    mixer.music.load(playing)
    mixer.music.play()

    list_box.delete(0,END)
    show()

    list_box.select_set(new_index)
    running_song['text']=playing

img_3=Image.open('img3.png')
img_3=img_3.resize((80,80))
img_3=ImageTk.PhotoImage(img_3)
previous_button=Button(down_frame,width=80,height=80,image=img_3,padx=10,bg='white',font=('Ivy 10'),command=previous_music)
previous_button.place(x=20+28,y=35)

def next_music():
    playing_song=running_song['text']
    index=songs.index(playing_song)
    new_index=index+1
    playing=songs[new_index]
    mixer.music.load(playing)
    mixer.music.play()

    list_box.delete(0,END)
    show()

    list_box.select_set(new_index)
    running_song['text']=playing

img_4=Image.open('img4.png')
img_4=img_4.resize((80,80))
img_4=ImageTk.PhotoImage(img_4)
next_button=Button(down_frame,width=80,height=80,image=img_4,padx=10,bg='white',font=('Ivy 10'),command=next_music)
next_button.place(x=204+28,y=35)

def pause_music():
    mixer.music.pause()

img_5=Image.open('img5.png')
img_5=img_5.resize((80,80))
img_5=ImageTk.PhotoImage(img_5)
pause_button=Button(down_frame,width=80,height=80,image=img_5,padx=10,bg='white',font=('Ivy 10'),command=pause_music)
pause_button.place(x=296+28,y=35)

def continue_music():
    mixer.music.unpause()

img_6=Image.open('img6.jpg')
img_6=img_6.resize((80,80))
img_6=ImageTk.PhotoImage(img_6)
continue_button=Button(down_frame,width=80,height=80,image=img_6,padx=10,bg='white',font=('Ivy 10'),command=continue_music)
continue_button.place(x=388+28,y=35)

def stop_music():
    mixer.music.stop()

img_7=Image.open('img7.png')
img_7=img_7.resize((80,80))
img_7=ImageTk.PhotoImage(img_7)
stop_button=Button(down_frame,width=80,height=80,image=img_7,padx=10,bg='white',font=('Ivy 10'),command=stop_music)
stop_button.place(x=480+28,y=35)

line=Label(left_frame,width=400,height=2,padx=10,bg='black')
line.place(x=0,y=1)

line=Label(left_frame,width=400,height=2,padx=10,bg='white')
line.place(x=0,y=3)

running_song=Label(down_frame,text="Choose a song",font=('Ivy 10'),width=88,height=1,padx=10,bg='white',fg='black',anchor='nw')
running_song.place(x=0,y=1)

def add_song():
    song=filedialog.askopenfilename(initialdir=os.getcwd(),title="select song", filetypes=[("Audio Files","*.mp3")])
    if song:
        list_box.insert(END,os.path.basename(song))
        songs.append(song)

add_button=Button(down_frame, text="Add song",command=add_song)
add_button.place(x=540+28,y=1)

os.chdir(r'F:\music')
songs=os.listdir()

def show():
    for i in songs:
        list_box.insert(END,i)

show()

mixer.init()
music=StringVar()
music.set('choose one song!')
window.mainloop()