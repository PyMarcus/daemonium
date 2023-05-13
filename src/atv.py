import string
import typing
import requests
from bs4 import BeautifulSoup


ALPHABET: str = string.ascii_lowercase


def get_data_from_repo() -> bytes:
    """Captura o readme do repositorio"""
    return requests.get("https://github.com/PyMarcus/daemonium/blob/main/README.md").content


def get_phrase() -> str:
    """Recupera a frase dos bytes baixados do repositorio"""
    data: bytes = get_data_from_repo()
    bs: BeautifulSoup = BeautifulSoup(data, 'html.parser')
    span_tag: typing.Any = bs.find_all("pre")[-1]
    return str(span_tag.text).strip()


def cesar_cipher_decrypt() -> None:
    """Decodifica a frase com base na cifra de cesar"""
    word: str = str()
    for number in range(26):
        print(f"---" * 30, end=f"Cipher {number}\n")
        for letter in get_phrase():
            if letter == " ":
                word += " "
            elif letter == ".":
                word += '.'
            elif letter == ";":
                word += ';'
            elif letter == ",":
                word += ','
            elif letter == ":":
                word += ':'
            else:
                word += ALPHABET[ALPHABET.index(letter.lower()) - number]
        print(word)
        word = ""


if __name__ == '__main__':
    print(cesar_cipher_decrypt())
