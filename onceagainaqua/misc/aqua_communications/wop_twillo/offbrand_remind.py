import smtplib
from email.message import EmailMessage


with open(r'F:\aqua\aqua_communications\wop_twillo\phone_numbers.txt', 'r') as file:
    phone_numbers = file.readlines()

message_content = """
gingle gong

"""


msg = EmailMessage()
msg.set_content(message_content)
msg["Subject"] = "aquatic failure"
msg["From"] = "xvpmwc3857@gmail.com"


with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    smtp.login("xvpmwc3857@gmail.com", "yuaoghvjckiozfbx")
    for number in phone_numbers:
        number = number.strip()
        msg = EmailMessage()
        msg.set_content(message_content)
        msg["Subject"] = "subject"
        msg["From"] = "xvpmwc3857@gmail.com"
        msg["To"] = number
        smtp.send_message(msg)

print("sen")
