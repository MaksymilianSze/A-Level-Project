import mysql.connector as mysql
db = mysql.connect(host="localhost", user="Maks",passwd="Password",database = "detentionsystem")
cursor = db.cursor(buffered=True)




curser.execute( "INSERT INTO detentions (StudentID, TeacherID, DetentionDatestamp, Length, Location, Ground, Description) VALUES (%s, %s, %s, %s, %s, %s, %s)", (6, 1, FullDate , 60, 145, "Fight", "Had some fight") 







'''
def InsertTeacherQuery(UsernameInput, PasswordInput):
    cursor.execute("INSERT INTO Teachers (Username,Password) VALUES (%s, %s)", (UsernameInput, PasswordInput))

InsertTeacherQuery("NewTeacher", "Lmao")

cursor.execute( "SELECT * FROM Teachers" )
TeacherInfo = cursor.fetchall()
for x in TeacherInfo:
    print(x)







cursor.execute( "SELECT * FROM Students")
StudentInfo = cursor.fetchall()

for x in StudentInfo:
    print(x)







cursor.execute("CREATE TABLE Teachers ( ID int NOT NULL AUTO_INCREMENT,Username VARCHAR(255), Password VARCHAR(255),PRIMARY KEY (ID))" )


'''

