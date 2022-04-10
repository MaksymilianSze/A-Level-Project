from tkinter import *
from tkinter import messagebox
root = Tk()

root.geometry("640x360")
#root.resizable(0,0)

class MainPage():
    def __init__(self,master, *args, **kwargs):
        frame = Frame(master)
        frame.pack()

    def Show(self):
        self.lift()


class LoginFrame(MainPage):
    def __init__(self, master,*args,**kwargs):
        super().__init__(master)
        frame = Frame(master)
        frame.pack()

        self.WelcomeLabel = Label( frame, text="Welcome to Detention Organiser!",font=(None,20) ).grid(columnspan=2)
        self.UsernameLabel = Label( frame, text="Username",font=(None,15) ).grid(row=1, sticky=E)
        self.PasswordLabel = Label( frame, text="Password",font=(None,15) ).grid(row=2, sticky=E)

        self.UsernameEntry  = Entry(frame).grid(row=1, column=1, sticky=W)
        self.PasswordEntry = Entry(frame, show="*").grid(row=2, column=1, sticky=W)

        self.LoginButton = Button(frame, text="Login",command=self.LoginClicked).grid(columnspan=2)
        self.RegisterButton = Button(frame, text="Register")
        #self.RegisterButton.configure(command=lambda:####)
        self.RegisterButton.grid(columnspan=2)
        self.IsRegisterClicked = False


    def MakeRegisterClicked(self):
        print("MakeRegisterClicked called")
        self.IsRegisterClicked = True


    def RegisterClicked(self):
        print("RegisterClicked called")
        if self.IsRegisterClicked:
            self.Show()
        

    def LoginClicked(self):
        pass #Placeholder
    
    
class RegisterFrame(MainPage):
    def __init__(self,master):
        frame = Frame(master)
        frame.pack()

        self.WelcomeLabel = Label( frame, text="Welcome to Detention Organiser!",font=(None,20) ).grid(columnspan=2)
        self.UsernameLabel = Label( frame, text="Username",font=(None,15) ).grid(row=1, sticky=E)

'''
class MainView():
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        p1 = Page1(self)
        p2 = Page2(self)
        p3 = Page3(self)

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = tk.Button(buttonframe, text="Page 1", command=p1.lift)
        b2 = tk.Button(buttonframe, text="Page 2", command=p2.lift)
        b3 = tk.Button(buttonframe, text="Page 3", command=p3.lift)

        b1.pack(side="left")
        b2.pack(side="left")
        b3.pack(side="left")

        p1.show()
'''

'''
Main = MainView(root)
Main.pack(side="top", fill="both", expand=True)
'''
LoginScreen = LoginFrame(root)

root.mainloop()


'''
WelcomeLabel = Label(root, text="Welcome to Detention Organiser!",font=(None,20)).place(x=320,y=20,anchor="center")

UsernameLabel = Label(root,text="Username",font=(None,15)).grid(row=0, sticky=E)
PasswordLabel = Label(root,text="Password",font=(None,15)).grid(row=1, sticky=E)

UsernameEntry = Entry(root,width=20).place(x=390,y=164,anchor="center")

PasswordEntry = Entry(root,width=20).place(x=390,y=196,anchor="center")

LoginButton = Button(root,text="Login",font=(None,15)).place(x=320,y=250,anchor="center")
'''





'''
class ButtonsLol:
    def __init__(self,master):
        root.geometry("640x360")
        frame = Frame(master)
        frame.pack()

        self.printButton = Button(frame,text="Test", command=self.printMessage).pack(side=LEFT)
        self.quitButton = Button(frame,text="Quit", command=frame.quit).pack(side=RIGHT)

    def printMessage(self):
        print("Kek")


ClassTest = ButtonsLol(root)
'''


root.mainloop()
