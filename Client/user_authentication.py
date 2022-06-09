import pyrebase

authConfig = {"apiKey": "AIzaSyCCNce0tYCeQS__R6bKUhY6tG_ZrxPw4Dk",
              "authDomain": "ivyaspire-2a365.firebaseapp.com",
              "projectId": "ivyaspire-2a365",
              "databaseURL": "https://ivyaspire-2a365-default-rtdb.firebaseio.com/",
              "storageBucket": "ivyaspire-2a365.appspot.com",
              "messagingSenderId": "107246567485",
              "appId": "1:107246567485:web:667e3fd33bcd7f26976a54",
              "measurementId": "G-98B467MZDG"}

firebase = pyrebase.initialize_app(authConfig)
auth = firebase.auth()


def Login(emailID, password):
    try:
        auth.sign_in_with_email_and_password(emailID, password)
        return True
    except:
        return False

def create_user(emailID,password):
    print("In here ")
    try:
        auth.create_user_with_email_and_password(emailID,password)
        return True
    except:
        return False

