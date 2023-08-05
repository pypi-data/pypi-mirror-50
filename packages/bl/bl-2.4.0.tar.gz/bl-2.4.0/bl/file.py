
import os, re, subprocess, sys, time, traceback, datetime, shutil
from bl.dict import Dict
from bl.string import String
from bl.rglob import rglob

import logging

log = logging.getLogger(__name__)


class File(Dict):
    def __init__(self, fn=None, data=None, ext=None, **args):
        if type(fn) == str:
            fn = self.normpath(fn)
        elif isinstance(fn, self.__class__):
            fn = str(fn)
        if ext is not None:
            fn = os.path.splitext(fn)[0] + ext
        Dict.__init__(self, fn=fn, data=data, **args)

    def __repr__(self):
        return "%s(fn=%r)" % (self.__class__.__name__, self.fn)

    def __str__(self):
        return str(self.fn)

    def __lt__(self, other):
        return self.fn < other.fn

    def open(self):
        subprocess.call(['open', fn], shell=True)

    def read(self, mode='rb'):
        if self.fn is not None and os.path.exists(self.fn):
            with open(self.fn, mode) as f:
                data = f.read()
            return data

    def dirpath(self):
        return self.normpath(os.path.dirname(os.path.abspath(self.fn)))

    @classmethod
    def normpath(C, path):
        p = (
            path.replace('\\ ', ' ')
            .replace('\\(', '(')
            .replace('\\)', ')')
            .replace('\\', '/')
            .strip()
        )
        if p != '/':
            p = p.rstrip('/')
        return p

    @classmethod
    def match(Class, path, pattern, flags=re.I, sortkey=None, ext=None):
        """for a given path and regexp pattern, return the files that match"""
        return sorted(
            [
                Class(fn=fn)
                for fn in rglob(path, f"*{ext or ''}")
                if re.search(pattern, os.path.basename(fn), flags=flags) is not None
                and os.path.basename(fn)[0] != '~'  # omit temp files
            ],
            key=sortkey,
        )

    @property
    def isdir(self):
        return os.path.isdir(str(self.fn))

    @property
    def isfile(self):
        return os.path.isfile(str(self.fn))

    @property
    def exists(self):
        return os.path.exists(str(self.fn))

    def makedir(self):
        os.makedirs(str(self.fn))

    def file_list(self, depth=None):
        fl = []
        if self.isdir:
            for folder in os.walk(self.fn):
                if folder[0] != self.fn:
                    fl.append(File(fn=folder[0]))  # add the folder itself
                for fb in folder[2]:
                    fl.append(File(fn=os.path.join(folder[0], fb)))
        if depth is not None:
            fl = [
                fi for fi in fl if len(os.path.relpath(fi.fn, self.fn).split(os.path.sep)) <= depth
            ]
        return fl

    @property
    def filename(self):
        return self.fn

    @property
    def path(self):
        return self.dirpath()

    @property
    def folder(self):
        from .folder import Folder

        return Folder(self.path)

    @property
    def basename(self):
        return os.path.basename(str(self.fn))

    @property
    def ext(self):
        return self.splitext()[-1]

    @property
    def name(self):
        return self.splitext(fn=self.basename)[0]

    def copy(self, new_fn):
        """copy the file to the new_fn, preserving atime and mtime"""
        new_file = self.__class__(fn=str(new_fn))
        new_file.write(data=self.read())
        new_file.utime(self.atime, self.mtime)
        return new_file

    def clean_filename(self, fn=None, ext=None):
        fn = fn or self.fn or ''
        if fn not in [None, '']:
            return os.path.join(os.path.dirname(fn), self.make_basename(fn=fn, ext=ext)).replace(
                '\\', '/'
            )
        else:
            return fn.replace('\\', '/')

    def make_basename(self, fn=None, ext=None):
        """make a filesystem-compliant basename for this file"""
        fb, oldext = os.path.splitext(os.path.basename(fn or self.fn))
        ext = ext or oldext.lower()
        fb = String(fb).hyphenify(ascii=True)
        return ''.join([fb, ext])

    def splitext(self, fn=None):
        return os.path.splitext(fn or self.fn)

    def relpath(self, dirpath=None):
        return os.path.relpath(self.fn, str(dirpath or self.dirpath())).replace('\\', '/')

    def stat(self):
        return os.stat(self.fn)

    def hash(self, **params):
        d = self.read()
        if d is not None:
            return String(d).digest(**params)

    @property
    def size(self):
        if self.isdir:
            s = (
                subprocess.check_output(['du', '-sh', self.fn])
                .decode('utf-8')
                .split('\t')[0]
                .strip()
            )
            return self.bytes_from_readable_size(s)
        elif self.isfile:
            return self.stat().st_size

    @property
    def last_modified(self):
        return datetime.datetime.fromtimestamp(self.mtime)

    @property
    def mtime(self):
        return self.stat().st_mtime

    @property
    def atime(self):
        return self.stat().st_atime

    def utime(self, atime, mtime):
        os.utime(self.fn, times=(atime, mtime))

    @property
    def mimetype(self):
        from mimetypes import guess_type

        return guess_type(self.fn)[0]

    def tempfile(self, mode='wb', **args):
        "write the contents of the file to a tempfile and return the tempfile filename"
        tf = tempfile.NamedTemporaryFile(mode=mode)
        self.write(tf.name, mode=mode, **args)
        return tfn

    def write(
        self, fn=None, data=None, mode='wb', max_tries=3
    ):  # sometimes there's a disk error on SSD, so try 3x
        def try_write(fd, outfn, tries=0):
            try:
                if fd is None and os.path.exists(self.fn):
                    if 'b' in mode:
                        fd = self.read(mode='rb')
                    else:
                        fd = self.read(mode='r')
                f = open(outfn, mode)
                f.write(fd or b'')
                f.close()
                log.debug('wrote %s' % outfn)
            except:
                log.warn(sys.exc_info()[1])
                if tries < max_tries:
                    log.debug(traceback.format_exc())
                    time.sleep(.1)  # I found 0.1 s gives the disk time to recover. YMMV
                    try_write(fd, outfn, tries=tries + 1)
                else:
                    raise

        outfn = fn or self.fn
        if not os.path.exists(os.path.dirname(outfn)):
            log.debug("creating directory: %s" % os.path.dirname(outfn))
            os.makedirs(os.path.dirname(outfn))
        try_write(data or self.data, outfn, tries=0)

    def delete(self):
        """delete the file from the filesystem."""
        if self.isfile:
            os.remove(self.fn)
        elif self.isdir:
            shutil.rmtree(self.fn)

    SIZE_UNITS = ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y']

    @classmethod
    def readable_size(C, bytes, suffix='B', decimals=1, sep='\u00a0'):
        """given a number of bytes, return the file size in readable units"""
        if bytes is None:
            return
        size = float(bytes)
        for unit in C.SIZE_UNITS:
            if abs(size) < 1024 or unit == C.SIZE_UNITS[-1]:
                return "{size:.{decimals}f}{sep}{unit}{suffix}".format(
                    size=size,
                    unit=unit,
                    suffix=suffix,
                    sep=sep,
                    decimals=C.SIZE_UNITS.index(unit) > 0 and decimals or 0,  # B with no decimal
                )
            size /= 1024

    @classmethod
    def bytes_from_readable_size(C, size, suffix='B'):
        """given a readable_size (as produced by File.readable_size()), return the number of bytes."""
        s = re.split("^([0-9\.]+)\s*([%s]?)%s?" % (''.join(C.SIZE_UNITS), suffix), size, flags=re.I)
        bytes, unit = round(float(s[1])), s[2].upper()
        while unit in C.SIZE_UNITS and C.SIZE_UNITS.index(unit) > 0:
            bytes *= 1024
            unit = C.SIZE_UNITS[C.SIZE_UNITS.index(unit) - 1]
        return bytes
