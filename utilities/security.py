from cryptography.fernet import Fernet
import base64
import logging
import traceback
from django.conf import settings


def encrypt(passcode):
    try:
        passcode = str(passcode) # convert integer etc to string first
        cipher_suite = Fernet(settings.ENCRYPT_KEY) # get encryption key from settings
        ciphertext = cipher_suite.encrypt(passcode.encode('ascii'))# convert ciphertext to byte
        ciphertext = base64.urlsafe_b64encode(ciphertext).decode("ascii")# encode to urlsafe format
        return ciphertext
    except Exception as e:
        logging.getLogger("error_logger").error(traceback.format_exc())# log any errors
        return None


def decrypt(passcode):
    try:
        passcode = base64.urlsafe_b64decode(passcode) # base64 decode
        cipher_suite = Fernet(settings.ENCRYPT_KEY)
        plaintext = cipher_suite.decrypt(passcode).decode("ascii")     
        return plaintext
    except Exception as e:
        logging.getLogger("error_logger").error(traceback.format_exc()) # log any errors
        return None