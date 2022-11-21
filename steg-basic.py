import sys
import os

file_end = {
    ".png": b'\x00\x00\x00\x00\x49\x45\x4e\x44\xae\x42\x60\x82',
    ".jpg": b'\xff\xd9'
}

def append_secret(filename, file_extension, secret):
    with open(f"{filename}{file_extension}", "ab") as f:
        f.write(bytes(secret, encoding="utf-8"))

def retrieve_secret(filename, file_extension):
    with open(f"{filename}{file_extension}", 'rb') as f:
        buff = bytes(f.read())
        index = buff.index(file_end[file_extension])
        return buff[index+len(file_end[file_extension]):].decode('utf-8')

def clear_secret(filename, file_extension):
    with open(f"{filename}{file_extension}", 'rb+') as f:
        buff = bytes(f.read())
        index = buff.index(file_end[file_extension])
        f.truncate(index+len(file_end[file_extension]))

def help():
    print("""
    Usage: python main.py <mode> <image> [<message>]

    mode: mode to use
    -a: --append
    -r: --retrieve
    -c: --clear
    image: image file (png|jpg)
    message: secret message to hide (only on mode a)
    """)

if __name__=="__main__":
    request = sys.argv[1]
    filename, file_extension = os.path.splitext(sys.argv[2])

    if request == "-a" or request == "--append":
        append_secret(filename, file_extension, sys.argv[3])
    elif request == "-r" or request == "--retrieve":
        secret = retrieve_secret(filename, file_extension)
        print(secret)
    elif request == "-c" or request == "--clear":
        clear_secret(filename, file_extension)
    else:
        print("[!] Incorrect mode selected!")
        help()
        sys.exit()

    if not file_extension in file_end:
        print("[!] Image file format not supported!")
        help()
        sys.exit()
