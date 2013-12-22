#!/usr/bin/python

import hashlib

def hashfile(file, hasher, blksz=65536):
    buf = file.read(blksz)
    while len(buf) > 0:
        hasher.update(buf)
        buf = file.read(blksz)
    return hasher.digest()

flist = ['test/2011-01-01/a.JPG']

clist = [(fname, "".join('%02x' % ord(c) for c in hashfile(open(fname, 'rb'), hashlib.sha256()))) for fname in flist]

print clist
