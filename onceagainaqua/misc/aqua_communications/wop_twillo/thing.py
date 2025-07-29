import imaplib
import email
import smtplib
import time
from email.message import EmailMessage

# 🔧 Configuration
EMAIL = "xvpmwc3857@gmail.com"
APP_PASSWORD = "yuaoghvjckiozfbx"
PHONE_EMAIL = "6823136450@tmomail.net"  # Replace with actual number + carrier gateway

# 🧠 Local rule-based chatbot
def get_local_response(prompt):
    prompt = prompt.lower()
    if "hello" in prompt:
        return "Hi there! 👋"
    elif "how are you" in prompt:
        return "I'm just a Python script, but I'm running smoothly!"
    elif "joke" in prompt:
        return "Why did the function break up with the loop? It got tired of going in circles."
    elif "bye" in prompt:
        return "Goodbye! Talk soon."
    else:
        return "I’m not sure how to respond to that, but I’m learning!"

# 📥 Check for new message from gateway
def get_latest_sms():
    with imaplib.IMAP4_SSL("imap.gmail.com") as imap:
        imap.login(EMAIL, APP_PASSWORD)
        imap.select("inbox")
        status, messages = imap.search(None, f'(UNSEEN FROM "{PHONE_EMAIL}")')
        if messages[0]:
            latest_id = messages[0].split()[-1]
            _, msg_data = imap.fetch(latest_id, "(RFC822)")
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        return part.get_payload(decode=True).decode().strip()
            else:
                return msg.get_payload(decode=True).decode().strip()
        return None

# 📤 Send SMS response via Gmail
def send_sms(reply):
    msg = EmailMessage()
    msg.set_content(reply)
    msg["From"] = EMAIL
    msg["To"] = PHONE_EMAIL
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL, APP_PASSWORD)
        smtp.send_message(msg)

# 🚀 Startup message
send_sms("✅ Offline chatbot is online. Say something!")

# 🔁 Loop to check messages and reply
while True:
    try:
        prompt = get_latest_sms()
        if prompt:
            print("📩 New message received!")
            print("User:", prompt)
            response = get_local_response(prompt)
            print("🧠 Reply:", response)
            send_sms(response)
        else:
            print("📭 No new messages.")
    except Exception as e:
        print("⚠️ Error:", str(e))
    time.sleep(10)