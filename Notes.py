from tkinter import *
from tkinter import ttk
import pickle
import os.path


root=Tk()
root.geometry('1200x600')
root.resizable(0,0)
root.title('Notebook')
first_open=FALSE

users = []

#Load users only when first opened -> Save users only before exitting
#Need a list of objects in memory 
#proba

#Local Data Functions
def save_object(objects,filename):
    with open(filename,'wb') as outp:
        for user in objects:
          pickle.dump(user,outp,pickle.HIGHEST_PROTOCOL)

def pickleLoader(pklFile):
    try:
        while True:
            yield pickle.load(pklFile)
    except EOFError:
        pass

def load_object(filename):

    if os.path.isfile(filename):    
        with open(filename,'rb') as inp:
            for usr in pickleLoader(inp):
                users.append(usr)
                select.insert(END,usr.username)
        
class User(object):
    def __init__(self,username,password,note):
        self.username=username
        self.password=password
        self.note=note


#Function to Get Selected Value
def Selected():
    return int(select.curselection()[0])


#Adding a new Note
def AddNote():
    Newuser=User(usernameEntry.get(),passwordEntry.get(),noteEntry.get("1.0",END))
    users.append(Newuser)
    select.insert(END,Newuser.username)

    usernameEntry.delete(0,END)
    passwordEntry.delete(0,END)
    noteEntry.delete('1.0',END)

def NoteCheck():
    user_ind=Selected()
    if len(users)>0:
        if user_ind<len(users):
            NotePopup()

#Note Popup
def NotePopup():

    def isCorrect(curr_user):
         password=passw.get() 

         if password==curr_user.password:
             passw_status.config(text='Correct!',fg="green")
             passw.delete(0,END)
             user_note.delete('1.0',END)
             user_note.insert(END,curr_user.note)            

         else: 
             passw_status.configure(text='Incorrect!',fg="red")
             passw.delete(0,END)
            

    user_ind=Selected()
    curr_user=users[user_ind]

    note=Tk()
    note.title(f"{curr_user.username}'s Note")
    note.geometry('500x550')

    Label(note,text="PASSWORD",font=("Helvetica",15,"bold")).place(x=160,y=80)
    passw=Entry(note,show="*",)
    passw.place(x=150,y=120)
    passw_status=Label(note,text='',font=("Helvetica",10))
    passw_status.place(x=200,y=150)

    Label(note,text="NOTE",font=("Helvetica",15,"bold")).place(x=200,y=250)

    user_note=Text(note,height=9,width=40)
    user_note.place(x=40,y=300)

    note.bind('<Return>', lambda x: isCorrect(curr_user))


def on_closing():
    save_object(users,'users.pkl')
    root.destroy()


def DeleteNote():
    user_ind=Selected()
    curr_user=users[user_ind]
    users.remove(curr_user)
    select.delete(user_ind)


Label(root,text="NOTEBOOK",font=("Helvetica",20,"bold")).place(x=200,y=50)
Label(root,text='USERNAME',font="12").place(x=150,y=150)
usernameEntry=Entry(root,width=25)
usernameEntry.place(x=300,y=150)

Label(root,text='PASSWORD',font="12").place(x=150,y=250)
passwordEntry=Entry(root,show="*",width=25)
passwordEntry.place(x=300,y=250)

Label(root,text='NOTE',font="12").place(x=150,y=350)
noteEntry=Text(root,height=9,width=40)
noteEntry.place(x=300,y=330)
Button(root,text="ADD",cursor="hand2",command=AddNote).place(x=430,y=540)
Button(root,text="DELETE",cursor="hand2",command=DeleteNote).place(x=530,y=540)


Label(root,text='USERS',font="12").place(x=950,y=50)
frame = Frame(root)
frame.place(x=900,y=100)

Button(root,text="View Note",cursor="hand2",command=NoteCheck).place(x=950,y=540)


scroll = ttk.Scrollbar(frame,orient=VERTICAL)
select = Listbox(frame,yscrollcommand=scroll.set,height=20)
scroll.config(command=select.yview)
scroll.pack(side=RIGHT,fill=Y)
select.pack(side=LEFT,fill=BOTH,expand=1)


if first_open==FALSE:
    
    load_object('users.pkl')
    first_open=TRUE

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
