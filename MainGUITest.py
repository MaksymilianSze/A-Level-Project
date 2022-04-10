import tkinter as tk    

from tkinter import messagebox

import mysql.connector as mysql

import hashlib

import tkcalendar

import datetime

db = mysql.connect(host="localhost", user="Maks",passwd="Password",database = "detentionsystem")
cursor = db.cursor(buffered=True)






class FrameHolder(tk.Tk): #Inherits from Tk

    def __init__(self, *args, **kwargs): #This is the constructor method which allows for any amount of paremeters 
        tk.Tk.__init__(self, *args, **kwargs) #Inherits from tk.Tk, essentially the same as super().__init__()


        container = tk.Frame(self) #This creates a frame widget will be used to contain all the pages which will be stacked on top of each other
        container.pack(expand=True) #Packs the container frame which wil expand when resized
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1) #Spreads the weight of the columns out evenly

        self.frames = {} #Create empty dictionary

        self.frames["LoginFrame"] = LoginFrame(parent=container, controller=self)
        self.frames["RegisterFrame"] = RegisterFrame(parent=container, controller=self)
        self.frames["StudentDetentionFrame"] = StudentDetentionFrame(parent=container, controller=self) #Create all the frames 
        self.frames["TeacherDetentionFrame"] = TeacherDetentionFrame(parent=container, controller=self)
        self.frames["AdminControlFrame"] = AdminControlFrame(parent=container, controller=self)
        self.frames["TeacherSetDetentionFrame"] = TeacherSetDetentionFrame(parent=container, controller=self)

        self.frames["LoginFrame"].grid(row=0, column=0, sticky="NESW")
        self.frames["RegisterFrame"].grid(row=0, column=0, sticky="NESW") #Put all the frames in the container
        self.frames["StudentDetentionFrame"].grid(row=0, column=0, sticky="NESW")
        self.frames["TeacherDetentionFrame"].grid(row=0, column=0, sticky="NESW")
        self.frames["AdminControlFrame"].grid(row=0, column=0, sticky="NESW")
        self.frames["TeacherSetDetentionFrame"].grid(row=0, column=0, sticky="NESW")

        self.ShowFrame("TeacherSetDetentionFrame") #Login frame is meant to be the first frame to be show

    def ShowFrame(self, FrameName):
        frame = self.frames[FrameName] #Sets frame to be the frame to switch to
        frame.tkraise() #Brings the desired frame to the top
        print("switching frames")

    def HashPassword(self, Password):
        h = hashlib.sha256()
        h.update(Password.encode("utf8")) 
        Hashed = h.hexdigest()
        return Hashed

        



class LoginFrame(tk.Frame, FrameHolder):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.grid_rowconfigure(5, weight=1) 
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.TypeTicked = ""


        WelcomeLabel = tk.Label(self, text="Welcome to Detention Organiser!", font=(None,20))
        WelcomeLabel.grid(columnspan=2)

        UsernameLabel = tk.Label(self, text="Username", font=(None,15) )
        UsernameLabel.grid(row=1, sticky="E")

        PasswordLabel = tk.Label(self, text="Password", font=(None,15) )
        PasswordLabel.grid(row=2, sticky="E")

        UsernameEntry  = tk.Entry(self)
        UsernameEntry.grid(row=1, column=1, sticky="W")

        PasswordEntry = tk.Entry(self, show="*")
        PasswordEntry.grid(row=2, column=1, sticky="W")

        StudentLabel = tk.Label(self, text="Student", font=(None,15) )
        StudentLabel.grid(row=3,column=0,columnspan=2)

        StudentTickBox = tk.Radiobutton(self,value=1, tristatevalue="1", command=lambda: self.Ticked("Students"))
        StudentTickBox.grid(row=3,column=1)

        TeacherLabel = tk.Label(self, text="Teacher", font=(None,15) )
        TeacherLabel.grid(row=4,column=0,columnspan=2)

        TeacherTickBox = tk.Radiobutton(self,value=2, tristatevalue="2", command=lambda: self.Ticked("Teachers"))
        TeacherTickBox.grid(row=4,column=1)

        AdminLabel = tk.Label(self, text="Admin", font=(None,15) )
        AdminLabel.grid(row=5,column=0,columnspan=2)

        AdminTickBox = tk.Radiobutton(self,value=3, tristatevalue="3", command=lambda: self.Ticked("Admins"))
        AdminTickBox.grid(row=5,column=1)

        LoginButton = tk.Button(self, text="Login", command=lambda: self.CheckDetails(UsernameEntry.get(),PasswordEntry.get(), self.TypeTicked, parent, controller) )
        
        LoginButton.grid(columnspan=2)

        RegisterButton = tk.Button(self, text="Sign Up", command=lambda: controller.ShowFrame("RegisterFrame"))
        RegisterButton.grid(columnspan=2)


    
    def Ticked(self,Type):
        self.TypeTicked = Type



    def CheckDetails(self, Username, Password, Type, parent, controller):
        self.controller = controller

        if Type == "Teachers":
            cursor.execute("SELECT * FROM teachers WHERE EXISTS(SELECT * FROM teachers WHERE TeacherName = %s AND Password = %s)", (Username, controller.HashPassword(Password)))
            if cursor.fetchone():
                controller.ShowFrame("TeacherDetentionFrame")
                messagebox.showinfo("Information", "You have successfully logged in!")
                self.UsernameHolder = Username
            else:
                messagebox.showinfo("Information","Wrong username or password")

        
        elif Type == "Students":
            cursor.execute("SELECT * FROM students WHERE EXISTS(SELECT * FROM students WHERE StudentName = %s AND Password = %s)", (Username, controller.HashPassword(Password) ) )
            if cursor.fetchone():
                controller.ShowFrame("StudentDetentionFrame")
                messagebox.showinfo("Information", "You have successfully logged in!")
            else:
                messagebox.showinfo("Information","Wrong username or password")


        elif Type == "Admins":
            cursor.execute("SELECT * FROM admins WHERE EXISTS(SELECT * FROM admins WHERE AdminName = %s AND Password = %s)", (Username, controller.HashPassword(Password) ) )
            if cursor.fetchone():
                controller.ShowFrame("AdminControlFrame")
                messagebox.showinfo("Information", "You have successfully logged in!")
            else:
                messagebox.showinfo("Information","Wrong username or password")
    

        else:
            messagebox.showinfo("Information", "Please select a user type")







    #def CreateWidget(self, Type, Text):
        #tkancer = getattr(tk, Type)
        #tkancer(self, text=Text)
        



class RegisterFrame(tk.Frame, FrameHolder):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)  

        self.FormStatus = tk.StringVar()
        self.FormStatus.set("7A")

        
        RegisterLabel = tk.Label(self, text="Register", font=(None,20))
        RegisterLabel.grid(columnspan=2)

        UsernameLabel = tk.Label(self, text="Username", font=(None,15))
        UsernameLabel.grid(column=0,sticky="E")

        UsernameEntry  = tk.Entry(self)
        UsernameEntry.grid(row=1,column=1, sticky="W")
        
        PasswordLabel = tk.Label(self, text="Password", font=(None,15))
        PasswordLabel.grid(sticky="E")

        PasswordEntry = tk.Entry(self, show="*")
        PasswordEntry.grid(row=2,column=1, sticky="W")

        FormGroupLabel = tk.Label(self, text="Form Group", font=(None,15))
        FormGroupLabel.grid(row=3,sticky="E")

        FormGroupDrop  = tk.OptionMenu(self, self.FormStatus,"7A","7B","8A","8B")
        FormGroupDrop.grid(row=3,column=1, sticky="W")
        
        RegisterButton = tk.Button(self, text="Register", command=lambda: self.RegisterStudent(UsernameEntry.get(), PasswordEntry.get(), self.FormStatus.get(), parent, controller) )
        RegisterButton.grid(row=4,columnspan=2)

        BackButton = tk.Button(self, text="Back",command=lambda: controller.ShowFrame("LoginFrame"))
        BackButton.grid(row=5,columnspan=2)


    def RegisterStudent(self, Username, Password, Form, parent, controller):
        self.controller = controller

        Username = Username.replace(" ", "")
        Password = Password.strip(" ")
        print(Username, Password)
        if (not Username) or (not Password):
            messagebox.showinfo("Information","Please enter a username and password")
        else:
            cursor.execute("SELECT FormID FROM forms WHERE Form = %s", (Form,) )
            FormID = cursor.fetchone()

            for x in FormID:
                cursor.execute( "INSERT INTO Students (StudentName, Password, FormID) VALUES (%s, %s, %s)", (Username, controller.HashPassword(Password), x) )
            db.commit()
            messagebox.showinfo("Information","You have successfully registered!")
        

        #RegisteredLabel = tk.Label(self, text="You have registered Successfully!")
        #RegisteredLabel.grid(row=6,columnspan=2)



class StudentDetentionFrame(tk.Frame, FrameHolder):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        Detentions = tk.Label(self, text="These are your upcoming detentions",font=(None,20))
        Detentions.grid(columnspan=2)


        LogoutButton = tk.Button(self, text="Logout",command=lambda: controller.ShowFrame("LoginFrame"))
        LogoutButton.grid(columnspan=2) 


class TeacherDetentionFrame(LoginFrame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        Detentions = tk.Label(self, text="These are your set detentions",font=(None,20))
        Detentions.grid(columnspan=2)

        NewDetentionButton = tk.Button(self, text="Set Detention",command=lambda: controller.ShowFrame("TeacherSetDetentionFrame"))
        NewDetentionButton.grid(columnspan=2) 

        LogoutButton = tk.Button(self, text="Logout",command=lambda: controller.ShowFrame("LoginFrame"))
        LogoutButton.grid(columnspan=2) 


class TeacherSetDetentionFrame(TeacherDetentionFrame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)


        self.FormStatus = tk.StringVar()
        self.FormStatus.set("7A")

        self.DefaultStudent = tk.StringVar()
        self.DefaultStudent.set("Select Student")

        self.DefaultGround = tk.StringVar()
        self.DefaultGround.set("Select a Ground")

        self.DefaultRoomText = tk.StringVar(self, value="Enter Room Number")
        self.DefaultLengthText = tk.StringVar(self, value="Between 30-120 mins")

        self.StudentsList = self.GetStudents( self.FormStatus.get() )

        self.Day = int( datetime.date.today().strftime("%d") )

        self.Month = int( datetime.date.today().strftime("%m") )

        self.Year = int( datetime.date.today().strftime("%y") )

        #self.UsernameHolder = LoginFrame.UsernameHolder


        StudentLabel = tk.Label(self, text="Student", font=(None,15))
        StudentLabel.grid(row=0,column=0,sticky="E")

        self.StudentDrop  = tk.OptionMenu(self,  self.DefaultStudent, *self.StudentsList )
        self.StudentDrop.grid(row=0, column=1, sticky="W")

        FormLabel = tk.Label(self, text="Form", font=(None,15))
        FormLabel.grid(row=1,column=0,sticky="E")

        FormDrop  = tk.OptionMenu(self, self.FormStatus, "7A","7B","8A","8B", command=lambda x: self.UpdateStudents( self.FormStatus.get() ) )
        FormDrop.grid(row=1,column=1, sticky="W")

        TimeStampLabel = tk.Label(self, text="Date", font=(None,15))
        TimeStampLabel.grid(row=2,column=0,sticky="E")

        TimeStamp  = tkcalendar.DateEntry(self,width=12, year=self.Year, month=self.Month, day=self.Day, background='darkblue', foreground='white', borderwidth=2)
        TimeStamp.grid(row=2,column=1, sticky="W")
        
        GroundLabel = tk.Label(self, text="Ground", font=(None,15))
        GroundLabel.grid(row=3,column=0,sticky="E")

        GroundDrop = tk.OptionMenu(self, self.DefaultGround,"Incomplete Homework","Non Compliant Behaviour","Classroom Disruption","Disrespectful to Staff","Disrespectful to Student","Fight","Not Ready For Learning")
        GroundDrop.grid(row=3,column=1, sticky="W")

        DescriptionLabel = tk.Label(self, text="Description", font=(None,15))
        DescriptionLabel.grid(row=4,column=0, rowspan=3, sticky="E")

        DescriptionEntry = tk.Text(self, height=3, width=40)
        DescriptionEntry.grid(row=4, column=1, rowspan=3, sticky="W")

        LengthLabel =  tk.Label(self, text="Length", font=(None,15))
        LengthLabel.grid(row=7, column=0, sticky="E")

        LengthEntry =  tk.Entry(self, textvariable=self.DefaultLengthText, font=(None,10) ) 
        LengthEntry.grid(row=7, column=1, sticky="W")       
        
        LocationLabel = tk.Label(self, text="Location", font=(None,15))
        LocationLabel.grid(row=8,column=0,sticky="E")

        LocationEntry = tk.Entry(self, textvariable=self.DefaultRoomText, font=(None,10))
        LocationEntry.grid(row=8,column=1, sticky="W")

        BackButton = tk.Button(self, text="Back",command=lambda: controller.ShowFrame("TeacherDetentionFrame"))
        BackButton.grid(columnspan=2)


    def GetStudents(self, Form):
        cursor.execute("SELECT Form, FormID FROM forms") 
        ListOfValues = cursor.fetchall()
        
        
        for x in ListOfValues:
            if Form in x:
                StudentFormID = x[1]
                

        cursor.execute( "SELECT StudentName FROM students WHERE FormID = %s", (StudentFormID,) )
        Students = list( cursor.fetchall() )
        return Students


    def UpdateStudents(self, Form):
        menu = self.StudentDrop["menu"]
        menu.delete(0, "end")
        ListStudents = self.GetStudents( Form )
        for Student in ListStudents:
            menu.add_command(label=Student, command=lambda: self.Students.append(Student) )


    def SetDetention(self, StudentID, TeacherID, DetentionTimeStamp, Length, Location, Ground, Description):
        pass


    
        


class AdminControlFrame(LoginFrame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        Detentions = tk.Label(self, text="Welcome!",font=(None,20))
        Detentions.grid(columnspan=2)


        LogoutButton = tk.Button(self, text="Logout",command=lambda: controller.ShowFrame("LoginFrame"))
        LogoutButton.grid(columnspan=2) 





if __name__ == "__main__":
    app = FrameHolder()
    app.geometry("640x360")
    app.mainloop()