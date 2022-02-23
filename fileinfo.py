import sys
import os
import hashlib
import zlib


def main():
    path = str(sys.argv[1])

    hashes = {
        'crc32': True,
        'md5': True,
        'sha1': True,
        'sha256': False,
        'sha512': False
    }

    chosen = []
    for key, value in hashes.items():
        if value:
            chosen.append(key)

    show_header()
    list_files(path)

    with open(output, 'r', encoding='utf-8') as list:
        crc = ''
        for file in list:
            if "crc32" in chosen:
                crc = calc_crc32(file.rstrip('\r\n'))
            hashes = '\t'.join(filter(None, calc_hashlib(file.rstrip('\r\n'), chosen)))
            with open("hashed.tsv", 'a', encoding='utf-8') as fout:
                filet = file.rstrip('\r\n')
                filesize = str(os.stat(filet).st_size)
                data = filet, filesize, crc, hashes
                fout.write("\t".join(filter(None, data)))
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


def calc_crc32(file):
    with open(file, 'rb') as fin:
        crc32 = 0
        while True:
            s = fin.read(65536)
            if not s:
                break
            crc32 = zlib.crc32(s, crc32)
        return "%08X" % (crc32 & 0xFFFFFFFF)


def calc_hashlib(file, chosen, block_size=64 * 128, human_readable=True):
    results = []
    for hash in chosen:
        if hash != "crc32":
            current = eval("hashlib."+hash+"()")
            with open(file, 'rb') as fin:
                for chunk in iter(lambda: fin.read(block_size), b''):
                    current.update(chunk)
                results.append(current.hexdigest())
    return results


if __name__ == '__main__':
    main()
