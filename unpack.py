#!/usr/bin/env python3

import sys
import os
import shutil
import subprocess

def unpack_upx(src):
    if not shutil.which('upx'):
        print('upx not found in path. Aborting..')
        sys.exit(1)
    
    dst = f'{src}.unpacked'
    shutil.copy(src, dst)

    with open(dst, 'r+b') as f:
        def patch(offset, whence):
            f.seek(offset, whence)
            f.write(b'UPX')

        patch(0xec, os.SEEK_SET)
        patch(-0x2e, os.SEEK_END)
        patch(-0x24, os.SEEK_END)
    
    upx = subprocess.run(['upx', '-d', dst])

    if upx.returncode != 0:
        os.remove(dst)

def show_usage():
    print(f"{sys.argv[0]} [file path]")

def main():
    if len(sys.argv) != 2:
        show_usage()
        sys.exit(0)
    
    unpack_upx(sys.argv[1])

if __name__ == '__main__':
    main()