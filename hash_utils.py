def hashfile(file, hasher, blksz=65536):
    buf = file.read(blksz)
    while len(buf) > 0:
        hasher.update(buf)
        buf = file.read(blksz)
    return hasher.digest()


