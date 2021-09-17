"""
Created on Sat Mar 27 18:30:58 2021

@author: bashirf
"""

from tkinter import *
from tkinter import messagebox
import socket
import webbrowser

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect ((socket.gethostname(),1251)) #CLIENT SIDE PORT NUMBER

helloMessage = s.recv(1024) #get the first message from server (welcome message)

def OpenUrl(): #Not really a main part of the project, thought it was a cool thing to add at the end
    url = 'http://www.netflix.com/login' 
    webbrowser.open_new(url)              

#front end tkinter function    
def enterInfo():
    def getTextInput():#function to ask the user to enter their username/password
        usernameInput=usernameText.get("1.0","end")
        pinInput = pinText.get("1.0","end")
        print(usernameInput)
        s.send(str.encode(usernameInput))
        #print(pinInput)
        dataFromServer = s.recv(1024)
        #s.send("Thanks")
        if dataFromServer.decode() == "Your username was found in our database.":
            passwordsAndWebsites = s.recv(1024)
            passwordDsiplayMessage = Label(root, text = "Stored passwords:")
            passwordDsiplayMessage.grid(row = 5, column = 0)
            passWeb = Label(root, text = "Password    Website:")
            passWeb.grid(row = 6, column = 0)
            passwords = Label(root, text = str(passwordsAndWebsites.decode()))
            passwords.grid(row = 7, column = 0)
            if "netflix" in passwordsAndWebsites.decode():
                web = Button(root, text="Netflix?", command=OpenUrl)
                web.grid(row = 7, column = 1)
            questionMessage = s.recv(1024)
            #print(questionMessage.decode())
            doYouWantToStore = Label(root, text = str(questionMessage.decode()))
            doYouWantToStore.grid(row = 8, column = 0, padx = 20,pady=10)
            morePass = Text(root, height = 1, width = 15)
            morePass.grid(row = 9, column = 1, padx = 20,pady=10)
            # morePass.configure(root, padx = 20,pady=10)
            moreWeb = Text(root, height = 1, width = 15)
            moreWeb.grid(row = 10, column = 1)
            usernameLabel = Label(root, text = "Password:")
            pinLabel = Label(root, text = "Website:")
            usernameLabel.grid(row = 9, column = 0)  
            pinLabel.grid(row = 10, column = 0)
            def morePassAndWeb(): #if the user wants to add more passwords, this functioon gets called
                morePassIn=morePass.get("1.0","end")
                moreWebIn = moreWeb.get("1.0","end")
                print(morePassIn)
                print(moreWebIn)
                s.send(str.encode(morePassIn))
                s.send(str.encode(moreWebIn))
                confirmation = s.recv(1024)
                confLabel = Label(root, text = confirmation.decode())
                confLabel.grid(row = 13, column = 0)   
            grabMore = Button(root, text = "Submit", command = morePassAndWeb)
            grabMore.grid(row = 12, column = 1, padx = 20,pady=10)
        else:
            def createUser(): #If the username is not found in the database, this function gets called to create a new username and password (account)
                newUser=createUserT.get("1.0","end")
                newPin = createPin.get("1.0","end")
                s.send(str.encode(newUser))
                s.send(str.encode(newPin))
                createdSuccesfully = Label(root, text = "User Created Succesfully!")
                createdSuccesfully.grid(row = 13, column = 0)  
            notFound = Label(root, text = dataFromServer.decode())
            notFound.grid(row = 6, column = 0)
            notFound = Label(root, text = "Create user:")
            notFound.grid(row = 7, column = 0)
            createUserT = Text(root, height = 1, width = 15)
            createUserT.grid(row = 10, column = 1)
            createPin = Text(root, height = 1, width = 15)
            createPin.grid(row = 11, column = 1)
            usernameLabel = Label(root, text = "Username:")
            pinLabel = Label(root, text = "PIN:")
            usernameLabel.grid(row = 10, column = 0)  
            pinLabel.grid(row = 11, column = 0)
            createUserB = Button(root, text = "Create User", command = createUser)
            createUserB.grid(row = 12, column = 1, padx = 20,pady=10)
            
    root = Tk()
    label = Label(root, text = "Enter Info:")
    label.grid(row = 1, column = 0, padx = 20,pady=10)
    username = Label(root, text = "Username:")
    pin = Label(root, text = "PIN:")
    username.grid(row = 2, column = 0)  
    pin.grid(row = 3, column = 0)
    usernameText = Text(root, height = 1, width = 15)
    usernameText.grid(row = 2, column = 1, padx = 20,pady=10)
    pinText = Text(root, height = 1, width = 15)
    pinText.grid(row = 3, column = 1, padx = 20,pady=10)
    grabData = Button(root, text = "Submit", command = getTextInput)
    grabData.grid(row = 4, column = 1, padx = 20,pady=10)
    root.mainloop()
        
root = Tk()
root.title("PassSaver")
label = Label(root, text = helloMessage)
label.grid(row= 0 , column = 0, padx = 20,pady=10)
yesButton = Button(root, text ="Start", command = enterInfo) #Calls enterInfo function when the button is pressed
yesButton.grid(row = 1, column = 0, padx = 20,pady=10)

root.mainloop()