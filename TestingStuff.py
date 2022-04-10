import mysql.connector as mysql
db = mysql.connect(host="localhost", user="Maks",passwd="Password",database = "detentionsystem")
cursor = db.cursor(buffered=True)

import datetime



#cursor.execute( "INSERT INTO forms (Form, TeacherID) VALUES (%s, %s)", ("8B","4") )
#db.commit()
#cursor.execute( "INSERT INTO forms (FormID, Form, TeacherID) VALUES (NULL, %s, %s)",("7A","3"))

'''
def InsertTeacherQuery(UsernameInput, PasswordInput):
    cursor.execute("INSERT INTO Teachers (TeacherName, TeacherPassword) VALUES (%s, %s)", (UsernameInput, PasswordInput))

InsertTeacherQuery("John Andrews ","Test")



cursor.execute( "SELECT * FROM Teachers" )
TeacherInfo = cursor.fetchall()
for x in TeacherInfo:
    print(x)


cursor.execute( "SELECT * FROM Teachers" )
'''
#cursor.execute( "INSERT INTO Teachers (TeacherName, Password) VALUES (%s, %s)", ("AndrewSmith","Test") )


'''
cursor.execute("CREATE TABLE Forms ( FormID int NOT NULL AUTO_INCREMENT, Form VARCHAR(255), PRIMARY KEY (FormID))" )
cursor.execute("CREATE TABLE Students ( StudentID int NOT NULL AUTO_INCREMENT, StudentName VARCHAR(255), StudentPassword VARCHAR(255), StudentEmail VARCHAR(255),PRIMARY KEY (StudentID))" )
cursor.execute("CREATE TABLE Teachers ( TeacherID int NOT NULL AUTO_INCREMENT,TeacherName VARCHAR(255), Password VARCHAR(255),PRIMARY KEY (TeacherID))" )

cursor.execute("ALTER TABLE Students ADD FormID int NOT NULL DEFAULT 0")
cursor.execute("ALTER TABLE Students ADD CONSTRAINT FKFormID FOREIGN KEY (FormID) REFERENCES Forms(FormID)")

cursor.execute("ALTER TABLE Forms ADD TeacherID int NOT NULL DEFAULT 0")
cursor.execute("ALTER TABLE Forms ADD CONSTRAINT FKTeacherID FOREIGN KEY (TeacherID) REFERENCES Teachers(TeacherID)")
'''


#cursor.execute("CREATE TABLE Admins ( AdminID int NOT NULL AUTO_INCREMENT, AdminName VARCHAR(255), Password VARCHAR(255), PRIMARY KEY (AdminID))" )




#a, b = map(list, zip(ListOfValues))

print( datetime.date.today() )




'''
for x in ListOfValues:
    for y in x:
        print(y)
'''
#db.commit()