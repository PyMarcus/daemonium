#!bin/bash/python
import asyncio
from Crypto.PublicKey import RSA
import aiofiles

KEY = RSA.generate(2048)  # length of the key (recommended 2048)
PRIVATE_KEY = KEY.export_key()
PUBLIC_KEY = KEY.publickey().export_key()


if __name__ == '__main__':

    async def private_key_rsa() -> None:
        async with aiofiles.open(r"../Keys/private_key.pem", "wb") as private:
            await private.write(PRIVATE_KEY)
        print("[+] SUCCESSFULLY Create private key")


    async def public_key_rsa() -> None:
        async with aiofiles.open(r"../Keys/public_key.pem", "wb") as public:
            await public.write(PUBLIC_KEY)
        print("[+] SUCCESSFULLY Create public key")

    a = asyncio.get_event_loop()
    a.run_until_complete(public_key_rsa())
    a.run_until_complete(private_key_rsa())
