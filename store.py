import pymongo
import tkinter as tk
from tkinter import messagebox, filedialog
import ssl
import base64
from PIL import Image,ImageTk
from cart import Cart
from myPage import goToMyPage

client = pymongo.MongoClient("mongodb+srv://CasperNS:Carlos12@cluster0.kcod6.mongodb.net/Store?retryWrites=true&w=majority", ssl_cert_reqs=ssl.CERT_NONE)
db = client["Store"]
users = db["Users"]
products = db["Products"]
chekOutHistory = db["Check_Out_History"]

currentUser = 0

def store():
    #Currentuser is collected from the database.
    global currentUser
    for user in users.find({"currentuser" : True}):
        currentUser = user
    store = tk.Tk()
    store.geometry("800x800")
    store.title("Store")
    store.config(background="#ACD8E6")
    buttonBox = tk.Frame(store, background="#ACD8E6")
    buttonBox.pack()
    product = tk.Button(buttonBox, text="Post Product", width=20, command=postProduct)
    searchBar = tk.Entry(store, width=20)
    goToCartButton = tk.Button(buttonBox, text="Go to cart", width=20, command=Cart)
    myPage = tk.Button(buttonBox, text="My page", width=20, command=goToMyPage)
    frame = tk.Frame(store, background="#ACD8E6")
    def fillstoreWindow():
        nonlocal frame
        productList = []
        frame.destroy()
        frame = tk.Frame(store)
        frame.pack()
        #Gets all the products in the database that is available by checking if its valeu is True.
        #And appends all the products to the list productList.
        for product in products.find({"available" : True}):
            nameTagsList = list(product["tags"]) + list(product["name"].split(" "))
            if any(item in searchBar.get().split(" ") for item in nameTagsList):
                productList.append(product)
                def addToCart(product):
                    users.update_one({"name" : currentUser["name"]}, {"$push": {"cart" : product}})
                    messagebox.showinfo("Sucess!", "The product has been added to your cart.")
                productWindow = tk.Text(frame, width=70, height=7)
                buttonbox = tk.Frame(frame)
                for x in range(len(productList)):
                    #These three buttons are added per product in the productlist
                    #Have to use lambda so that the value for the buttons are overwritten. 
                    #Add them to a buttonbox so it is possible to have them side by side. 
                    addToCartButton = tk.Button(buttonbox, width=15, text="Add to cart", command= lambda x=x: addToCart(productList[x]))
                    showImageButton = tk.Button(buttonbox, width=15, text="Show image", command= lambda x=x: showImage(productList[x]))
                    goToUserButton = tk.Button(buttonbox, width= 20, text=f'Posted by {product["user"]["name"]}', command= lambda x=x: goToUser(productList[x]))
                productWindow.insert(tk.END, f'Name: {product["name"]}\nDescription: {product["description"]}')
                productWindow.pack(side=tk.TOP)
                buttonbox.pack()
                addToCartButton.pack(side=tk.LEFT)
                showImageButton.pack(side=tk.LEFT)
                goToUserButton.pack(side=tk.LEFT)
    searchButton = tk.Button(store, text="Search", width=15, command=fillstoreWindow)
    product.pack(side=tk.LEFT, pady=20)
    goToCartButton.pack(side=tk.LEFT, pady=20)
    myPage.pack(side=tk.LEFT, pady=20)
    searchBar.pack()
    searchButton.pack(pady=10)
    #This function is ran if the window closes.
    #When it is ran it unsets the value "currentuser" for the user that is logged in.
    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            users.update({"currentuser" : True}, {"$unset" : {"currentuser" : 1}})
            store.destroy()
    #This protocol checks if the window is active and runs the function on_closing
    #when it closes. 
    store.protocol("WM_DELETE_WINDOW", on_closing)
    store.mainloop()

#Post Product opens a separate window where you can all the information about the product
#and post a picutre of said product. 
def postProduct():
    img = 0
    productPage = tk.Toplevel()
    productPage.config(background="#ACD8E6")
    productPage.title("Post a product")
    productPage.geometry("400x250")
    name_label = tk.Label(productPage, text="Name", bg="#ACD8E6")
    name = tk.Entry(productPage, width=20, bg="White")
    descriptionLabel = tk.Label(productPage, text="Description", bg="#ACD8E6")
    description = tk.Entry(productPage, width=50)
    tagsLabel = tk.Label(productPage, text="Tags", bg="#ACD8E6")
    tags = tk.Entry(productPage, width=30)
    def check():
        tag_list = list(tags.get().split(" "))
        products.insert_one({"name" : name.get(), "description" : description.get(), "available" : True, "user" : currentUser, "photo" : img, "tags" : tag_list})
        messagebox.showinfo("Sucess!", "Product has been posted")
        productPage.destroy()
    #When it posts the picture it gets encoded to a string and added in the code above. 
    def postPicture():
        nonlocal img
        file_path = filedialog.askopenfilename()
        with open(file_path, "rb") as imageFile:
            img = base64.b64encode(imageFile.read())
        messagebox.showinfo("Sucess!", "Picture has been added.")
    postPictureButton = tk.Button(productPage, text="Add Picture", width=15, command=postPicture)
    postButton = tk.Button(productPage, text="Post", width=15, command=check)
    name_label.pack()
    name.pack()
    descriptionLabel.pack()
    description.pack()
    tagsLabel.pack()
    tags.pack()
    postPictureButton.pack(pady=15)
    postButton.pack()
    productPage.mainloop()

#Here the image string is retrieved from the database and decoded.
#A new window pops up and the image is displayed. 
def showImage(product):
    imagebox = tk.Toplevel()
    imagebox.title("Image")
    b = products.find({"name" : product["name"]}).distinct("photo")
    with open(f'{product["name"]}.jpg', "wb") as fimage:
        fimage.write(base64.b64decode(b[0]))
    canv = tk.Canvas(imagebox)
    canv.pack(fill=tk.BOTH, expand=1)
    global img
    img = ImageTk.PhotoImage(Image.open(f'{product["name"]}.jpg'))
    canv.create_image(0,0, image=img, anchor=tk.NW)

#This gets all the information about the user that posted the product.
#You can see the name of the user and the name and description of the 
#products he or she has for sale. 
def goToUser(product):
    userWindow = tk.Toplevel()
    userWindow.config(background="#ACD8E6")
    userWindow.geometry("600x600")
    userWindow.title(f'Products posted by {product["user"]["name"]}')
    userInfo = tk.Label(userWindow, text=f'Username: {product["user"]["name"]}', bg="#ACD8E6")
    userInfo.pack(pady=10)
    for product in products.find({"user._id" : product["user"]["_id"]}):
        productWindow = tk.Text(userWindow, width=70, height=7)
        productWindow.insert(tk.END, f'Name: {product["name"]}\nDescription: {product["description"]}\nAvailable: {product["available"]}')
        productWindow.pack()
    userWindow.mainloop()

