import json

from flask import Flask
import smtplib
import pprint
import threading
import datetime

import gspread
from dateutil import parser
from oauth2client.service_account import ServiceAccountCredentials

from email.message import EmailMessage
from flask_restful import Api, Resource

import gspread

app = Flask(__name__)
api = Api(app)


class Is_Admin(Resource):
    def post(self, Username):
        with open("Admins.json", "r+") as f:
            data = json.load(f)
        print(data)
        if Username in data["Admins"]:
            return {"status": True}
        else:
            return {"status": False}


class Create_Admin(Resource):
    def post(self, Username):
        with open("Admins.json", "r+") as f:
            data = json.load(f)
        data["Admins"].append(Username)
        with open("Admins.json", "w") as f:
            json.dump(data, f)


class Remove_Admin(Resource):
    def post(self, Username):
        with open("Admins.json", "r+") as f:
            data = json.load(f)
        try:
            data["Admins"].remove(Username)
            with open("Admins.json", "w") as f:
                json.dump(data, f)
            return {"Status": "Success"}
        except:
            return {"Status": "Username does not exit"}


class List_Admin(Resource):
    def post(self):
        with open("Admins.json", "r+") as f:
            data = json.load(f)

        return {"Admins": data["Admins"]}


class addCounselor(Resource):
    def post(self, Counselor_Name, Email_Id, isAdmin):
        CounselorDict = {"Counselor Name": Counselor_Name, "Students": {}}
        if (isAdmin == "True"):
            with open("Counselor_Details.json", "r+") as f:
                data = json.load(f)
            data[Email_Id] = CounselorDict
            with open("Counselor_Details.json", "w") as f:
                json.dump(data, f)
            Create_Admin().post(Email_Id)
            return {"Status": True}
        else:
            with open("Counselor_Details.json", "r+") as f:
                data = json.load(f)
            data[Email_Id] = CounselorDict
            with open("Counselor_Details.json", "w") as f:
                json.dump(data, f)
            return {"Status": True}


class addStudent(Resource):
    def post(self, StudentName, CounselorMail, GuardianName, StudentMail, GuardianMail, StudentExcel):
        l =  list(StudentExcel)

        for index in range(len(l)):
            if(l[index] ==  "-"):
                l[index] =  "/"

        StudentExcel = "".join(l)

        with open("Counselor_Details.json", "r+") as f:
            data = json.load(f)


        studentdict = {"studentMailId": StudentMail, "studentName": StudentName, "CounselorMail": CounselorMail,
                       "guardianName": GuardianName, "guardianMail": GuardianMail, "studentExcel": StudentExcel}
        d = {StudentMail: studentdict}
        try:
            data[CounselorMail]["Students"][StudentMail] = studentdict
        except:
            return {"Status": False}

        with open("Counselor_Details.json", "w+") as f:
            json.dump(data, f)
        return {"Status": True}

class fetch_data(Resource):
    def get(self,CounselorMailId):
        isAdmin =  False
        with open("Admins.json", "r+") as f:
            data = json.load(f)
        print(data)
        if CounselorMailId in data["Admins"]:
            isAdmin =  True

        else:
            isAdmin =  False

        with open("Counselor_Details.json") as f:
            data =  json.load(f)

        if(isAdmin == True):
            return {"Details":data}
        else:
            return {"Details":data}

class remind(Resource):
    def post(self,StudentMailid):
        msg = EmailMessage()
        msg.set_content('Reminder for you to complete your tasks!')

        msg['Subject'] = 'REMINDER!'
        msg['From'] = "ivyaspire.reminder@gmail.com"
        msg['To'] = StudentMailid
        s =  smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(user="ivyaspire.reminder@gmail.com",password="ivyaspire@#$123$#@")
        s.send_message(msg)

class scheculer():
    def schedule(self):
        executed =  False
        while True:
            todays_date = datetime.datetime.now()
            if(datetime.datetime.now().hour == 15 and executed == False):
                scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
                         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
                cred =  ServiceAccountCredentials.from_json_keyfile_name("credentials.json",scope)
                gs =  gspread.authorize(cred)
                with open("Counselor_Details.json","r+") as f:
                    counselor_data = json.load(f)
                for counselors in counselor_data:
                    for studentMail in counselor_data[counselors]["Students"]:
                        sheet_url = counselor_data[counselors]["Students"][studentMail]["studentExcel"]
                        guardianMail =  counselor_data[counselors]["Students"][studentMail]["guardianMail"]
                        CounselorMail =  counselor_data[counselors]["Students"][studentMail]["CounselorMail"]
                        spreadsheet = gs.open_by_url(sheet_url)
                        ws =  spreadsheet.worksheet("Tasks")
                        tasks_data =  ws.get_all_values()
                        print(tasks_data)
                        for i in range(len(tasks_data)):
                            task_name =  tasks_data[i][0]
                            deadline =  parser.parse(tasks_data[i][1])
                            checkbox_value =  tasks_data[i][2]
                            deadline_day =  deadline.date().day
                            todays_day =  todays_date.day
                            rem =  deadline_day -  todays_day
                            if(rem == 0 and checkbox_value == "FALSE"):
                                content =  f"PLEASE COMPLETE YOUR TASKS OF {task_name} AS SOON AS POSSIBLE. TODAY IS THE DEADLINE"
                                # mailing_list =  [studentMail,guardianMail,CounselorMail]
                                mailing_list = [studentMail, guardianMail]
                                self.send_mail(mailing_list,content )
                            if(rem ==  1 and checkbox_value == "FALSE"):
                                content =  f"Please complete your task OF {task_name} as soon as possible. TOMORROW is the deadline"
                                # mailing_list =  [studentMail,guardianMail,CounselorMail]
                                mailing_list =  [studentMail,guardianMail]
                                self.send_mail(mailing_list,content)
                            if(rem ==  3 and checkbox_value == "FALSE"):
                                content = f"DEADLINE APPROACHING SOON (within 3 days). Please complete {task_name} as soon as possible"
                                # mailing_list = [studentMail,CounselorMail]
                                mailing_list =  [studentMail]
                                self.send_mail(mailing_list,content)
                            if(rem == 5 and checkbox_value == "FALSE"):
                                content =  f"DEADLINE APPROACHING SOON (within 5 days). Please complete {task_name} as soon as possible "
                                # mailing_list = [studentMail,CounselorMail]
                                mailing_list =  [studentMail]
                                self.send_mail(mailing_list, content)


                executed =  True

            if(datetime.datetime.now().hour == 10):
                executed = True


    def send_mail(self,receivers,content):
        msg = EmailMessage()
        msg.set_content(content)

        msg['Subject'] = 'REMINDER!'
        msg['From'] = "robotics.shaurya@gmail.com"
        msg['To'] =  ", ".join(receivers)
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(user="ivyaspire.reminder@gmail.com", password="ivyaspire@#$123$#@")
        s.send_message(msg)

#
#
api.add_resource(Is_Admin, "/Is_Admin/<string:Username>")
api.add_resource(Create_Admin, "/Create_Admin/<string:Username>")
api.add_resource(Remove_Admin, "/Remove_Admin/<string:Username>")
api.add_resource(List_Admin, "/List_Admin/")
api.add_resource(addCounselor, "/addCounselor/<string:Counselor_Name>/<string:Email_Id>/<string:isAdmin>")
api.add_resource(addStudent,"/addStudent/<string:StudentName>/<string:CounselorMail>/<string:GuardianName>/<string:StudentMail>/<string:GuardianMail>/<string:StudentExcel>")
api.add_resource(fetch_data,"/fetchData/<string:CounselorMailId>")
api.add_resource(remind,"/remind/<string:StudentMailid>")
#
if __name__ == "__main__":
    threading.Thread(target=scheculer().schedule).start()
    app.run(debug=True)
#
# scheculer().send_mail(["directme.competitions@gmail.com"],"Test Email")
