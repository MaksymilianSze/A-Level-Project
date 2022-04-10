class MainClass():

    def __init__(self, Username):
        self.Username = Username

    def Method():
        print("Works lol")

class SubClass(MainClass):
    def __init__(self,NewUsername):
        self.NewUsername = NewUsername



Main = MainClass("Maks")
Sub = SubClass("Lmao")


SubClass.Method()




