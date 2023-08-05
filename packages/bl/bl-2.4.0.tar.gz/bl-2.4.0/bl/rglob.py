
import logging
log = logging.getLogger(__name__)

import os
from glob import glob
try:
    from glob import escape
except:                                                 # support Python < 3.4
    import re
    magic_check = re.compile('([*?[])')
    def escape(s):
        drive, pathname = os.path.splitdrive(s)
        pathname = magic_check.sub(r'[\1]', pathname)
        return drive + pathname

def rglob(dirname, pattern, dirs=False, sort=True):
    """recursive glob, gets all files that match the pattern within the directory tree"""
    fns = []
    path = str(dirname)
    if os.path.isdir(path):
        fns = glob(os.path.join(escape(path), pattern))
        dns = [fn for fn 
                in [os.path.join(path, fn)
                    for fn in os.listdir(path)] 
                if os.path.isdir(fn)]
        if dirs==True:
            fns += dns
        for d in dns:
            fns += rglob(d, pattern)
        if sort==True:
            fns.sort()
    else:
        log.warn("not a directory: %r" % path)
    return fns
