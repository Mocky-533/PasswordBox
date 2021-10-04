import hashlib

def get_md5(s):
    md = hashlib.md5()
    md.update(s.encode("utf-8"))
    return md.hexdigest()  # hash the login password

def encrypt(psw: str, offset: int) -> str:
    ascii_num = []
    for i in psw:
        ascii_num.append(enascii(ord(i), offset + 15))
    encrypted = [chr(a) for a in ascii_num]
    # print("".join(encrypted))
    return "".join(encrypted)

def decrypt(s: str, offset: int) -> str:
    # encrypted = s.split("|")
    pwd = [chr(deascii(ord(a), offset + 15)) for a in s]
    # print("".join(pwd))
    return "".join(pwd)

def enascii(num: int, offset: int) -> int:
    if num - offset >= 33:
        return num - offset
    else:
        return 93 + num - offset

def deascii(num: int, offset: int) -> int:
    if num + offset <= 126:
        return num + offset
    else:
        return num + offset - 93


if __name__ == '__main__':
    string = '12345'
    encryption = encrypt(string, 30)
    decrypt(encryption, 30)
