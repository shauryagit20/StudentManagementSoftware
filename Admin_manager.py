import requests
BASE_URL =  "http://127.0.0.1:5000/"

option =  int(input("Please select the option which you want to perform\n 1) New Admin \n 2) Remove Admin \n 3) List Admins \n : "))
if(option ==  1):
    username = input("Enter the username:  ")
    requests.post(f"{BASE_URL}/Create_Admin/{username}")
elif(option ==  2):
    username =  input("Enter the username:  ")
    Status  =  requests.post(f"{BASE_URL}/Remove_Admin/{username}").json()
    print(Status["Status"])
elif(option ==  3):
    data =  requests.post(f"{BASE_URL}/List_Admin/").json()
    print(data["Admins"])