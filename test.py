from typing import IO
import pymongo
import tkinter as tk
from tkinter import Entry, Label, Text, Tk, messagebox, filedialog
from tkinter.constants import END, LEFT, WORD
import datetime
import ssl
import base64
from PIL import Image, ImageTk

client = pymongo.MongoClient("mongodb+srv://CasperNS:Carlos12@cluster0.kcod6.mongodb.net/Store?retryWrites=true&w=majority", ssl_cert_reqs=ssl.CERT_NONE)
db = client["Store"]
users = db["Users"]
products = db["Products"]

import pymongo
import tkinter as tk
from tkinter import messagebox
import ssl
from PIL import Image,ImageTk
from store import store

client = pymongo.MongoClient("mongodb+srv://CasperNS:Carlos12@cluster0.kcod6.mongodb.net/Store?retryWrites=true&w=majority", ssl_cert_reqs=ssl.CERT_NONE)
db = client["Store"]
users = db["Users"]
products = db["Products"]
chekOutHistory = db["Check_Out_History"]
images = db["Images"]

