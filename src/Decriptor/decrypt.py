from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA


with open('../../Keys/private_key.pem', 'rb') as f:
    private_key = RSA.import_key(f.read())

cipher = PKCS1_OAEP.new(private_key)
decrypted_data = bytearray()




with open('../Ransomware/arquivo.jpg', 'rb') as f:
    while True:
        chunk = f.read(cipher._key.size_in_bytes())
        if not chunk:
            break
        decrypted_chunk = cipher.decrypt(chunk)
        decrypted_data.extend(decrypted_chunk)

with open('../Ransomware/arquivo.jpg', 'wb') as f:
    f.write(decrypted_data)
