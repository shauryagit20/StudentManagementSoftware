import json
import os
import tkinter as tk
import tkinter.font
import tkinter.messagebox
from tkinter import ttk
from tkinter import ttk
import webbrowser

import requests
from PIL import Image, ImageTk

import user_authentication

BASE_URL = "http://127.0.0.1:5000/"


class Main:
    def __init__(self, Username, Password):
        self.Username = Username
        self.Password = Password
        self.BASE_URL = "http://127.0.0.1:5000/"
        self.Frame_Details = {}
        self.background1 = "#7600e6"
        self.isAdmin = False
        self.CURRENT_DIR = os.getcwd()

    def fetch_username(self):
        return (requests.get(f"{self.BASE_URL}/getUsername/{self.Username}").json())["value"]

    def checkAdmin(self):
        os.chdir(self.CURRENT_DIR)
        with open("Credentials.json", "r") as f:
            data = json.load(f)
        self.isAdmin = data["isAdmin"]

    def addStudnetScreen(self):
        StudentScreen().main()

    def addCounselorScreen(self):
        # self.root.destroy()
        CounselorScreen(self.Username).main()

    def open_excel(self,link):
        webbrowser.get(using='google-chrome').open(link,2)

    def send_mail(self,mail_id):
        requests.post(f"{BASE_URL}remind/{mail_id}")

    def App(self):
        self.checkAdmin()
        self.root = tk.Tk()
        root = self.root
        root.geometry("1280x900")
        root.config(bg="#FDF7FF")

        print(self.CURRENT_DIR)

        # Title
        bar = tk.Frame(root, height=8)
        bar.pack(fill=tk.X)
        tk.Label(bar, bg=self.background1, height=5).pack(fill=tk.X)

        logo_image = (Image.open("Logo.png"))

        logo_image = logo_image.resize((175, 90), Image.ANTIALIAS)
        logo_image = ImageTk.PhotoImage(logo_image)
        panel = tk.Label(bar, image=logo_image, bg=self.background1)
        panel.image = logo_image
        panel.place(x=-1, y=0)

        username_size = tkinter.font.Font(family='Helvetica', size=15).measure(self.Username)
        print(username_size)

        user_image = (Image.open("Username.png"))
        user_image = user_image.resize((60, 60), Image.ANTIALIAS)
        user_image = ImageTk.PhotoImage(user_image)
        user_image_label = tk.Label(bar, image=user_image, bg=self.background1)
        user_image_label.image = user_image
        user_image_label.place(x=1280 - (username_size + 80), y=10)

        username_label = tk.Label(self.root, text=self.Username, bg=self.background1, font=('Helvetica', 15))
        username_label.place(x=1280 - (username_size + 10), y=40)

        Student_Frame = tk.Frame(root, bg="#FDF7FF", height=110, borderwidth=0, highlightthickness=0)
        Student_Frame.pack(fill=tk.X)
        tk.Label(Student_Frame, text="STUDENTS", bg="#FDF7FF", font=('Helvetica', 35), borderwidth=0,
                 highlightthickness=0).place(x=50, y=50)
        print(Student_Frame)

        main_frame = tk.Frame(root, bg="#FDF7FF", borderwidth=0, highlightthickness=0)
        main_frame.pack(fill=tk.BOTH, expand=1)

        self.my_Canvas = tkinter.Canvas(main_frame, bg="#FDF7FF", borderwidth=0, highlightthickness=0)
        self.my_Canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        style = tkinter.ttk.Style()

        style.element_create("My.Vertical.TScrollbar.trough", "from", "clam")
        style.element_create("My.Vertical.TScrollbar.thumb", "from", "clam")
        style.element_create("My.Vertical.TScrollbar.grip", "from", "clam")

        style.layout("My.Vertical.TScrollbar",
                     [('My.Vertical.TScrollbar.trough',
                       {'children': [('My.Vertical.TScrollbar.thumb',
                                      {'unit': '1',
                                       'children':
                                           [('My.Vertical.TScrollbar.grip', {'sticky': ''})],
                                       'sticky': 'nswe'})
                                     ],
                        'sticky': 'ns'})])

        style.configure("My.Vertical.TScrollbar", gripcount=0, background=self.background1,
                        troughcolor='#FDF7FF', borderwidth=3, bordercolor='#252526',
                        lightcolor='#252526', darkcolor='#252526',
                        arrowsize=25)

        myScrollBar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.my_Canvas.yview,
                                    style="My.Vertical.TScrollbar")
        myScrollBar.pack(side=tk.RIGHT, fill=tk.Y)

        self.my_Canvas.config(yscrollcommand=myScrollBar.set)

        self.my_Canvas.bind('<Configure>', lambda e: self.my_Canvas.configure(scrollregion=self.my_Canvas.bbox("all")))

        self.window_frame = tk.Frame(self.my_Canvas, bg="#FDF7FF")

        self.canvas_frame = self.my_Canvas.create_window((100, 0), window=self.window_frame, anchor="nw")
        list_of_frame = []

        self.window_frame.bind("<Configure>", self.OnFrameConfigure)
        self.my_Canvas.bind('<Configure>', self.FrameWidth)

        counsel_data = requests.get(f"{BASE_URL}fetchData/{self.Username}").json()["Details"]
        print(counsel_data)

        if self.isAdmin == True:
            counselors = list(counsel_data.keys())
            to_break = False
            current_index = 0
            while to_break == False:
                counselorMailId = counselors[current_index]
                print(f"Line 142 : {counselorMailId}")
                CmailId =  counselors[current_index]
                counselorName = counsel_data[counselorMailId]["Counselor Name"]
                studentsList = list(counsel_data[counselorMailId]["Students"].keys())
                list_of_frame  = []
                for ele in range(len(counsel_data[counselorMailId]["Students"])):
                    list_of_frame.append(tk.Frame(self.window_frame))
                    print(list_of_frame)
                    list_of_frame[ele].pack(fill=tk.BOTH, pady=40)
                    list_of_frame[ele].config(bg=self.background1)
                    list_of_frame[ele].config(height=300)
                    list_of_frame[ele].pack_propagate(0)

                    Button_Frame = tk.Frame(list_of_frame[ele])
                    Button_Frame.pack(side=tk.RIGHT, fill=tk.Y)
                    Button_Frame.config(width=400, bg=self.background1)


                    studentMailId = studentsList[ele]


                    StudentName = counsel_data[counselorMailId]["Students"][studentMailId]["studentName"]
                    guardianName = counsel_data[counselorMailId]["Students"][studentMailId]["guardianName"]
                    guardianMail =  counsel_data[counselorMailId]["Students"][studentMailId]["guardianMail"]
                    counselorMailId =  counsel_data[counselorMailId]["Students"][studentMailId]["CounselorMail"]
                    excel_link =  counsel_data[counselorMailId]["Students"][studentMailId]["studentExcel"]

                    Excel_Button = tk.Button(Button_Frame, text="OPEN EXCEL", bg="#9F88B1",
                                             font=('Helvetica', 15, "bold"), height=2, width=15, command=lambda i = excel_link: self.open_excel(i))
                    Excel_Button.pack(padx=30, side=tk.RIGHT)

                    MaunalMail = tk.Button(Button_Frame, text="REMIND", bg="#9F88B1", font=('Helvetica', 15, "bold"),
                                           height=2, width=15,command= lambda i  = studentMailId: self.send_mail(i))
                    MaunalMail.pack(padx=30, side=tk.RIGHT)

                    StudentNameFrame = tk.Frame(list_of_frame[ele], bg=self.background1)
                    StudentNameFrame.pack(fill=tk.X)
                    StudentNameFrame.pack_propagate(0)
                    StudentNameFrame.config(height=80)
                    tk.Label(StudentNameFrame, text=f"{StudentName}", fg="white", bg=self.background1,
                             font=('Helvetica', 30)).pack(side=tk.LEFT, padx=20, pady=20, anchor="n")
                    CounselorNameFrame = tk.Frame(list_of_frame[ele], bg=self.background1,pady=10)
                    CounselorNameFrame.pack(fill =  tk.X)
                    CounselorNameFrame.pack_propagate(0)
                    CounselorNameFrame.config(height=40)
                    tk.Label(CounselorNameFrame, text=f"Assigned Counselor : {counselorName}", fg="white",
                             bg=self.background1, font=('Helvetica', 15)).pack(side=tk.LEFT, padx = 30,
                                                                               anchor="nw")
                    CounselorMailIdFrame = tk.Frame(list_of_frame[ele], bg=self.background1, pady=10)
                    CounselorMailIdFrame.pack(fill=tk.X)
                    CounselorMailIdFrame.pack_propagate(0)
                    CounselorMailIdFrame.config(height=40)

                    tk.Label(CounselorMailIdFrame, text=f"Counselor's Mail id : {CmailId}", fg="white",
                             bg=self.background1, font=('Helvetica', 15)).pack(side=tk.LEFT, padx=30,
                                                                               anchor="nw")
                    GuardianNameFrame = tk.Frame(list_of_frame[ele], bg=self.background1, pady=10)
                    GuardianNameFrame.pack(fill=tk.X)
                    GuardianNameFrame.pack_propagate(0)
                    GuardianNameFrame.config(height=40)
                    tk.Label(GuardianNameFrame, text=f"Guardian Name : {guardianName}", fg="white",
                             bg=self.background1, font=('Helvetica', 15)).pack(side=tk.LEFT, padx=30,
                                                                               anchor="nw")
                    StudentMailIdFrame = tk.Frame(list_of_frame[ele], bg=self.background1, pady=10)
                    StudentMailIdFrame.pack(fill=tk.X)
                    StudentMailIdFrame.pack_propagate(0)
                    StudentMailIdFrame.config(height=40),
                    tk.Label(StudentMailIdFrame, text=f"Student's Mail id : {studentMailId}", fg="white",
                             bg=self.background1, font=('Helvetica', 15)).pack(side=tk.LEFT, padx=30,
                                                                               anchor="nw")
                    GuardianMailIdFrame = tk.Frame(list_of_frame[ele], bg=self.background1, pady=10)
                    GuardianMailIdFrame.pack(fill=tk.X)
                    GuardianNameFrame.pack_propagate(0)
                    GuardianMailIdFrame.config(height=40)
                    tk.Label(GuardianMailIdFrame, text=f"Guardian's Mail id : {guardianMail}", fg="white",
                             bg=self.background1, font=('Helvetica', 15)).pack(side=tk.LEFT, padx=30,
                                                                               anchor="nw")

                    EmailButton =  tk.Button()

                current_index =  current_index+1
                if(current_index ==  len(counselors)):
                    to_break = True
        else:
            ele = 0
            print(counsel_data.keys())
            counselorName =  counsel_data[self.Username]["Counselor Name"]

            for studentMailId in counsel_data[self.Username]["Students"]:
                list_of_frame.append(tk.Frame(self.window_frame))
                list_of_frame[ele].pack(fill=tk.BOTH, pady=40)
                list_of_frame[ele].config(bg=self.background1)
                list_of_frame[ele].config(height=300)
                list_of_frame[ele].pack_propagate(0)

                Button_Frame = tk.Frame(list_of_frame[ele])
                Button_Frame.pack(side=tk.RIGHT, fill=tk.Y)
                Button_Frame.config(width=400, bg=self.background1)


                StudentName = counsel_data[self.Username]["Students"][studentMailId]["studentName"]
                guardianName = counsel_data[self.Username]["Students"][studentMailId]["guardianName"]
                guardianMail = counsel_data[self.Username]["Students"][studentMailId]["guardianMail"]
                counselorMailId = counsel_data[self.Username]["Students"][studentMailId]["CounselorMail"]
                excel_link = counsel_data[counselorMailId]["Students"][studentMailId]["studentExcel"]

                Excel_Button = tk.Button(Button_Frame, text="OPEN EXCEL", bg="#9F88B1",
                                         font=('Helvetica', 15, "bold"), height=2, width=15,
                                         command=lambda i=excel_link: self.open_excel(i))
                Excel_Button.pack(padx=30, side=tk.RIGHT)

                MaunalMail = tk.Button(Button_Frame, text="REMIND", bg="#9F88B1", font=('Helvetica', 15, "bold"),
                                       height=2, width=15, command=lambda i=studentMailId: self.send_mail(i))
                MaunalMail.pack(padx=30, side=tk.RIGHT)

                StudentNameFrame = tk.Frame(list_of_frame[ele], bg=self.background1)
                StudentNameFrame.pack(fill=tk.X)
                StudentNameFrame.pack_propagate(0)
                StudentNameFrame.config(height=80)
                tk.Label(StudentNameFrame, text=f"{StudentName}", fg="white", bg=self.background1,
                         font=('Helvetica', 30)).pack(side=tk.LEFT, padx=20, pady=20, anchor="n")
                CounselorNameFrame = tk.Frame(list_of_frame[ele], bg=self.background1, pady=10)
                CounselorNameFrame.pack(fill=tk.X)
                CounselorNameFrame.pack_propagate(0)
                CounselorNameFrame.config(height=40)
                tk.Label(CounselorNameFrame, text=f"Assigned Counselor : {counselorName}", fg="white",
                         bg=self.background1, font=('Helvetica', 15)).pack(side=tk.LEFT, padx=30,
                                                                           anchor="nw")
                CounselorMailIdFrame = tk.Frame(list_of_frame[ele], bg=self.background1, pady=10)
                CounselorMailIdFrame.pack(fill=tk.X)
                CounselorMailIdFrame.pack_propagate(0)
                CounselorMailIdFrame.config(height=40)

                tk.Label(CounselorMailIdFrame, text=f"Counselor's Mail id : {self.Username}", fg="white",
                         bg=self.background1, font=('Helvetica', 15)).pack(side=tk.LEFT, padx=30,
                                                                           anchor="nw")
                GuardianNameFrame = tk.Frame(list_of_frame[ele], bg=self.background1, pady=10)
                GuardianNameFrame.pack(fill=tk.X)
                GuardianNameFrame.pack_propagate(0)
                GuardianNameFrame.config(height=40)
                tk.Label(GuardianNameFrame, text=f"Guardian Name : {guardianName}", fg="white",
                         bg=self.background1, font=('Helvetica', 15)).pack(side=tk.LEFT, padx=30,
                                                                           anchor="nw")
                StudentMailIdFrame = tk.Frame(list_of_frame[ele], bg=self.background1, pady=10)
                StudentMailIdFrame.pack(fill=tk.X)
                StudentMailIdFrame.pack_propagate(0)
                StudentMailIdFrame.config(height=40),
                tk.Label(StudentMailIdFrame, text=f"Student's Mail id : {studentMailId}", fg="white",
                         bg=self.background1, font=('Helvetica', 15)).pack(side=tk.LEFT, padx=30,
                                                                           anchor="nw")
                GuardianMailIdFrame = tk.Frame(list_of_frame[ele], bg=self.background1, pady=10)
                GuardianMailIdFrame.pack(fill=tk.X)
                GuardianNameFrame.pack_propagate(0)
                GuardianMailIdFrame.config(height=40)
                tk.Label(GuardianMailIdFrame, text=f"Guardian's Mail id : {guardianMail}", fg="white",
                         bg=self.background1, font=('Helvetica', 15)).pack(side=tk.LEFT, padx=30,
                                                                           anchor="nw")

                list_of_frame = []

        if self.isAdmin == True:

            footerFrame = tk.Frame(root, height=90, bg="#FDF7FF")
            footerFrame.pack(fill=tk.X)
            addCounselor = tk.Button(footerFrame, bg="#9F88B1", text="ADD COUNSELOR", width=18, height=2,
                                     font=('Helvetica', 15, "bold"), command=lambda: self.addCounselorScreen())
            addCounselor.pack(side=tk.RIGHT, pady=10)
            addStudent = tk.Button(footerFrame, bg="#9F88B1", text="ADD STUDENT", width=20, height=2,
                                   font=('Helvetica', 15, "bold"), command=lambda: self.addStudnetScreen())
            addStudent.pack(side=tk.RIGHT, pady=10, padx=5)

        root.mainloop()


    def FrameWidth(self, event):
        canvas_width = event.width - 200

        self.my_Canvas.itemconfig(self.canvas_frame, width=canvas_width)

    def OnFrameConfigure(self, event):
        self.my_Canvas.configure(scrollregion=self.my_Canvas.bbox("all"))


class CounselorScreen:
    def __init__(self, Username):
        self.background1 = "#7600E6"
        self.Username = Username

    def main(self):
        Username = self.Username

        self.root = tk.Toplevel()

        self.LoginId = tk.StringVar()
        self.CounselorName = tk.StringVar()
        self.Password = tk.StringVar()
        self.ConfirmPassword = tk.StringVar()
        self.isAdmin = tk.IntVar()

        root = self.root
        root.geometry("1280x900")
        root.config(bg="#FDF7FF")
        bar = tk.Frame(root, height=8)
        bar.pack(fill=tk.X)
        tk.Label(bar, bg=self.background1, height=5).pack(fill=tk.X)

        logo_image_s1 = (Image.open("Logo1.png"))

        logo_image_s1 = logo_image_s1.resize((175, 90), Image.ANTIALIAS)
        logo_image_s1 = ImageTk.PhotoImage(logo_image_s1)
        panel = tk.Label(bar, image=logo_image_s1, bg=self.background1)
        panel.image = logo_image_s1
        panel.place(x=-1, y=0)

        username_size = tkinter.font.Font(family='Helvetica', size=15).measure(self.Username)
        print(username_size)

        user_image = (Image.open("Username.png"))
        user_image = user_image.resize((60, 60), Image.ANTIALIAS)
        user_image = ImageTk.PhotoImage(user_image)
        user_image_label = tk.Label(bar, image=user_image, bg=self.background1)
        user_image_label.image = user_image
        user_image_label.place(x=1280 - (username_size + 80), y=10)

        username_label = tk.Label(self.root, text=self.Username, bg=self.background1, font=('Helvetica', 15))
        username_label.place(x=1280 - (username_size + 10), y=40)

        Label_Frame = tk.Frame(root, height=10, bg="#FDF7FF")
        Label_Frame.pack(fill=tk.X, padx=10, pady=30)
        tk.Label(Label_Frame, text="ADD NEW LOGIN", font=('Helvetica', 25, "bold"), bg="#FDF7FF").pack(pady=2, padx=10)

        form_frame = tk.Frame(root, bg="#FDF7FF")
        form_frame.pack(pady=90)
        tk.Label(form_frame, text="EMAIL ID :  ", font=("Helvetica", 20, "bold"), bg="#FDF7FF").place(x=190, y=20)
        tk.Entry(form_frame, textvariable=self.LoginId, bg="white").grid(row=0, column=1, pady=20, ipady=3, ipadx=20)

        tk.Label(form_frame, text="COUNSELLOR'S NAME : ", font=("Helvetica", 20, "bold"), bg="white").grid(row=1,
                                                                                                           column=0,
                                                                                                           padx=10,
                                                                                                           pady=20)
        tk.Entry(form_frame, textvariable=self.CounselorName, bg="#FDF7FF").grid(row=1, column=1, pady=20, ipady=3,
                                                                                 ipadx=20)

        tk.Label(form_frame, text="PASSWORD :  ", font=("Helvetica", 20, "bold"), bg="#FDF7FF").place(x=148, y=160)
        tk.Entry(form_frame, textvariable=self.Password, bg="white").grid(row=2, column=1, pady=20, ipady=3, ipadx=20)

        tk.Label(form_frame, text="CONFIRM PASSWORD :  ", font=("Helvetica", 20, "bold"), bg="#FDF7FF").place(x=18,
                                                                                                              y=230)
        tk.Entry(form_frame, textvariable=self.ConfirmPassword, bg="white").grid(row=3, column=1, pady=20, ipady=3,
                                                                                 ipadx=20)

        tk.Checkbutton(form_frame, text="Is Admin?", bg="#FDF7FF", font=("Helvetica", 20, "bold"),
                       variable=self.isAdmin, onvalue=1, offvalue=0, height=2, width=10).grid(row=4, column=0)

        tk.Button(root, text="ADD LOGIN", bg="green", height=2, width=20, font=("Helvetica", 15, "bold"),
                  command=lambda: self.addLogin()).place(x=530, y=660)

    def addLogin(self):
        if (self.ConfirmPassword.get() != self.Password.get()):
            tkinter.messagebox.showerror(title="Error", message="Passwords do not match")
            self.ConfirmPassword.set("")
            self.Password.set("")

        if (len(self.Password.get()) > 0 and len(self.ConfirmPassword.get()) > 0 and len(
                self.CounselorName.get()) > 0 and len(self.LoginId.get()) > 0):

            res = user_authentication.create_user(emailID=self.LoginId.get(), password=self.Password.get())

            Username = str(self.CounselorName.get())
            LoginId = str(self.LoginId.get())

            if (res == True):
                print("HERE")
                if (self.isAdmin.get() == 1):
                    status = requests.post(f"{BASE_URL}addCounselor/{Username}/{LoginId}/True")
                    tkinter.messagebox.showinfo(title="USER CREATED", message="The user has been created")
                    self.root.destroy()
                else:
                    status = requests.post(f"{BASE_URL}addCounselor/{Username}/{LoginId}/False")
                    tkinter.messagebox.showinfo(title="USER CREATED", message="The user has been created")
                    self.root.destroy()
            else:
                tkinter.messagebox.showerror(title="Error", message="The user creation process was not successful")
                self.root.destroy()
        else:
            tkinter.messagebox.showerror(title="Error", message="Please fill all the fields")


class StudentScreen:
    def __init__(self):
        self.background1 = "#7600E6"

    def main(self):
        self.root = tk.Toplevel()
        root = self.root
        root.geometry("1280x900")
        root.config(bg="white")
        self.Username = "robotics.shauryas@gmail.com"

        Username = self.Username

        self.root = tk.Toplevel()

        self.StudentName = tk.StringVar()
        self.CounselorMail = tk.StringVar()
        self.GuardianName = tk.StringVar()
        self.StudentMailId = tk.StringVar()
        self.GuardianMailId = tk.StringVar()
        self.Excel = tk.StringVar()

        root = self.root
        root.geometry("1280x900")
        root.config(bg="#FDF7FF")
        bar = tk.Frame(root, height=8)
        bar.pack(fill=tk.X)
        tk.Label(bar, bg=self.background1, height=5).pack(fill=tk.X)

        logo_image_s1 = (Image.open("Logo1.png"))

        logo_image_s1 = logo_image_s1.resize((175, 90), Image.ANTIALIAS)
        logo_image_s1 = ImageTk.PhotoImage(logo_image_s1)
        panel = tk.Label(bar, image=logo_image_s1, bg=self.background1)
        panel.image = logo_image_s1
        panel.place(x=-1, y=0)

        username_size = tkinter.font.Font(family='Helvetica', size=15).measure(self.Username)
        print(username_size)

        user_image = (Image.open("Username.png"))
        user_image = user_image.resize((60, 60), Image.ANTIALIAS)
        user_image = ImageTk.PhotoImage(user_image)
        user_image_label = tk.Label(bar, image=user_image, bg=self.background1)
        user_image_label.image = user_image
        user_image_label.place(x=1280 - (username_size + 80), y=10)

        username_label = tk.Label(self.root, text=self.Username, bg=self.background1, font=('Helvetica', 15))
        username_label.place(x=1280 - (username_size + 10), y=40)

        Label_Frame = tk.Frame(root, height=10, bg="#FDF7FF")
        Label_Frame.pack(fill=tk.X, padx=10, pady=30)
        tk.Label(Label_Frame, text="ADD NEW STUDENT", font=('Helvetica', 25, "bold"), bg="#FDF7FF").pack(pady=2,
                                                                                                         padx=10)

        form_frame = tk.Frame(root, bg="#FDF7FF")
        form_frame.pack(pady=50)
        tk.Label(form_frame, text="STUDENT NAME :  ", font=("Helvetica", 20, "bold"), bg="#FDF7FF").place(x=64, y=20)
        tk.Entry(form_frame, textvariable=self.StudentName, bg="white").grid(row=0, column=1, pady=20, ipady=3,
                                                                             ipadx=20)

        tk.Label(form_frame, text="COUNSELOR'S MAIL : ", font=("Helvetica", 20, "bold"), bg="white").grid(row=1,
                                                                                                          column=0,
                                                                                                          padx=10,
                                                                                                          pady=20)
        tk.Entry(form_frame, textvariable=self.CounselorMail, bg="#FDF7FF").grid(row=1, column=1, pady=20, ipady=3,
                                                                                 ipadx=20)

        tk.Label(form_frame, text="GUARDIAN NAME :  ", font=("Helvetica", 20, "bold"), bg="#FDF7FF").place(x=57, y=160)
        tk.Entry(form_frame, textvariable=self.GuardianName, bg="white").grid(row=2, column=1, pady=20, ipady=3,
                                                                              ipadx=20)

        tk.Label(form_frame, text="STUDENT MAIL ID :  ", font=("Helvetica", 20, "bold"), bg="#FDF7FF").place(x=45,
                                                                                                             y=230)
        tk.Entry(form_frame, textvariable=self.StudentMailId, bg="white").grid(row=3, column=1, pady=20, ipady=3,
                                                                               ipadx=20)

        tk.Label(form_frame, text="GUARDIAN MAIL ID :  ", font=("Helvetica", 20, "bold"), bg="#FDF7FF").place(x=30,
                                                                                                              y=300)
        tk.Entry(form_frame, textvariable=self.GuardianMailId, bg="white").grid(row=4, column=1, pady=20, ipady=3,
                                                                                ipadx=20)

        tk.Label(root, text="LINK TO EXCEL SHEET :  ", font=("Helvetica", 20, "bold"), bg="#FDF7FF").place(x=355,
                                                                                                           y=610)
        tk.Entry(form_frame, textvariable=self.Excel, bg="white").grid(row=5, column=1, pady=20, ipady=3,
                                                                       ipadx=20)

        tk.Button(root, text="ADD STUDENT", bg="#9F88B1", height=2, width=20, font=("Helvetica", 15, "bold"),
                  command=lambda: self.addLogin()).place(x=530, y=720)

    def addLogin(self):
        if (len(self.StudentName.get()) > 0 and len(self.StudentMailId.get()) > 0 and len(
                self.CounselorMail.get()) > 0 and len(self.GuardianName.get()) > 0 and len(
            self.GuardianMailId.get()) > 0
                and len(self.Excel.get()) > 0):
            l = "-".join(self.Excel.get().split("/"))
            status = requests.post(
                f"{BASE_URL}addStudent/{self.StudentName.get()}/{self.CounselorMail.get()}/{self.GuardianName.get()}/{self.StudentMailId.get()}/{self.GuardianMailId.get()}/{l}").json()
            print(status)
            print(type(status["Status"]))
            if (status["Status"] == True):
                print("True")
                tkinter.messagebox.showinfo(title="Student Added", message="The student has been added")
                self.root.destroy()

            else:
                tkinter.messagebox.showerror(title="ERROR", message="Could not add the student")
        else:
            tkinter.messagebox.showerror(title="ERROR", message="Error")


# Main("robotics.shaurya@gmail.com", "Tower@11").App()
# khushisingh70951@gmail.com
