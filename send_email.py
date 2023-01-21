import smtplib
import imghdr
from email.message import EmailMessage
import os


def send_email(image):
    password = os.environ["SMTP_PASSWORD"]
    email = "officeguyyt@gmail.com"

    email_msg = EmailMessage()
    email_msg["Subject"] = "Camera detected movement!"
    email_msg.set_content("Here is an image.")

    with open(image, "rb") as file:
        content = file.read()

    email_msg.add_attachment(content, maintype="image", subtype=imghdr.what(None, content))

    mail = smtplib.SMTP("smtp.gmail.com", 587) # why not 465?
    mail.ehlo()
    mail.starttls()
    mail.login(email, password)
    mail.sendmail(email, email, email_msg.as_string())
    mail.quit()


if __name__ == "__main__":
    send_email(image="Metro.jpg")
