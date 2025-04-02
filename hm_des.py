import base64
from Cryptodome.Cipher import DES

class BtsHash():
    def __init__(self) -> None:
        self.key = b'btsbrest'
    
    def pad(self, s: bytes, bs=8) -> bytes:
        pad_size = bs - (len(s) % bs)
        return s + bytes([pad_size] * pad_size)

    def unpad(self, s: bytes) -> bytes:
        pad_size = s[-1]
        return s[:-pad_size]

    def encrypt(self, text: str) -> bytes:
        des = DES.new(self.key, DES.MODE_ECB)
        l_text = bytes(text, 'utf-8')
        padded_text = self.pad(l_text)
        encrypted_text = des.encrypt(padded_text)
        return encrypted_text

    def decrypt(self, cipher_text: bytes) -> str:
        des = DES.new(self.key, DES.MODE_ECB)
        text = des.decrypt(cipher_text)
        return self.unpad(text).decode('utf-8')
    
def main():
    chipher = BtsHash()
    #text = 'duri4bmb'
    #chipher_text = chipher.encrypt(text)
    #print(base64.b64encode(cipher_text).decode('utf-8'))
    chipher_text = bytes('dxlsiEWBRvUmZJUbgwpj6w==', 'utf-8')
    
    #print(cipher_text.fromhex)                # b'\xce{\x17\xdd\xf7\xe3\xef\xe1'
    print(chipher.decrypt(chipher_text))


if __name__ == "__main__":
    main()