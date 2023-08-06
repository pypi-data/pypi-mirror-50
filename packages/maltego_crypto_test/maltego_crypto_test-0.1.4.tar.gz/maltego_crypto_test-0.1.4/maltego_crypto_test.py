"""Maltego OAuth Crypto Helper"""

__version__ = '0.1.4'

from Crypto.Cipher import PKCS1_v1_5, AES
from Crypto.Util.Padding import pad, unpad
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from Crypto import Random
import base64

class MaltegoCrypto(object):
    """
    A Crypto Helper Class for Maltego OAuth Secrets recieved from the Transform Distribution Server

    """
    @staticmethod
    def rsa_decrypt(private_key_path=None, ciphertext=None):
        dsize = SHA.digest_size
        sentinel = Random.new().read(20+dsize)
        ciphertext = base64.b64decode(ciphertext)
        private_key = RSA.import_key(open(private_key_path).read())
        cipher = PKCS1_v1_5.new(private_key)
        plaintext = cipher.decrypt(ciphertext, sentinel)
        return plaintext
    
    @staticmethod
    def aes_decrypt(key=None, ciphertext=None):
        
        BLOCK_SIZE = 16  # Bytes
        pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * \
                    chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
        unpad = lambda s: s[:-ord(s[len(s) - 1:])]

        key = base64.b64decode(key)
        ciphertext = base64.b64decode(ciphertext)
        cipher = AES.new(key, AES.MODE_ECB)
        plaintext = unpad(cipher.decrypt(ciphertext)).decode('utf8')
        return plaintext

    @classmethod
    def decrypt_secrets(cls,private_key_path = None, encoded_ciphertext=None):
        encrypted_fields = encoded_ciphertext.split("$")
        if len(encrypted_fields) == 1 :
            token = cls.rsa_decrypt(private_key_path,encrypted_fields[0])
            token_fieds = { 
                "token":token
            }

        elif len(encrypted_fields) == 2:
            # token
            token = cls.rsa_decrypt(private_key_path,encrypted_fields[0])
            # token_secret 
            token_secret = cls.rsa_decrypt(private_key_path, encrypted_fields[1])
            token_fieds = { 
                "token":token,
                "token_secret": token_secret
            }

        elif len(encrypted_fields) == 3: 
            aes_key = cls.rsa_decrypt(private_key_path, encrypted_fields[2])
            token = cls.aes_decrypt(aes_key, encrypted_fields[0])
            token_secret = cls.aes_decrypt(aes_key,encrypted_fields[1])
            token_fieds = { 
                "token":token,
                "token_secret": token_secret
            }
        elif len(encrypted_fields) == 4:
            # token
            token = cls.rsa_decrypt(private_key_path,encrypted_fields[0])
            # token_secret 
            token_secret = cls.rsa_decrypt(private_key_path, encrypted_fields[1])
            # refresh token 
            refresh_token = cls.rsa_decrypt(private_key_path, encrypted_fields
            [2])
            # expires in 
            expires_in = cls.rsa_decrypt(private_key_path, encrypted_fields
            [3])
            token_fieds = { 
                "token":token,
                "token_secret": token_secret,
                "refresh_token": refresh_token,
                "expires_in": expires_in
            }
        elif len(encrypted_fields) == 5: 
            aes_key = cls.rsa_decrypt(private_key_path, encrypted_fields[4])
            # token
            token = cls.rsa_decrypt(private_key_path,encrypted_fields[0])
            # token_secret 
            token_secret = cls.rsa_decrypt(private_key_path, encrypted_fields[1])
            # refresh token 
            refresh_token = cls.rsa_decrypt(private_key_path, encrypted_fields
            [2])
            # expires in 
            expires_in = cls.rsa_decrypt(private_key_path, encrypted_fields
            [3])
            token_fieds = { 
                "token":token,
                "token_secret": token_secret,
                "refresh_token": refresh_token,
                "expires_in": expires_in
            }
        else: 
            token_fieds = { 
                "token":"",
                "token_secret": "",
                "refresh_token": "",
                "expires_in": ""
            }

        return token_fieds

