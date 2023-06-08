import pymongo
import tkinter as tk
from tkinter import messagebox
import ssl
import datetime

client = pymongo.MongoClient("mongodb+srv://CasperNS:Carlos12@cluster0.kcod6.mongodb.net/Store?retryWrites=true&w=majority", ssl_cert_reqs=ssl.CERT_NONE)
db = client["Store"]
users = db["Users"]
products = db["Products"]
chekOutHistory = db["Check_Out_History"]

currentUser = 0

def Cart():
    for user in users.find({"currentuser" : True}):
        currentUser = user
    cart = tk.Toplevel()
    cart.geometry("400x400")
    cart.config(background="#ACD8E6")
    cart.title(f'{currentUser["name"]}s cart')
    productList = []
    frame = tk.Frame(cart, background="#ACD8E6")
    frame.pack()
    #Gets all the items in the current users cart and retrieves the name and description.
    #Appends it all to the variable productList. 
    for user in users.find({"name" : currentUser["name"]},{"cart.name" : 1, "cart.description" : 1}):
        if user["cart"]:
            for product in user["cart"]:
                productList.append(product)
                for x in range(len(productList)):
                    #A "remove from cart button" is added under each cart object
                    #Again the use of lambda is to make sure that the each button is set to the right object.
                    removeFromCartButton = tk.Button(frame, text="Remove from Cart", width=15, command=lambda x=x : removeFromCart(productList[x]))
                productWindow = tk.Text(frame, width=70, height=5)
                productWindow.insert(tk.END, f'Name: {product["name"]}\nDescription: {product["description"]}')
                productWindow.pack()
                removeFromCartButton.pack()
        else:
            empty_cart = tk.Label(cart, text="Your cart is empty", background="#ACD8E6")
            empty_cart.pack(pady=10)
    #The function that removes the selected object from the cart. 
    def removeFromCart(product):
        nonlocal frame
        users.update({"name" : currentUser["name"]}, {"$pull" : {"cart" : {"name" : product["name"]}}})
        cart.destroy()
        Cart()
    #First it checks if there are any items in the cart.
    # If there are all the items value available is set to fale.
    # And an insert is made to checkOutHistory with the users name, the content of the cart and the date.   
    def checkOut():
        if productList:
            for product in productList:
                products.update_one({"name" : product["name"]}, {"$set" : {"available" : False}})
            messagebox.showinfo("Sucess", "Thank you for the purchase")
            users.update_one({"name" : currentUser["name"]}, {"$set" : {"cart" : []}})
            chekOutHistory.insert({"userName" : currentUser["name"], "date" : datetime.datetime.now(), "products" : productList})
            cart.destroy()
        else:
            #If there is nothing in the cart the user tries to check out
            #this message will be shown. 
            messagebox.showinfo("Error", "Cart is empty")
    checkOutButton = tk.Button(cart, text="Check Out", width=15, command=checkOut)
    checkOutButton.pack(pady=10)
    cart.mainloop()