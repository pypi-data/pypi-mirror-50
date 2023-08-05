"""
The String() class provided in this library allows a more object-oriented usage pattern and adds 
several convenience methods that are not available in the standard library. String() inherits from 
str and overrides all of its methods that return strings, so that the return value is itself a 
String(), which enables chaining. For example:

>>> s = String('In the beginning God created')
>>> s.titleify()                    # knows English capitalization rules, can be taught other languages.
'In the Beginning God Created'
>>> _.hyphenify()                   # adds hyphens
'In-the-Beginning-God-Created'
>>> s                               # the original string is not changed -- immutability by default
'In the beginning God created'
"""

import re, urllib.parse

# articles, conjunctions, prepositions, the s in 's
LOWERCASE_WORDS = {
    'en': """a an the and or nor for but than because vs to in on off from at of by under over 
            through with against about across aboard above according after along alongside amid 
            among apart around beneath beyond below beside behind before between concerning despite 
            during into near onto throughout toward until unto upon versus via within without s amp 
            n v adj adv prep ed ing eth th""".split()
}


class String(str):
    """our own str string class that adds several useful methods"""

    def digest(self, alg='sha256', b64=True, strip=True):
        """return a url-safe hash of the string, optionally (and by default) base64-encoded
            alg='sha256'    = the hash algorithm, must be in hashlib
            b64=True        = whether to base64-encode the output
            strip=True      = whether to strip trailing '=' from the base64 output
        Using the default arguments returns a url-safe base64-encoded SHA-256 hash of the string.
        Length of the digest with different algorithms, using b64=True and strip=True:
            * SHA224 = 38 
            * SHA256 = 43 (DEFAULT)
            * SHA384 = 64
            * SHA512 = 86
        """
        import base64, hashlib

        h = hashlib.new(alg)
        h.update(str(self).encode('utf-8'))
        if b64 == True:
            # this returns a string with a predictable amount of = padding at the end
            b = base64.urlsafe_b64encode(h.digest()).decode('ascii')
            if strip == True:
                b = b.rstrip('=')
            return b
        else:
            return h.hexdigest()

    def base64(self):
        import base64 as b64

        return b64.urlsafe_b64encode(bytes(self, encoding='utf-8'))

    def camelify(self):
        """turn a string to CamelCase, omitting non-word characters"""
        outstring = self.titleify(allwords=True)
        outstring = re.sub(r"&[^;]+;", " ", outstring)
        outstring = re.sub(r"\W+", "", outstring)
        return String(outstring)

    def titleify(self, lang='en', allwords=False, lastword=True, asis=None):
        """takes a string and makes a title from it"""
        if asis is None:
            asis = []
        if lang in LOWERCASE_WORDS:
            lc_words = LOWERCASE_WORDS[lang]
        else:
            lc_words = []
        s = str(self).strip()
        l = re.split(r"([_\W]+)", s)
        for i in range(len(l)):
            if l[i] in asis:
                continue
            l[i] = l[i].lower()
            if i==0 or re.match(r'.*[\.\u2013\u2014:\?\!]$', l[i-1].strip()) is not None:
                is_firstword = True
            else:
                is_firstword = False
            if (allwords == True or is_firstword == True or (lastword == True and i == len(l) - 1)
                    or l[i].lower() not in lc_words):
                w = l[i]
                if len(w) > 1:
                    w = w[0].upper() + w[1:]
                else:
                    w = w.upper()
                l[i] = w
        s = "".join(l)
        return String(s)

    def identifier(self, camelsplit=False, ascii=True):
        """return a python identifier from the string (underscore separators)"""
        return self.nameify(camelsplit=camelsplit, ascii=ascii, sep='_')

    def tagify(self):
        """lowercase, hyphen-separated string, useful for XML tags."""
        return self.nameify().lower()

    def nameify(self, camelsplit=False, ascii=True, sep='-'):
        """return an XML name (hyphen-separated by default, initial underscore if non-letter)"""
        s = String(str(self))  # immutable
        if camelsplit == True:
            s = s.camelsplit()
        s = s.hyphenify(ascii=ascii).replace('-', sep)
        if len(s) == 0 or re.match("[A-Za-z_]", s[0]) is None:
            s = "_" + s
        return String(s)

    def hyphenify(self, ascii=False):
        """Turn non-word characters (incl. underscore) into single hyphens.
        If ascii=True, return ASCII-only.
        If also lossless=True, use the UTF-8 codes for the non-ASCII characters.
        """
        s = str(self)
        s = re.sub("""['"\u2018\u2019\u201c\u201d]""", '', s)  # quotes
        s = re.sub(r'(?:\s|%20)+', '-', s)  # whitespace
        if ascii == True:  # ASCII-only
            s = s.encode('ascii', 'xmlcharrefreplace').decode('ascii')  # use entities
        s = re.sub("&?([^;]*?);", r'.\1-', s)  # entities
        s = s.replace('#', 'u')
        s = re.sub(r"\W+", '-', s).strip(' -')
        return String(s)

    def camelsplit(self):
        """Turn a CamelCase string into a string with spaces"""
        s = str(self)
        for i in range(len(s) - 1, -1, -1):
            if i != 0 and (
                (s[i].isupper() and s[i - 1].isalnum() and not s[i - 1].isupper())
                or (s[i].isnumeric() and s[i - 1].isalpha())
            ):
                s = s[:i] + ' ' + s[i:]
        return String(s.strip())

    def words(self):
        l = [String(w) for w in re.split(r"\s+", str(self))]
        return l

    def __add__(self, other):
        return String(str(self) + str(other))

    # add regexp methods as re*
    def refindall(self, pattern, flags=0):
        return [String(s) for s in re.findall(pattern, self, flags=flags)]

    def research(self, pattern, flags=0):
        return re.search(pattern, self, flags=flags)

    def rematch(self, pattern, flags=0):
        return re.match(pattern, self, flags=flags)

    def resplit(self, pattern, maxsplit=0, flags=0):
        return [String(s) for s in re.split(pattern, self, maxsplit=maxsplit, flags=flags)]

    def resub(self, pattern, repl, count=0, flags=0):
        return String(re.sub(pattern, repl, self, count=count, flags=flags))

    def resubn(self, pattern, repl, count=0, flags=0):
        s, n = re.subn(pattern, repl, self, count=count, flags=flags)
        return (String(s), n)

    # override common string methods to return String() rather than str
    def capitalize(self):
        return String(str.capitalize(self))

    def casefold(self):
        return String(str.casefold(self))

    def center(self, *args):
        return String(str.center(self, *args))

    def encode(self, **kwargs):
        return str.encode(self, **kwargs)

    def expandtabs(self, *tabsize):
        return String(str.expandtabs(self, *tabsize))

    def find(self, sub, *args):
        return String(str.find(self, sub, *args))

    def format(self, *args, **kwargs):
        return String(str.format(self, *args, **kwargs))

    def format_map(self, mapping):
        return String(str.format_map(self, mapping))

    def index(self, sub, *args):
        return String(str.index(self, sub, *args))

    def join(self, iterable):
        return String(str.join(self, iterable))

    def ljust(self, width, *fillchar):
        return String(str.ljust(self, width, *fillchar))

    def lower(self):
        return String(str.lower(self))

    def lstrip(self, *chars):
        return String(str.lstrip(self, *chars))

    def replace(self, old, new, *count):
        return String(str.replace(self, old, new, *count))

    def rfind(self, sub, *args):
        return String(str.rfind(self, sub, *args))

    def rindex(self, sub, *args):
        return String(str.rindex(self, sub, *args))

    def rjust(self, width, *fillchar):
        return String(str.rjust(self, width, *fillchar))

    def rsplit(self, **kwargs):
        return String(str.rsplit(self, **kwargs))

    def rstrip(self, *chars):
        return String(str.rstrip(self, *chars))

    def split(self, arg):
        return [String(s) for s in str.split(arg)]

    def splitlines(self, *keepends):
        return [String(l) for l in str.splitlines(self, *keepends)]

    def strip(self, *chars):
        return String(str.strip(self, *chars))

    def swapcase(self):
        return String(str.swapcase(self))

    def title(self):
        return String(str.title(self))

    def translate(self, mapping):
        return String(str.translate(self, mapping))

    def upper(self):
        return String(str.upper(self))

    def zfill(self, width):
        return String(str.zfill(self, width))


if __name__ == '__main__':
    import doctest

    doctest.testmod()
