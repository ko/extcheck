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
    # NOTE: to debug, != to ==
    if line[1].lower() != clist[0][1].lower():
        line.append(clist[0][1])
        return line
    else:
        return None

def verify_cksumfile(path):
    corrupt_list = []
    with open(path, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            mismatch = verify_line(row) 
            if mismatch is not None:
                corrupt_list.append(mismatch)
    return corrupt_list

def verifydb():
    corrupt_list = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith(cksumfile):
                corrupt = verify_cksumfile(os.path.join(root,file))
                if corrupt:
                    corrupt_list.extend(corrupt)
    return corrupt_list

def listdb():
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith(cksumfile):
                list_cksumfile(os.path.join(root,file))
 
def write_list_to_file(list):
    if not list:
        return 0
    with open(corruptlistfile, 'wb') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerows(list)
    return len(list)
            
def print_corrupt_notice(count):
    fullpath = os.path.join(os.getcwd(),corruptlistfile) 
    print '%(corrupt)s corrupt file(s) found' % {'corrupt':count}
    if count is not 0:
        print 'for more details, check %(file)s' % {'file':fullpath}

def handle_args(args):
    if vars(args)['resetdb'] is True:
        resetdb()
        return
    if vars(args)['list'] is True:
        listdb()
        return
    if vars(args)['verify'] is True:
        corrupt_list = verifydb()
        count = write_list_to_file(corrupt_list)
        print_corrupt_notice(count)
        return
    if vars(args)['ext'] is not None:
        flist = populate_flist(vars(args)['ext'])
        clist = flist_to_clist(flist)
        handle_clist(clist)
        return


corruptlistfile='corrupt'
cksumfile='.cksum'

args = parse_args()
handle_args(args)


