import pymongo
import tkinter as tk
from tkinter import messagebox
import ssl
from PIL import Image,ImageTk
import base64
from store import store

client = pymongo.MongoClient("mongodb+srv://CasperNS:Carlos12@cluster0.kcod6.mongodb.net/Store?retryWrites=true&w=majority", ssl_cert_reqs=ssl.CERT_NONE)
db = client["Store"]
users = db["Users"]
products = db["Products"]
chekOutHistory = db["Check_Out_History"]
images = db["Images"]

currentUser = 0


#The main window is the first window being opened with a login and register button.
def main():
    main = tk.Tk()
    main.geometry("425x250")
    main.config(background="#ACD8E6")
    main.title("Log in")
    text = tk.Canvas(main, background="#ACD8E6", highlightthickness=0)
    text.pack()
    global img
    with open("login_img.png", "wb") as fimage:
        fimage.write(base64.b64decode(images.find().distinct("login image")[0]))
    img = (Image.open("login_img.png"))
    resize_img = img.resize((80,80), Image.ANTIALIAS)
    new_img = ImageTk.PhotoImage(resize_img)
    text.create_image(210,48, image=new_img)
    tk.Label(main, text="Username:", bg="#ACD8E6").place(relx=.35,rely=.4, anchor="center")
    username = tk.Entry(main, width=20)
    username.place(relx=.6,rely=.41, anchor="center")
    tk.Label(main, text="Password:", bg="#ACD8E6").place(relx=.35,rely=.5, anchor="center")
    passwordEntry = tk.Entry(width=20, show="*")
    passwordEntry.place(relx=.6,rely=.5, anchor="center")

    #The login function with an if/else to check if the content of the entries are valid. 
    #If everything checks out it loads the store window with store() and at the same
    #time destroys the current window. 
    def login():
        global currentUser
        name = 0
        for user in users.find({"name" : username.get()}):
            name = user
        if len(username.get()) == 0 or len(passwordEntry.get()) == 0:
            messagebox.showinfo("Error", "Both username and password must be filled in")
        elif username.get() not in users.find().distinct("name"):
            messagebox.showinfo("Error", "Username does not exists")
        elif name["password"] != passwordEntry.get():
            messagebox.showinfo("Error", "Wrong password")
        elif name["password"] == passwordEntry.get():
            main.destroy()
            #Here the user that logs in is set as currentuser which all the queries later on is based on. 
            users.update({"name" : name["name"]}, {"$set" : {"currentuser" : True}})
            currentUser = name
            store()
        
    loginButton = tk.Button(text="Login", width=15, command=login).place(relx=.4,rely=.65, anchor="center")
    registerButton = tk.Button(text="Register", width=15, command=register).place(relx=.7,rely=.65, anchor="center")
    main.mainloop()

#Register function with a simple database update if the username is not already in the database.
#Retrieves all the name using the .distinct() function that gets all the names as a list.
#If the name get() from the username entry is not in that list a user is created. 
def register():
    window = tk.Tk()
    window.config(background="#ACD8E6")
    window.geometry("425x225")
    window.title("Register")
    tk.Label(window, text="Username:", bg="#ACD8E6").place(relx=.35,rely=.4, anchor="center")
    usernameEntry = tk.Entry(window, width=20)
    usernameEntry.place(relx=.6,rely=.41, anchor="center")
    tk.Label(window, text="Password:", bg="#ACD8E6").place(relx=.35,rely=.5, anchor="center")
    passwordEntry = tk.Entry(window, width=20,show="*")
    passwordEntry.place(relx=.6,rely=.5, anchor="center")
    def check():
        if usernameEntry.get() in users.find().distinct("name"):
            messagebox.showinfo("Error", "User already used")
        else:
            user = usernameEntry.get()
            password = passwordEntry.get()
            users.insert_one({"name" : user, "password" : password, "cart" : []})
            messagebox.showinfo("Sucess", "User sucessfully created")
            window.destroy()
    submit = tk.Button(window, text="Submit", command=check).place(relx=.55,rely=.65, anchor="center")
    window.mainloop()


#Run this script to start the whole program. 
main()
