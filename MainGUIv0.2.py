import tkinter as tk    

from tkinter import messagebox

import mysql.connector as mysql

import hashlib

import tkcalendar

import tkinter.ttk as ttk

import datetime

import secrets

db = mysql.connect(host="localhost", user="Maks",passwd="Password",database = "detentionsystem")
cursor = db.cursor(buffered=True)






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

        self.ShowFrame("LoginFrame") #Login frame is meant to be the first frame to be show

    def GetPage(self, PageClass):
        return self.frames[PageClass]

    def ShowFrame(self, FrameName):
        frame = self.frames[FrameName] #Sets frame to be the frame to switch to
        frame.tkraise() #Brings the desired frame to the top
        print("switching frames")

    def RegisterHashPassword(self, Password):
        Salt = secrets.token_hex(8)
        h = hashlib.sha256()
        SaltedPassword = Password + Salt
        h.update(SaltedPassword.encode("utf8")) 
        Hashed = h.hexdigest()
        return Hashed, Salt

    def LoginHashPassword(self, Password, Salt):
        Password = Password
        Salt = Salt
        SaltedPassword = Password + Salt
        h = hashlib.sha256()
        h.update(SaltedPassword.encode("utf8"))
        Hashed = h.hexdigest()
        return Hashed

    def GetID(self, Type, Name):

        if Type == "Student":
            cursor.execute( "SELECT StudentID FROM students WHERE StudentName = %s", (Name,) )
            FoundID = cursor.fetchone()[0]
            return FoundID

        elif Type == "Teacher":
            cursor.execute( "SELECT TeacherID FROM teachers WHERE TeacherName = %s", (Name,) )
            if cursor.fetchone():
                cursor.execute( "SELECT TeacherID FROM teachers WHERE TeacherName = %s", (Name,) )
                FoundID = cursor.fetchone()[0]
                return FoundID

            else: 
                messagebox.showinfo("Error", "Please login again")
                return False

            
    def GetName(self, Type, ID):

        if Type == "Student":
            cursor.execute("SELECT StudentName FROM students WHERE StudentID = %s", (ID,) )
            FoundName = cursor.fetchone()[0]
            return FoundName



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

        self.LoginButton = tk.Button(self, text="Login", command=lambda: self.CheckDetails(self.UsernameEntry.get(), self.PasswordEntry.get(), self.SelectionRadio.get(), parent, controller) )
        
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
        
        self.RegisterButton = tk.Button(self, text="Register", command=lambda: self.RegisterStudent(self.UsernameEntry.get(), self.PasswordEntry.get(), self.FormStatus.get(), parent, controller) )
        self.RegisterButton.grid(row=4,columnspan=2)

        self.BackButton = tk.Button(self, text="Back",command=lambda: controller.ShowFrame("LoginFrame"))
        self.BackButton.grid(row=5,columnspan=2)


    def RegisterStudent(self, Username, Password, Form, parent, controller):
        self.controller = controller

        FormattedUsername = Username.replace(" ", "")
        FormattedPassword = Password.replace(" ", "")
        FormattedPassword, Salt = controller.RegisterHashPassword(Password)
        
        if (not FormattedUsername) or (not FormattedPassword):
            messagebox.showinfo("Information","Please enter a username and password")
        else:
            cursor.execute("SELECT FormID FROM forms WHERE Form = %s", (Form,) )
            FormID = cursor.fetchone()

            for x in FormID:
                cursor.execute( "INSERT INTO Students (StudentName, Password, Salt, FormID) VALUES (%s, %s, %s, %s)", (FormattedUsername, FormattedPassword, Salt, x) )
            db.commit()
            messagebox.showinfo("Information","You have successfully registered!")
        

        #RegisteredLabel = tk.Label(self, text="You have registered Successfully!")
        #RegisteredLabel.grid(row=6,columnspan=2)



class StudentDetentionFrame(tk.Frame, FrameHolder):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.User = self.controller.SharedData["UsernameHolder"].get()

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.Detentions = tk.Label(self, text="These are your upcoming detentions",font=(None,20))
        self.Detentions.grid(columnspan=2)


        self.LogoutButton = tk.Button(self, text="Logout",command=lambda: self.Test() )
        self.LogoutButton.grid(columnspan=2) 

        #controller.ShowFrame("LoginFrame")

    def Test(self):
        print("The user is:", self.controller.SharedData["UsernameHolder"].get() )


class TeacherDetentionFrame(LoginFrame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
 

        self.Detentions = tk.Label(self, text="These are your set detentions",font=(None,20))
        self.Detentions.grid(columnspan=2)

        self.DetentionTree = ttk.Treeview(self)

        self.DetentionTree["columns"]=("0","1","2","3","4")
        self.DetentionTree.column("0", width=120, minwidth=100, stretch=tk.NO)
        self.DetentionTree.column("1", width=80, minwidth=50, stretch=tk.NO)
        self.DetentionTree.column("2", width=80, minwidth=50, stretch=tk.NO)
        self.DetentionTree.column("3", width=80, minwidth=50, stretch=tk.NO)
        self.DetentionTree.column("4", width=120, minwidth=100, stretch=tk.NO)

        self.DetentionTree.heading("0", text="Student",anchor=tk.W)
        self.DetentionTree.heading("1", text="Form",anchor=tk.W)
        self.DetentionTree.heading("2", text="Length",anchor=tk.W)
        self.DetentionTree.heading("3", text="Date",anchor=tk.W)
        self.DetentionTree.heading("4", text="Room Number",anchor=tk.W)

        self.DetentionTree.grid(columnspan=2,row=1)
        self.DetentionTree['show'] = 'headings'

        self.NewDetentionButton = tk.Button(self, text="Set Detention",command=lambda: controller.ShowFrame("TeacherSetDetentionFrame"))
        self.NewDetentionButton.grid(columnspan=2) 

        self.RefreshDetentions = tk.Button(self, text="Refresh Detentions",command=lambda:  self.GetDetentions( controller.GetID( "Teacher", self.controller.SharedData["UsernameHolder"].get() ), controller ) )
        self.RefreshDetentions.grid(columnspan=2) 

        self.LogoutButton = tk.Button(self, text="Logout",command=lambda: controller.ShowFrame("LoginFrame"))
        self.LogoutButton.grid(columnspan=2) 

    def GetDetentions(self, TeacherID, controller):
        self.controller = controller
        cursor.execute( "SELECT StudentID FROM detentions WHERE TeacherID = %s", (TeacherID,) )


        TuplesOfIds = cursor.fetchall()
        ListOfIds = []
        ListOfNames = []
        ListOfForms = []

        cursor.execute( "SELECT Length, DetentionDateStamp, Location FROM detentions WHERE TeacherID = %s ", (TeacherID,) )
        DetentionInfo = cursor.fetchall()

        for x in TuplesOfIds:
            for ID in x:
                ListOfIds.append(ID)

       
        for x in ListOfIds:
            ListOfNames.append( controller.GetName("Student", x) )

        for x in ListOfNames:
            cursor.execute("SELECT FormID FROM students WHERE StudentName = %s", (x,) )
            FormID = cursor.fetchone()[0]
            cursor.execute("SELECT Form FROM forms WHERE FormID= %s", (FormID,) )
            Form = cursor.fetchone()[0]
            ListOfForms.append(Form)

        FormDetentionInfo = tuple( zip( ListOfForms, *zip(*DetentionInfo) ) ) #https://stackoverflow.com/questions/52442388/how-to-merge-1d-2d-tuples-in-python

        AllInfo = tuple( zip( ListOfNames, *zip(*FormDetentionInfo) ) )


        for x in AllInfo:
            self.DetentionTree.insert("", "end", values=(x)  )





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



        self.StudentLabel = tk.Label(self, text="Student", font=(None,15))
        self.StudentLabel.grid(row=0,column=0,sticky="E")

        self.StudentDrop  = tk.OptionMenu(self,  self.DefaultStudent, *self.StudentsList )
        self.StudentDrop.grid(row=0, column=1, sticky="W")

        self.FormLabel = tk.Label(self, text="Form", font=(None,15))
        self.FormLabel.grid(row=1,column=0,sticky="E")

        self.FormDrop  = tk.OptionMenu(self, self.FormStatus, "7A","7B","8A","8B", command=lambda x: self.UpdateStudents( self.FormStatus.get() ) )
        self.FormDrop.grid(row=1,column=1, sticky="W")

        self.TimeStampLabel = tk.Label(self, text="Date", font=(None,15))
        self.TimeStampLabel.grid(row=2,column=0,sticky="E")

        self.TimeStamp  = tkcalendar.DateEntry(self,width=12, year=self.Year, month=self.Month, day=self.Day, background='darkblue', foreground='white', borderwidth=2)
        self.TimeStamp.grid(row=2,column=1, sticky="W")
        
        self.GroundLabel = tk.Label(self, text="Ground", font=(None,15))
        self.GroundLabel.grid(row=3,column=0,sticky="E")

        self.GroundDrop = tk.OptionMenu(self, self.DefaultGround,"Incomplete Homework","Non Compliant Behaviour","Classroom Disruption","Disrespectful to Staff","Disrespectful to Student","Fight","Not Ready For Learning")
        self.GroundDrop.grid(row=3,column=1, sticky="W")

        self.DescriptionLabel = tk.Label(self, text="Description", font=(None,15))
        self.DescriptionLabel.grid(row=4,column=0, rowspan=3, sticky="E")

        self.DescriptionEntry = tk.Text(self, height=3, width=40)
        self.DescriptionEntry.grid(row=4, column=1, rowspan=3, sticky="W")

        self.LengthLabel =  tk.Label(self, text="Length", font=(None,15))
        self.LengthLabel.grid(row=7, column=0, sticky="E")

        self.LengthEntry =  tk.Entry(self, textvariable=self.DefaultLengthText, font=(None,10) ) 
        self.LengthEntry.grid(row=7, column=1, sticky="W")       
        
        self.LocationLabel = tk.Label(self, text="Location", font=(None,15))
        self.LocationLabel.grid(row=8,column=0,sticky="E")

        self.LocationEntry = tk.Entry(self, textvariable=self.DefaultRoomText, font=(None,10))
        self.LocationEntry.grid(row=8,column=1, sticky="W")

        self.Set = tk.Button(self, text="Set",command=lambda: self.SetDetention( self.DefaultStudent.get(), self.controller.SharedData["UsernameHolder"].get() , str( self.TimeStamp.get_date() ), self.LengthEntry.get(), self.LocationEntry.get(), self.DefaultGround.get(), self.DescriptionEntry.get("1.0","end"), controller ) )
        self.Set.grid(columnspan=2)

        self.BackButton = tk.Button(self, text="Back",command=lambda: controller.ShowFrame("TeacherDetentionFrame") )
        self.BackButton.grid(columnspan=2)


    def GetStudents(self, Form):
        cursor.execute("SELECT Form, FormID FROM forms") 
        ListOfValues = cursor.fetchall()
        
        
        for x in ListOfValues:
            if Form in x:
                StudentFormID = x[1]
                

        cursor.execute( "SELECT StudentName FROM students WHERE FormID = %s", (StudentFormID,) )
        Students = [item[0] for item in cursor.fetchall()]


        if Students:
            return Students

            
        else:
            return ""



    def UpdateStudents(self, Form):
        menu = self.StudentDrop["menu"]
        menu.delete(0, "end")
        ListStudents = self.GetStudents( Form )
        for Student in ListStudents:
            menu.add_command(label=Student, command=self.StudentSelector(Student) )


    def StudentSelector(self, student):
        def inner():
            self.StudentsList.append(student)
            self.DefaultStudent.set(student)
        return inner





    def SetDetention(self, Student, Teacher, DetentionDate, Length, Location, Ground, Description, controller): 
        self.controller = controller

        StudentID = controller.GetID("Student", Student)
        TeacherID = controller.GetID("Teacher", Teacher)

        if not TeacherID:
            controller.ShowFrame("LoginFrame")
            return

        cursor.execute("INSERT INTO detentions (StudentID, TeacherID, DetentionDatestamp, Length, Location, Ground, Description) VALUES (%s, %s, %s, %s, %s, %s, %s)", (StudentID, TeacherID, DetentionDate, Length, Location, Ground, Description) )
        db.commit()
        print(Student, Teacher, DetentionDate, Length, Location, Ground, Description)




    
        


class AdminControlFrame(LoginFrame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.Detentions = tk.Label(self, text="Welcome!",font=(None,20))
        self.Detentions.grid(columnspan=2)


        self.LogoutButton = tk.Button(self, text="Logout",command=lambda: controller.ShowFrame("LoginFrame"))
        self.LogoutButton.grid(columnspan=2) 





if __name__ == "__main__":
    app = FrameHolder()
    app.geometry("640x360")
    app.mainloop()