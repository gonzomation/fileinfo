import sys
import os
import hashlib


def main():
    path = str(sys.argv[1])
    show_header()
    list_files(path)
    with open(output, 'r', encoding='utf-8') as list:
        for file in list:
            md5 = calc_hashes(file.rstrip('\r\n'))
            with open("hashed.tsv", 'a', encoding='utf-8') as fout:
                filet = file.rstrip('\r\n')
                data = f"{filet}\t{md5}"
                fout.write(''.join(data))
                fout.write("\n")


def show_header():
    print("----------------------------------")
    print("   FileInfo")
    print("----------------------------------")


def list_files(path):
    global output
    output = os.path.join(os.getcwd(), 'list.txt')

    for cwd, subdirs, files in os.walk(path):
        for file in files:
            with open(output, 'a', encoding='utf-8') as fout:
                fout.write(os.path.join(cwd, file))
                fout.write('\n')

    return output


def calc_hashes(file, block_size=64 * 128, human_readable=True):
    md5 = hashlib.md5()
    with open(file, 'rb') as fin:
        for chunk in iter(lambda: fin.read(block_size), b''):
            md5.update(chunk)
    if human_readable:
        return md5.hexdigest()
    return md5.digest()


if __name__ == '__main__':
    main()
