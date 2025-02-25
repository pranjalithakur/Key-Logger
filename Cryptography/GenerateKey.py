from cryptography.fernet import Fernet

key = Fernet.generate_key()
file = open("encruption_key.txt", "wb")
file.write(key)
file.close()