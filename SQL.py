import mysql.connector as mysql
db = mysql.connect(host="localhost", user="Maks",passwd="Password",database = "detentionsystem")
cursor = db.cursor(buffered=True)



'''
cursor.execute( "INSERT INTO detentions (StudentID, TeacherID, DetentionDatestamp, Length, Location, Ground, Description) VALUES (%s, %s, %s, %s, %s, %s, %s)", (8, 1, "2020-02-17" , 60, 145, "Fight", "Had some fight") )
db.commit()
'''


cursor.execute("CREATE TABLE Forms ( FormID int NOT NULL AUTO_INCREMENT, Form VARCHAR(255), PRIMARY KEY (FormID))" )
cursor.execute("CREATE TABLE Students ( StudentID int NOT NULL AUTO_INCREMENT, StudentName VARCHAR(255), StudentPassword VARCHAR(255), StudentEmail VARCHAR(255), Salt VARCHAR(16), PRIMARY KEY (StudentID))" )
cursor.execute("CREATE TABLE Teachers ( TeacherID int NOT NULL AUTO_INCREMENT, TeacherName VARCHAR(255), Password VARCHAR(255), Salt VARCHAR(16), PRIMARY KEY (TeacherID))" )

cursor.execute("ALTER TABLE Students ADD FormID int NOT NULL DEFAULT 0")
cursor.execute("ALTER TABLE Students ADD CONSTRAINT FKFormID FOREIGN KEY (FormID) REFERENCES Forms(FormID)")

cursor.execute("ALTER TABLE Forms ADD TeacherID int NOT NULL DEFAULT 0")
cursor.execute("ALTER TABLE Forms ADD CONSTRAINT FKTeacherID FOREIGN KEY (TeacherID) REFERENCES Teachers(TeacherID)")

cursor.execute("CREATE TABLE Admins ( AdminID int NOT NULL AUTO_INCREMENT, AdminName VARCHAR(255), Password VARCHAR(255), Salt VARCHAR(16), PRIMARY KEY (AdminID))" )

cursor.execute("CREATE TABLE detentions ( DetentionID int(11) NOT NULL AUTO_INCREMENT, StudentID int(11) NOT NULL, TeacherID int(11) NOT NULL, DetentionDateStamp date DEFAULT NULL, SetTimestamp timestamp NOT NULL DEFAULT current_timestamp(), 
                "Attended tinyint(1) DEFAULT NULL, Length tinyint(4) NOT NULL, Location smallint(6) NOT NULL, Ground varchar(100) NOT NULL, Description varchar(200) NOT NULL, PRIMARY KEY (DetentionID)")

cursor.execute("ALTER TABLE detentions ADD TeacherID (TeacherID), StudentID (StudentID)")
cursor.execute("ALTER TABLE detentions ADD CONSTRAINT FKStudentID FOREIGN KEY (StudentID) REFERENCES students (StudentID), CONSTRAINT FKTeacherDetentionID FOREIGN KEY (TeacherID) REFERENCES teachers")


