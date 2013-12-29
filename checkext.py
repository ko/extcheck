#!/usr/bin/python

import hashlib
import os
import argparse
import csv

import list_utils
import hash_utils

def populate_flist(extension=''):
    flist = []
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith((extension)):
                path = os.path.join(root,file)
                flist.append(path)
    return flist

def flist_to_clist(flist=[]):
    return [(fname, "".join('%02x' % ord(c) for c in hash_utils.hashfile(open(fname, 'rb'), hashlib.sha256()))) for fname in flist]


# TODO check for duplicates
def write_clist_to_csv(clist=[]):
    for pair in clist:
        dirpath = os.path.dirname(pair[0])
        # TODO cksumfile per file
        cksum_file = os.path.join(dirpath,cksumfile)
        # XXX complicates csv.writer?
        if (os.path.exists(cksum_file) == False):
            f = open(cksum_file, 'w')
        else:
            f = open(cksum_file, 'a')
        s = "%(name)s,%(csum)s\n" % {'name':pair[0], 'csum':pair[1]}
        f.write(s)
        f.close()
    if False:
        write_clist_to_csv_discrete(cksumdir, cksumext, clist)
    return len(clist)

def write_clist_to_csv_discrete(dir, ext, clist=[]):
    if os.path.exists(dir) == False:
        # mkdir
    # cd dir
    # foreach pair in clist; do echo $pair > $pair[0].$extension; done
        return
    return


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rmdb', 
                        action='store_true',
                        help='remove checksum database files')
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

def rmdb():
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith(cksumfile):
                os.remove(os.path.join(root,file))

def print_cksumfile(path):
    with open(path, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            print row

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

def printdb():
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith(cksumfile):
                print_cksumfile(os.path.join(root,file))

def print_verify_notice(count):
    fullpath = os.path.join(os.getcwd(),corruptlistfile) 
    print '%(count)s corrupt file(s) found' % {'count':count}
    if count is not 0:
        print 'for more details, check %(file)s' % {'file':fullpath}

def print_ext_notice(count):
    print '%(count)s files recorded' % {'count':count}

def handle_args(args):
    if vars(args)['rmdb'] is True:
        rmdb()
        return
    if vars(args)['list'] is True:
        printdb()
        return
    if vars(args)['verify'] is True:
        corrupt_list = verifydb()
        count = list_utils.write_to_csv(corruptlistfile, corrupt_list)
        print_verify_notice(count)
        return
    if vars(args)['ext'] is not None:
        flist = populate_flist(vars(args)['ext'])
        clist = flist_to_clist(flist)
        count = write_clist_to_csv(clist)
        print_ext_notice(count)
        return


corruptlistfile='corrupt'
cksumfile   = '.cksum'
cksumdir    = '.cksums'
cksumext    = '.chk'

args = parse_args()
handle_args(args)


