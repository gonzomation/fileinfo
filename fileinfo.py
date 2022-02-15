import sys
import os
import hashlib


def main():
    file = str(sys.argv[1])
    show_header()
    md5 = calc_hashes(file)
    print(f"md5 of {file} is {md5}")


def show_header():
    print("----------------------------------")
    print("   FileInfo")
    print("----------------------------------")


def calc_hashes(path, block_size=64 * 128, human_readable=True):
    md5 = hashlib.md5()
    with open(path, 'rb') as fin:
        for chunk in iter(lambda: fin.read(block_size), b''):
            md5.update(chunk)
    if human_readable:
        return md5.hexdigest()
    return md5.digest()


if __name__ == '__main__':
    main()
