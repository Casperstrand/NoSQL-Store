import pymongo
import tkinter as tk
import ssl


client = pymongo.MongoClient("mongodb+srv://CasperNS:Carlos12@cluster0.kcod6.mongodb.net/Store?retryWrites=true&w=majority", ssl_cert_reqs=ssl.CERT_NONE)
db = client["Store"]
users = db["Users"]
products = db["Products"]
chekOutHistory = db["Check_Out_History"]

currentUser = 0

#Pops up a winow with the name of the current user and the possibility to change the name.
#And a list of all the prodycts the user has posted. 
def goToMyPage():
    global currentUser
    for user in users.find({"currentuser" : True}):
        currentUser = user
    global myPage
    myPage = tk.Toplevel()
    myPage.geometry("400x400")
    myPage.config(background="#ACD8E6")
    myPage.title(f'{currentUser["name"]}`s page')
    tk.Label(myPage, text=f'Username: {currentUser["name"]}', bg="#ACD8E6").pack(pady=10)
    changeNameButton = tk.Button(myPage, text="Change Name", width=15, command=changeNameWindow)
    changeNameButton.pack()
    tk.Label(myPage, text="List of all your products", bg="#ACD8E6").pack(pady=10)
    for product in products.find({"user.name" : currentUser["name"]}):
        productWindow = tk.Text(myPage, width=70, height=5)
        productWindow.insert(tk.END, f'Name: {product["name"]}\nDescription: {product["description"]}\nAvailable: {product["available"]}')
        removeProductButton = tk.Button(myPage, text="Remove", width=15, command=lambda: removeProduct(product))
        productWindow.pack()
        removeProductButton.pack()

#A simple update query to change the active users name. 
#It also changes all the user name in all the products linked to the current user.
def changeNameWindow():

    nameWindow = tk.Toplevel()
    nameWindow.geometry("425x225")
    nameWindow.config(background="#ACD8E6")
    tk.Label(nameWindow, text="Enter new name", background="#ACD8E6").pack()
    name = tk.Entry(nameWindow, width=15)
    name.pack()
    def changeName():
        users.update({"name" : currentUser["name"]}, {"$set" : {"name" : name.get()}})
        products.update({"user.name" : currentUser["name"]}, {"$set" : {"user.name" : name.get()}})
        nameWindow.destroy()
        myPage.destroy()
        goToMyPage()
    enter = tk.Button(nameWindow, text="Enter", width=15, command=changeName)
    enter.pack()

def removeProduct(product):
    products.delete_one({"name" : product["name"]})
    myPage.destroy()
    goToMyPage()


