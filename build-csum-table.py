#!/usr/bin/python

import hashlib
import os
import argparse

def hashfile(file, hasher, blksz=65536):
    buf = file.read(blksz)
    while len(buf) > 0:
        hasher.update(buf)
        buf = file.read(blksz)
    return hasher.digest()

def populate_flist():
    flist = []
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith((extension)):
                path = os.path.join(root,file)
                flist.append(path)
    return flist

def flist_to_clist(flist=[]):
    return [(fname, "".join('%02x' % ord(c) for c in hashfile(open(fname, 'rb'), hashlib.sha256()))) for fname in flist]


def handle_clist(clist=[]):
    for pair in clist:
        dirpath = os.path.dirname(pair[0])
        # TODO cksumfile per file
        cksum_file = os.path.join(dirpath,cksumfile)
        if (os.path.exists(cksum_file) == False):
            f = open(cksum_file, 'w')
        else:
            f = open(cksum_file, 'a')
        s = "%(name)s,%(csum)s\n" % {'name':pair[0], 'csum':pair[1]}
        f.write(s)
        f.close()


cksumfile='.cksum'
extension='.JPG'
flist = populate_flist()
clist = flist_to_clist(flist)
handle_clist(clist)


