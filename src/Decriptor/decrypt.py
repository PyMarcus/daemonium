# !/usr/bin/python
import base64
import os
import time

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from getpass import getuser
import argparse
from argparse import Namespace
from pathlib import Path


class Decrypt:
    """
    Decrypts files that have the extension
    left by the malware, therefore using
    the private key.
    """
    def __init__(self, file: str) -> None:
        self.__file: str = file

    @staticmethod
    def __parser() -> Namespace:
        parser = argparse.ArgumentParser(prog="decrypt",
                                         description="Decrypt files, but to do this, pass private key",
                                         epilog="Created by Marcus")
        parser.add_argument("-f", "--file", help="private key", required=True)
        args = parser.parse_args()
        return args.file

    def start(self) -> None:
        try:
            privatekey: str = str(self.__parser())  # ../../Keys/private_key.pem
            with open(privatekey, 'rb') as f:
                private_key = RSA.import_key(f.read())
            cipher = PKCS1_OAEP.new(private_key)
            decrypted_data = bytearray()
        except FileNotFoundError as e:
            print("[-] File not found")

        with open(self.__file, 'rb') as f:
            while True:
                try:
                    chunk = f.read(cipher._key.size_in_bytes())
                    if not chunk:
                        break
                    decrypted_chunk = cipher.decrypt(chunk)
                    decrypted_data.extend(decrypted_chunk)
                except Exception as e:
                    ...

        with open(self.__file, 'wb') as f:
            f.write(decrypted_data)
            print(f"[+] Decrypting {self.__file}")


def find_crypto_files() -> None:
    home: str = os.path.join(os.path.expanduser('~'), r'Documents/ransomTests')
    for root, dirs, files in os.walk(home):
        for names in files:
            if ".666" == Path(os.path.join(root, names)).suffix:
                try:
                    os.rename(os.path.join(root, names), os.path.join(root, names).replace(".666", ""))
                    file: str = os.path.join(root, names).replace(".666", "")
                    time.sleep(0.02)
                    decrypt: Decrypt = Decrypt(file)
                    decrypt.start()
                except Exception as e:
                    ...


if __name__ == '__main__':
    find_crypto_files()
