# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 22:06:05 2021

@author: bashirf
"""

import socket
from _thread import *
from random import randint #Not gonna use this
import mysql.connector #Database Connector

#Info for database user
mydb = mysql.connector.connect(
  host="localhost",
  user="fadlbashir",
  password="fadlbashir",            
  port = 3307,
  database = "mydatabase"
)

#Cursor used to execute sql queries
mycursor = mydb.cursor()  

#Socket cnnection statements
ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 1251 #PORT NUMBER HAS TO BE THE SAME AS THE ONE IN THE CLIENT SIDE
ThreadCount = 0
ServerSocket.bind(('', port))

#Open file for writing (probably not gonna use it)
file = open("messagesFile", "w")
file.write("0")
file.close()

#Just a print statement showing that the server is still waiting for a connection
print('Waitiing for a Connection..')

#Listen to connections (5)
ServerSocket.listen(5)

def encrypt(message):
    """
    Parameters
    ----------
    message : String

    Returns
    -------
    encrypt : Encrypted String

    """
    alphabet = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM123456789'
    key = 5
    encrypt=''
    decrypt=''
    for i in message:
        position = alphabet.find(i)
        newposition = (position + 5) %61
        encrypt += alphabet[newposition]
    return encrypt

def decrypt(message): 
    """
    Parameters
    ----------
    message : Encrypted String

    Returns
    -------
    decrypt : Decrypted String

    """
    alphabet = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM123456789'
    key = 5
    encrypt=''
    decrypt=''
    for i in message:
        if i.isalnum():
            position = alphabet.find(i)
            newposition = (position - 5) %61
            decrypt += alphabet[newposition] 
        else:
            decrypt += i
    return decrypt
    
# Thread method declaration
def threaded_client(connection, num):
    """
    Parameters
    ----------
    connection : Client socket connection. 
    num : Passed as a tuple including the number of threads as well as the client connection

    Returns
    -------
    None.

    """
    #This connection.send statement sends the welcome message to the client
    connection.send(str.encode("Welcome to our database management system!\n Click Start to proceed?"))
    #Receive first client reply, weather they have an account or no
    clientReplyMessage = connection.recv(1024).decode()
    print(clientReplyMessage)
    
    while True:
        #Try except block to handle the sql error if the username is not in our database
        try:
            mycursor.execute("SELECT PASSWORDS,WEBSITES FROM mydatabase." + str(clientReplyMessage) + ";") #SQL query too get the stored passwords with the given username
            myresult = mycursor.fetchall() #Fetch the records 
            result = "" #Just a string variable to store the stuff we get from the database
            connection.send(str.encode("Your username was found in our database.")) #Print that the username was found
            print("Your username was found in our database.") #Print that the username was found
            #For loop to format the data received from the database
            for x in str(myresult):
                if x.isalnum() or x == "(" or x == ")" or x == ",":
                    if x == ",":
                        x = "    "  # 4 spaces
                    if x == ")":
                        x += "\n"
                    result += x
            result = (decrypt(result)) 
            #If no records are stored, send a message to the user letting them know 
            if result == "(  )":
                result = "No passwords stored."
            else:    
                result = result
            connection.send(str.encode(result.translate({ord('9'): None})))    
            #Ask the user to store more passwords if the want
            connection.send(str.encode("Store more passwords?"))
            newPass = connection.recv(1024).decode()
            newWeb = connection.recv(1024).decode()
            #Make sure all the data received from the user is not empty (new password and website)
            if newPass != "" or newWeb != "":
                newPass = encrypt(newPass)
                newWeb = encrypt(newWeb)
                sql = "INSERT INTO mydatabase." +str(clientReplyMessage)+ " (PIN,PASSWORDS,WEBSITES) VALUES (%s,%s,%s)"
                val = ('',str(newPass),str(newWeb))
                mycursor.execute(sql, val)
                mydb.commit()
                connection.send(str.encode('New password and website inserted!'))
            break;
        except mysql.connector.Error:  #If the username ws not found in our database
            print("Database not found")
            connection.send(str.encode("Your username was not found in our database.")) #Let the user know
            newUser = connection.recv(1024).decode() 
            newPin = connection.recv(1024).decode()
            #Sql statement to create a new user
            mycursor.execute("CREATE TABLE " + str(newUser) + " (PIN VARCHAR(5) , PASSWORDS VARCHAR(30), WEBSITES VARCHAR(30));")
            sql = "INSERT INTO mydatabase." +str(newUser)+ " (PIN,PASSWORDS,WEBSITES) VALUES (%s,%s,%s)" #Insert the pin into the tabel
            val = (str(newPin),'','')
            mycursor.execute(sql, val)
            mydb.commit()
            break;
            connection.close()
    connection.close()
   
    
# Primary while loop
while True:
    Client, address = ServerSocket.accept()  # accept new client
    print('Connected to: ' + address[0] + ':' + str(address[1]))  # print client address
    start_new_thread(threaded_client, (Client, ThreadCount,))  # create new thread with client connection and id
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))    