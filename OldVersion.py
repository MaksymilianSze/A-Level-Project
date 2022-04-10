import tkinter as tk    


class FrameHolder(tk.Tk):
    def __init__(self, *args, **kwargs): 
        tk.Tk.__init__(self, *args, **kwargs) 

        container = tk.Frame(self) 
        container.pack(expand=True) 
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1) 

        self.frames = {} 

        self.frames["TeacherSetDetentionFrame"] = TeacherSetDetentionFrame(parent=container, controller=self)
        self.frames["TeacherSetDetentionFrame"].grid(row=0, column=0, sticky="NESW")

        self.ShowFrame("TeacherSetDetentionFrame")

    def ShowFrame(self, FrameName):
        frame = self.frames[FrameName] 
        frame.tkraise() 

class TeacherSetDetentionFrame(tk.Frame):
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


        self.StudentsList = self.GetStudents( self.FormStatus.get() )


        self.StudentLabel = tk.Label(self, text="Student", font=(None,15))
        self.StudentLabel.grid(row=0,column=0,sticky="E")

        self.StudentDrop  = tk.OptionMenu(self,  self.DefaultStudent, *self.StudentsList )
        self.StudentDrop.grid(row=0, column=1, sticky="W")

        self.FormLabel = tk.Label(self, text="Form", font=(None,15))
        self.FormLabel.grid(row=1,column=0,sticky="E")

        self.FormDrop  = tk.OptionMenu(self, self.FormStatus, "7A","7B","8A","8B", command=lambda x: self.UpdateStudents( self.FormStatus.get() ) )
        self.FormDrop.grid(row=1,column=1, sticky="W")

    def GetStudents(self, Form):
        StudentList7A = ["Max","Kelly","Andrew"]
        StudentList8A = ["Steven","Harry","Kyle"]
        StudentList7B = ["Lilly", "Tim"]
        StudentList8B = ["Mike"]
        if Form == "7A":
            return StudentList7A
        elif Form == "8A":
            return StudentList8A
        elif Form == "7B":
            return StudentList7B
        else:
            return StudentList8B

    def student_selector(self, student):
        def inner():
            self.StudentsList.append(student)
            self.DefaultStudent.set(student)

        return inner

    def UpdateStudents(self, Form):
        menu = self.StudentDrop["menu"]
        menu.delete(0, "end")
        ListStudents = self.GetStudents( Form )
        for Student in ListStudents:
            menu.add_command(label=Student, command=self.student_selector(Student))


if __name__ == "__main__":
    app = FrameHolder()
    app.geometry("640x360")
    app.mainloop()