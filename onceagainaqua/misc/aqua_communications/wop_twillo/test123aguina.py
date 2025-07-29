import smtplib
import imaplib
import email
from email.message import EmailMessage
import time

# Config
EMAIL = "xvpmwc3857@gmail.com"
APP_PASSWORD = "yuaoghvjckiozfbx"
FRIEND_SMS_EMAIL = "6826003257@vzwpix.com"  # Replace with your friend's real number & gateway
FREIND_SMS="6826003257"
IMAP_SERVER = "imap.gmail.com"
SMTP_SERVER = "smtp.gmail.com"

# Send SMS via Email
def send_sms(message):
    msg = EmailMessage()
    msg.set_content(message)
    msg["From"] = EMAIL
    msg["To"] = FRIEND_SMS_EMAIL

    with smtplib.SMTP_SSL(SMTP_SERVER, 465) as smtp:
        smtp.login(EMAIL, APP_PASSWORD)
        smtp.send_message(msg)

# Check for Reply via Email
def get_reply():
    with imaplib.IMAP4_SSL(IMAP_SERVER) as imap:
        imap.login(EMAIL, APP_PASSWORD)
        imap.select("inbox")
        status, messages = imap.search(None, 'UNSEEN')
        if messages[0]:
            latest_id = messages[0].split()[-1]
            _, msg_data = imap.fetch(latest_id, "(RFC822)")
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)

            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode()
                        print(f"\n📩 Friend: {body.strip()}")
                        return
            else:
                body = msg.get_payload(decode=True).decode()
                print(f"\n📩 Friend: {body.strip()}")
        else:
            print("\n📭 No new messages.")

# Main Chat Loop
while True:
    get_reply()
    msg = input("You: ")
    send_sms(msg)
    time.sleep(4)