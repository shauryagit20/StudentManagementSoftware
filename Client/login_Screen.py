import os
import tkinter as tk
import json
import tkinter.messagebox

import requests
from PIL import Image, ImageTk
import studentDetailsCounsellorScreen
import user_authentication
from tkinter import messagebox


class App:
    def __init__(self):
        self.Username = None
        self.Password = None
        self.BASE_URL = "http://127.0.0.1:5000/"
        self.fileExists = False
        self.Background_1 = "#FDF7FF"
        self.Background_2 = "#7600e6"

    def Login_Screen(self):
        # Window Initialization

        self.root = tk.Tk()

        root = self.root
        root.geometry("1280x900")
        root.config(bg=self.Background_1)
        root.resizable(False, False)

        self.Username = tk.StringVar()
        self.Password = tk.StringVar()

        Left_Strip = tk.Frame(self.root, width=500, bg="#7600e6")
        Left_Strip.pack(side=tk.LEFT, fill=tk.Y)

        # # LOGO
        logo_image = (Image.open("Logo.png"))
        logo_image = logo_image.resize((340, 210), Image.ANTIALIAS)
        logo_image = ImageTk.PhotoImage(logo_image)
        panel = tk.Label(Left_Strip, image=logo_image, bg=self.Background_2)
        panel.image = logo_image
        panel.place(x=65, y=60)

        tk.Label(Left_Strip, text="Welcome to the\n\n Student Management\n\n System", fg="white", bg=self.Background_2,
                 font=("Helvetica", 30 ,"bold"), justify="right").place(x =  30, y = 350)
        tk.Label(Left_Strip,text="Developed by:\n Ivy Aspire", fg="white", bg=self.Background_2,
                 font=("Helvetica", 14 ), justify="right").place(x =  300, y = 800)


        # Credentials
        tk.Label(root, text="Login to your account", fg=self.Background_2, bg=self.Background_1,
                 font=("Poppins", 28, "bold"), justify="right").place(x=550, y=220)


        tk.Label(root, text="Username", font=('Poppins bold', 14, "bold"), bg=self.Background_1).place(x=540, y=350)

        self.entryUsername = tk.Entry(root, textvariable=self.Username, width=60,
                                      font=('Poppins bold', 12),borderwidth=15, relief=tk.FLAT)
        self.entryUsername.place(x=618, y=390, height=50)

        tk.Label(root, text="Login to your account", fg=self.Background_2, bg=self.Background_1,
                 font=("Poppins", 28, "bold"), justify="right").place(x=550, y=220)
        username_image = (Image.open("Username.png"))
        username_image = username_image.resize((60, 60), Image.ANTIALIAS)
        username_image = ImageTk.PhotoImage(username_image)
        username_image_label = tk.Label(root, image=username_image,borderwidth=0, bg="white")
        username_image_label.image = username_image
        username_image_label.place(x=545, y=386)

        tk.Label(root, text="Password", font=('Poppins bold', 14, "bold"), bg=self.Background_1).place(x=540, y=460)
        entryPassword = tk.Entry(root, textvariable=self.Password, width=60,
                                 font=('Poppins bold', 12),borderwidth=15, relief=tk.FLAT)
        entryPassword.place(x=618, y=510, height=50)
        password_image = (Image.open("Password.png"))
        password_image = password_image.resize((100, 60), Image.ANTIALIAS)
        password_image = ImageTk.PhotoImage(password_image)
        password_image_label = tk.Label(root, image=password_image,bg = "white", borderwidth=0)
        password_image_label.image = password_image
        password_image_label.place(x=520, y=496)

        logInButton = tk.Button(root, text="Login", fg="white", bg="#392A46", width=10, height=2,
                                font=(('Poppins bold', 16)), command=lambda: self.login())
        logInButton.place(x=800, y=630)


        if ("Credentials.json" in os.listdir()):
            self.fileExists = True
            self.login()

        root.mainloop()

    def login(self):
        if (self.fileExists == False):
            Username = self.Username.get()
            Password = self.Password.get()
            userExists = user_authentication.Login(Username, Password)

            if (userExists == True):
                isAdmin = requests.post(f"{self.BASE_URL}/Is_Admin/{Username}").json()["status"]
                data = {"Username": Username, "Password": Password, "isAdmin": isAdmin}
                with open("Credentials.json", "w+") as f:
                    json.dump(data, f)
                self.root.destroy()
                studentDetailsCounsellorScreen.Main(Username,Password).App()
            else:
                tkinter.messagebox.showerror(title="Authentication Error",
                                             message="User not found or incorrect password! Please try again")
        else:
            with open("Credentials.json") as f:
                data = json.load(f)
            Username = data["Username"]
            Password = data["Password"]
            isAdmin = data["isAdmin"]
            userExists = user_authentication.Login(Username, Password)
            if (userExists == True):
                self.root.destroy()
                studentDetailsCounsellorScreen.Main(Username,Password).App()
            else:
                self.Login_Screen()


if __name__ == '__main__':
    App().Login_Screen()
