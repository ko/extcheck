#!/usr/bin/python

import hashlib
import os
import argparse
import csv

def hashfile(file, hasher, blksz=65536):
    buf = file.read(blksz)
    while len(buf) > 0:
        hasher.update(buf)
        buf = file.read(blksz)
    return hasher.digest()

def populate_flist(extension=''):
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

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--resetdb', 
                        action='store_true',
                        help='reset checksum database files')
    parser.add_argument('--ext',
                        help='file extension to target')
    parser.add_argument('--verify',
                        action='store_true',
                        help='verify files and stored checksums')
    parser.add_argument('--list',
                        action='store_true',
                        help='list checksum db contents')
    args = parser.parse_args()
    return args

def resetdb():
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith(cksumfile):
                os.remove(os.path.join(root,file))

def list_line(line):
    print line

def list_cksumfile(path):
    with open(path, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            list_line(row)

def verify_line(line):
    flist = [line[0]]
    clist = flist_to_clist(flist)
    if line[1].lower() != clist[0][1].lower():
        line.append(clist[0][1])
        return line
    else:
        return None

def verify_cksumfile(path):
    with open(path, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            mismatch = verify_line(row) 
            if mismatch is not None:
                print mismatch

def verifydb():
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith(cksumfile):
                verify_cksumfile(os.path.join(root,file))

def listdb():
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith(cksumfile):
                list_cksumfile(os.path.join(root,file))
 
def handle_args(args):
    if vars(args)['resetdb'] is True:
        resetdb()
        return
    if vars(args)['list'] is True:
        listdb()
        return
    if vars(args)['verify'] is True:
        verifydb()
        return
    if vars(args)['ext'] is not None:
        flist = populate_flist(vars(args)['ext'])
        clist = flist_to_clist(flist)
        handle_clist(clist)
        return


cksumfile='.cksum'

args = parse_args()
handle_args(args)


