import base64
import hashlib
import logging

from Crypto import Random
from Crypto.Cipher import AES


def aes_pad(s, bs):
    """
    Pads the string using the given block size.
    :param s: the string to pad
    :param bs: the block size
    :return: the padded string
    """
    return s + (bs - len(s) % bs) * chr(bs - len(s) % bs)


def aes_unpad(s):
    """
    Unpads the string padded with aes_pad().
    :param s: the string to unpad
    :return: the unpadded string
    """
    return s[:-ord(s[len(s) - 1:])]


def aes_key(key):
    """
    Generate a valid AES key from a string.
    :param key: the key from which generate an AES key
    :return: the AES key
    """
    return hashlib.sha256(key.encode()).digest()


def aes_encrypt(plaintext, iv, key):
    """
    Encrypts a text using the given IV and key.
    :param plaintext: the text to encrypt
    :param iv: the AES initialization vector
    :param key: the key
    :return: the encrypted content
    """
    padded_text = aes_pad(plaintext, AES.block_size)
    cipher = AES.new(aes_key(key), mode=AES.MODE_CBC, IV=iv)
    return base64.b64encode(iv + cipher.encrypt(padded_text))


def aes_decrypt(encrypted_content, key):
    """
    Decrypts an encrypted content using the given key.
    :param encrypted_content: the encrypted content
    :param key: the key
    :return: the plaintext
    """
    decoded_text = base64.b64decode(encrypted_content)
    iv = decoded_text[:AES.block_size]
    cipher = AES.new(aes_key(key), mode=AES.MODE_CBC, IV=iv)
    return aes_unpad(cipher.decrypt(decoded_text[AES.block_size:])).decode("utf-8")
    

def aes_encrypt_file(path, key, content):
    """
    Encrypts a file using AES.
    :param path: the path where store the encrypted file
    :param key: the key
    :param content: the plaintext
    :return: whether the file has been encrypted successfully
    """
    try:
        with open(path, "wb") as file:
            iv = Random.new().read(AES.block_size)
            encrypted_content = aes_encrypt(content, iv, key)
            file.write(encrypted_content)
        return True
    except OSError as e:
        logging.error("AES I/O error", e)
        return False


def aes_decrypt_file(path, key):
    """
    Decrypts a file using AES.
    :param path: the path of the file to decrypt
    :param key: the key
    :return: whether the file has been decrypted successfully
    """
    try:
        with open(path, "rb") as file:
            encrypted_content = file.read()
            plaintext = aes_decrypt(encrypted_content, key)
            return plaintext
    except OSError as e:
        logging.error("AES I/O error", e)
        return False
    except UnicodeError:
        logging.error("AES decrypt error (invalid key?)")
        return False
