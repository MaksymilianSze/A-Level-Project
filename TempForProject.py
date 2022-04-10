import tkinter as tk    

from tkinter import messagebox

import hashlib

import secrets

import tkcalendar

import tkinter.ttk as ttk

import datetime

import smtplib, ssl

from email.mime.text import MIMEText

from email.mime.multipart import MIMEMultipart

import mysql.connector as mysql

import matplotlib

class FrameHolder(tk.Tk): #Inherits from Tk

    def __init__(self, *args, **kwargs): #This is the constructor method which allows for any amount of paremeters 
        tk.Tk.__init__(self, *args, **kwargs) #Inherits from tk.Tk, essentially the same as super().__init__()
        self.SharedData = {
          "UsernameHolder": tk.StringVar()
        }


        container = tk.Frame(self) #This creates a frame widget will be used to contain all the pages which will be stacked on top of each other
        container.pack(expand=True) #Packs the container frame which wil expand when resized
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1) #Spreads the weight of the columns out evenly

        self.frames = {} #Create empty dictionary

        self.frames["LoginFrame"] = LoginFrame(parent=container, controller=self) #Create the frames
        self.frames["RegisterFrame"] = RegisterFrame(parent=container, controller=self)
   

        self.frames["LoginFrame"].grid(row=0, column=0, sticky="NESW") #Place them 
        self.frames["RegisterFrame"].grid(row=0, column=0, sticky="NESW")

        self.ShowFrame("LoginFrame") #Login frame is meant to be the first frame to be show

    def ShowFrame(self, FrameName):
        frame = self.frames[FrameName] #Sets frame to be the frame to switch to
        frame.tkraise() #Brings the desired frame to the top

    def RegisterHashPassword(self, Password):
        Salt = secrets.token_hex(8) #Generate Salt
        h = hashlib.sha256() #Set hashing algorithm to use
        SaltedPassword = Password + Salt #Concatenate password and salt
        h.update(SaltedPassword.encode("utf8")) #Enode the combined password and salt string with utf8 then run it throught the hashing algorithm
        Hashed = h.hexdigest() #Assign it to a variable
        return Hashed, Salt

    def LoginHashPassword(self, Password, Salt): #Here the salt is passed in as a parameter
        SaltedPassword = Password + Salt
        h = hashlib.sha256()
        h.update(SaltedPassword.encode("utf8"))
        Hashed = h.hexdigest()
        return Hashed
        

class LoginFrame(tk.Frame, FrameHolder):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        

        self.SelectionRadio = tk.StringVar()

        self.TypeTicked = ""


        self.WelcomeLabel = tk.Label(self, text="Welcome to Detention Organiser!", font=(None,20))
        self.WelcomeLabel.grid(columnspan=2)

        self.UsernameLabel = tk.Label(self, text="Username", font=(None,15) )
        self.UsernameLabel.grid(row=1, sticky="E")

        self.PasswordLabel = tk.Label(self, text="Password", font=(None,15) )
        self.PasswordLabel.grid(row=2, sticky="E")

        self.UsernameEntry  = tk.Entry(self)
        self.UsernameEntry.grid(row=1, column=1, sticky="W")

        self.PasswordEntry = tk.Entry(self, show="*")
        self.PasswordEntry.grid(row=2, column=1, sticky="W")

        self.StudentLabel = tk.Label(self, text="Student", font=(None,15) )
        self.StudentLabel.grid(row=3,column=0,columnspan=2)

        self.StudentTickBox = tk.Radiobutton(self,value= "Students", variable=self.SelectionRadio, tristatevalue="1")
        self.StudentTickBox.grid(row=3,column=1)

        self.TeacherLabel = tk.Label(self, text="Teacher", font=(None,15) )
        self.TeacherLabel.grid(row=4,column=0,columnspan=2)

        self.TeacherTickBox = tk.Radiobutton(self,value= "Teachers", variable=self.SelectionRadio, tristatevalue="2")
        self.TeacherTickBox.grid(row=4,column=1)

        self.AdminLabel = tk.Label(self, text="Admin", font=(None,15) )
        self.AdminLabel.grid(row=5,column=0,columnspan=2)

        self.AdminTickBox = tk.Radiobutton(self,value= "Admins", variable=self.SelectionRadio, tristatevalue="3")
        self.AdminTickBox.grid(row=5,column=1)

        self.LoginButton = tk.Button(self, text="Login")
        
        self.LoginButton.grid(columnspan=2)

        self.RegisterButton = tk.Button(self, text="Sign Up", command=lambda: controller.ShowFrame("RegisterFrame"))
        self.RegisterButton.grid(columnspan=2)


    def CheckDetails(self, Username, Password, Type, parent, controller):
        self.controller = controller
        
        if Type == "Teachers":

            cursor.execute("SELECT * FROM teachers WHERE EXISTS(SELECT * FROM students WHERE TeacherName = %s)", (Username,) )

            if cursor.fetchone():

                cursor.execute("SELECT Salt FROM teachers WHERE TeacherName = %s", (Username,) )
                Salt = cursor.fetchone()
                Salt =  ''.join(Salt) #Converts salt from tuple to string
                cursor.execute("SELECT * FROM teachers WHERE EXISTS(SELECT * FROM teachers WHERE TeacherName = %s AND Password = %s)", (Username, controller.LoginHashPassword(Password, Salt) ) )

                if cursor.fetchone():

                    controller.ShowFrame("TeacherDetentionFrame")
                    self.controller.SharedData["UsernameHolder"].set(Username)
                    messagebox.showinfo("Information", "You have successfully logged in!")

                else:
                    messagebox.showinfo("Information","Wrong username or password")

            else:
                messagebox.showinfo("Information","Wrong username or password")

        

        elif Type == "Students":

            cursor.execute("SELECT * FROM students WHERE EXISTS(SELECT * FROM students WHERE StudentName = %s)", (Username,) )

            if cursor.fetchone():

                cursor.execute("SELECT Salt FROM students WHERE StudentName = %s", (Username,) )
                Salt = cursor.fetchone()
                Salt =  ''.join(Salt) #Converts salt from tuple to string
                cursor.execute("SELECT * FROM students WHERE EXISTS(SELECT * FROM students WHERE StudentName = %s AND Password = %s)", (Username, controller.LoginHashPassword(Password, Salt) ) )

                if cursor.fetchone():

                    controller.ShowFrame("StudentDetentionFrame")
                    self.controller.SharedData["UsernameHolder"].set(Username)
                    messagebox.showinfo("Information", "You have successfully logged in!")
                
                else:
                    messagebox.showinfo("Information","Wrong username or password")

            else:
                messagebox.showinfo("Information","Wrong username or password")



        elif Type == "Admins":

            cursor.execute("SELECT * FROM admins WHERE EXISTS(SELECT * FROM admins WHERE AdminName = %s)", (Username,) )

            if cursor.fetchone():

                cursor.execute("SELECT Salt FROM admins WHERE AdminName = %s", (Username,) )
                Salt = cursor.fetchone()
                Salt =  ''.join(Salt) #Converts salt from tuple to string
                cursor.execute("SELECT * FROM admins WHERE EXISTS(SELECT * FROM admins WHERE AdminName = %s AND Password = %s)", (Username, controller.LoginHashPassword(Password, Salt) ) )

                if cursor.fetchone():

                    controller.ShowFrame("AdminControlFrame")
                    self.controller.SharedData["UsernameHolder"].set(Username)
                    messagebox.showinfo("Information", "You have successfully logged in!")
                
                else:
                    messagebox.showinfo("Information","Wrong username or password")

            else:
                messagebox.showinfo("Information","Wrong username or password")
    

        else:
            messagebox.showinfo("Information", "Please select a user type")


class RegisterFrame(tk.Frame, FrameHolder):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)  

        self.FormStatus = tk.StringVar()
        self.FormStatus.set("7A")
        
        self.RegisterLabel = tk.Label(self, text="Register", font=(None,20))
        self.RegisterLabel.grid(columnspan=2)

        self.UsernameLabel = tk.Label(self, text="Username", font=(None,15))
        self.UsernameLabel.grid(column=0,sticky="E")

        self.UsernameEntry  = tk.Entry(self)
        self.UsernameEntry.grid(row=1,column=1, sticky="W")
        
        self.PasswordLabel = tk.Label(self, text="Password", font=(None,15))
        self.PasswordLabel.grid(sticky="E")

        self.PasswordEntry = tk.Entry(self, show="*")
        self.PasswordEntry.grid(row=2,column=1, sticky="W")

        self.FormGroupLabel = tk.Label(self, text="Form Group", font=(None,15))
        self.FormGroupLabel.grid(row=3,sticky="E")

        self.FormGroupDrop  = tk.OptionMenu(self, self.FormStatus,"7A","7B","8A","8B")
        self.FormGroupDrop.grid(row=3,column=1, sticky="W")
        
        self.RegisterButton = tk.Button(self, text="Register")
        self.RegisterButton.grid(row=4,columnspan=2)

        self.BackButton = tk.Button(self, text="Back",command=lambda: controller.ShowFrame("LoginFrame"))
        self.BackButton.grid(row=5,columnspan=2)


if __name__ == "__main__":
    app = FrameHolder()
    app.title("Detention System")
    app.geometry("800x450")
    app.mainloop()