import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


Teacher = "TestTeacher"
Date = "TestDate"
Room = "TestRoom"

message = MIMEMultipart("alternative")
message["Subject"] = "Detention Reminder"
message["From"] = "detentionnotifications@gmail.com"
message["To"] = "makslilo11@gmail.com"


html = ("""\
<html>
  <body>

    <p>This is a reminder that you have been set a detention <br> You have a detention with {0} on {1} in room {2} <br> 
       
    </p>
  </body>
</html>
""" .format(Teacher, Date, Room) )

part1 = MIMEText(html, "html")
message.attach(part1)



context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login("detentionnotifications@gmail.com", "r8yYwVUaIf75")
    server.sendmail( "detentionnotification@gmail.com", "makslilo11@gmail.com", message.as_string() )