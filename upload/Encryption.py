#############################################################################
# Author: Kyle Hays
# Date: 4/25/2018
# requirements: cryptography
# abstract: This function encrypt takes in a username and password as strings
#           and encrypts it to a plain text file.
#           The text can then be decrypted using the decrypt function and is
#           returned as a list of 2 strings.
#############################################################################


###imports###################################################################
from cryptography.fernet import Fernet
import getpass
#############################################################################


####encrypt##################################################################
# This method takes in two string objects to be encrypted.
# The strings are saved in a text file called user.txt
# The key for decryption is saved as info.txt
#############################################################################
def encrypt(username, password):
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)

    username_bytes = bytes(username, 'utf-8')
    password_bytes = bytes(password, 'utf-8')
    space = bytes('\n', 'utf-8')

    cipher_text_password = cipher_suite.encrypt(password_bytes)
    cipher_text_username = cipher_suite.encrypt(username_bytes)

    with open("user.txt", "wb") as text_file:
        text_file.write(cipher_text_username)
        text_file.write(space)
        text_file.write(cipher_text_password)

    with open("info.txt", "wb") as text_file2:
        text_file2.write(key)

    print("Encryption complete")


###decrypt###################################################################
# This method takes no arguments and decrypts the encrypted strings.
# The method will find the key from the info.txt file.
# It will decrypt the strings and return them as a list of two strings.
#############################################################################
def decrypt():
    in_key = open("info.txt", "rb")
    key = in_key.read()
    cipher_suite = Fernet(key)

    split_list = []
    decrypt_list = []

    in_file = open("user.txt", "rb")
    data = in_file.read()
    split_list =data.split(b'\n')
    for item in split_list:
        decrypt_list.append(cipher_suite.decrypt(item).decode('utf-8'))


###Test Code#################################################################
# username = input("Enter your username: ")
# password = getpass.getpass("Enter your password: ")
#
# encrypt(username,password)
# items = decrypt()
# print(items)
#############################################################################
