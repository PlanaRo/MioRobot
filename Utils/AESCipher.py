from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
import base64


# AES加密类
class AESCipher:
    def __init__(self, key):
        self.key = key

    # 填充数据，使其长度为16的倍数
    def _pad(self, text):
        # AES的块大小是16字节
        block_size = AES.block_size
        padding_length = block_size - len(text) % block_size
        # 使用PKCS7填充
        padding = chr(padding_length) * padding_length
        return text + padding

    # 去除填充
    def _unpad(self, text):
        padding_length = ord(text[-1])
        return text[:-padding_length]

    # 加密函数
    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = get_random_bytes(AES.block_size)  # 生成初始化向量
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        encrypted = cipher.encrypt(raw.encode("utf-8"))
        # 返回加密后的内容（初始化向量 + 加密数据），并进行Base64编码
        return base64.b64encode(iv + encrypted).decode("utf-8")

    # 解密函数
    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[: AES.block_size]  # 提取初始化向量
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(enc[AES.block_size :]).decode("utf-8")
        return self._unpad(decrypted)
