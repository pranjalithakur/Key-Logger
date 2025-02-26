# KeyLogger Project

## Overview

This project is a Python-based keylogger tool that collects various pieces of system information and sends them via email. The tool is designed to record keystrokes, capture clipboard contents, take screenshots, record audio from the microphone, and collect system information such as IP addresses and processor details. Additionally, the collected data is encrypted and sent via email, then cleaned up from the local machine. 

> **Warning:** This tool is provided for educational purposes only. Unauthorized use of keyloggers or similar surveillance software is illegal and unethical. Always ensure you have explicit permission before running this tool on any machine.

## Features

- **Keystroke Logging:** Records all key presses and saves them to a log file.
- **System Information:** Gathers and logs system details such as public and private IP addresses, processor info, OS version, and hostname.
- **Clipboard Capture:** Reads and logs the clipboard data.
- **Screenshot Capture:** Takes screenshots and saves them as image files.
- **Audio Recording:** Records audio from the microphone (default duration is 10 seconds).
- **File Encryption:** Encrypts collected log files using Fernet symmetric encryption.
- **Email Transmission:** Sends the captured data (logs, screenshots, and encrypted files) to a specified email address.
- **Cleanup:** Deletes local log files to cover tracks after data has been transmitted.

## Requirements

- **Python 3.x**

### Python Libraries
The following libraries are required:
- `pynput`
- `pywin32`
- `Pillow`
- `sounddevice`
- `scipy`
- `cryptography`
- `requests`

You can install the dependencies via pip:

```bash
pip install pynput pywin32 Pillow sounddevice scipy cryptography requests
```

## Project Structure
```
.
├── Cryptography
│   ├── DecryptFile.py
│   ├── encryption_key.txt
│   └── GenerateKey.py
└── src
    ├── audio.wav
    ├── clipboard.txt
    ├── key_log.txt
    ├── keylogger.exe
    ├── README.md
    ├── screenshot.png
    └── systeminfo.txt
```

### **Cryptography Folder**
- **DecryptFile.py**  
  Python script used to decrypt encrypted files. It utilizes the key stored in `encryption_key.txt` or a key you specify.
  
- **encryption_key.txt**  
  A text file containing the encryption key generated by `GenerateKey.py`. Keep this file secret if you plan to encrypt/decrypt sensitive data.

- **GenerateKey.py**  
  Python script that generates a new Fernet encryption key and writes it to `encryption_key.txt`.

### **Source Folder**
- **audio.wav**  
  An audio recording captured by the keylogger (if audio capture is enabled).

- **clipboard.txt**  
  Clipboard contents captured by the keylogger.

- **key_log.txt**  
  Keystroke log recorded by the keylogger.

- **keylogger.exe**  
  The compiled executable version of the keylogger. It can be run on systems without requiring Python installed (assuming dependencies are bundled).

- **README.md**  
  This documentation file.

- **screenshot.png**  
  A screenshot captured by the keylogger.

- **systeminfo.txt**  
  Collected system information (IP address, OS version, hostname, etc.).


## Usage

1. **Generate an Encryption Key (Optional)**  
   If you wish to use a custom encryption key:
   1. Navigate to the `Cryptography` folder in your terminal.
   2. Run `python GenerateKey.py`.  
   3. A new `encryption_key.txt` will be created or overwritten.

2. **Run the KeyLogger**  
   - Double-click or run `keylogger.exe` (in the `src` folder).  
   - Alternatively, if you have the Python source code, you can run it via `python keylogger.py`.  
   - The keylogger will capture keystrokes, clipboard data, system info, screenshots, and (optionally) audio. Files will be saved in the same folder.

3. **Decrypting Files**  
   - After the keylogger has encrypted files, you can use `DecryptFile.py` in the `Cryptography` folder to decrypt them.  
   - Make sure `encryption_key.txt` is present and contains the correct key.  
   - Run `python DecryptFile.py --file path/to/encrypted_file --key path/to/encryption_key.txt`  
   - The script will produce a decrypted version of the file.