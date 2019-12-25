# -------------------------------------------------------------------------------
# Name:        addaUtils
# Purpose:     Houses the utility functions used in various other modules
#
# Author:      Mahdi Kefayati
#
# Created:     15/07/2013
# Copyright:   (c) EPE Consulting, 2013
# Licence:     EPE-ADDA
# -------------------------------------------------------------------------------
import sys, os, time, datetime, re, urlparse, urllib, logging
from dateutil import parser as dtparser

atStrip = re.compile(r"^([^@]*)@*")

toNamePhase = lambda name: name.split('@')


def notNone(a): return filter(lambda x: False if x is None else True, a)


def mean(a): return sum(a) / len(a) if len(a) > 0 else None


def lastSecOfMonth(d):
    return (d + datetime.timedelta(days=32)).replace(day=1, hour=23, minute=59, second=59,
                                                     microsecond=999999) - datetime.timedelta(days=1)


def getTimeString(t=None):
    if not t: t = datetime.datetime.now()
    dString = t.strftime("%Y_%m_%d_%H_%M_%S")
    return dString


def timeMessage(tic=0, jobMsg="Last task", log=None, wrt=None):
    """ Prints the the time took to finish the last set of activities.
	"""
    """ Prints the the time took to finish the last set of activities.
	"""
    tick = time.time()
    wrt = sys.stdout.write if wrt is None else wrt
    le = '\n'
    if log:
        if isinstance(log, file):
            wrt = log.write
            le = '\n'
        elif isinstance(log, logging.Logger):
            wrt = log.debug
            le = ''
    if tic:
        jl = tick - tic
        if jl <= 90:
            wrt("%s took %.2f seconds.%s" % (jobMsg, jl, le))
        elif 90 < jl <= (90 * 60):
            wrt("%s took %d minutes and %d seconds.%s" % (jobMsg, jl / 60, jl % 60, le))
        else:
            wrt("%s took %d hours, %d minutes and %d seconds.%s" % (jobMsg, jl / 3600, jl % 3600 / 60, jl % 60, le))
    return tick


def stPh(s):
    """ Strips phase suffix from a node name.
	"""
    return s.split('@')[0]


def parseSubset(s):
    """ Parses the subset selection string to a list of tuples
	"""
    return [(sub.split(',')[0], sub.split(',')[1]) for sub in s.split(';')] if s != '*' else [('*', '*')]


def fieldMap(fields):
    """ Creates a dictionary of field indices
	"""
    # return dict([(fields[i], i) for i in range(len(fields))])
    return dict(zip(fields, range(len(fields))))


def toDict(r, fields):
    """ Converts a field array to a dict
	"""
    # return dict([(fields[i], r[i]) for i in range(len(fields))])
    return dict(zip(fields, r))


def decodeStat(pc):
    """ Maps phase code to status
	"""
    return ('0' if pc.find('A') == -1 else '1') + ('0' if pc.find('B') == -1 else '1') + (
    '0' if pc.find('C') == -1 else '1')


def phaseMatch(phase, parphase):
    # return len([p for p in [(t in parphase) for t in phase] if not p])==0
    return len(phase) > 0 and len([p for p in phase if p not in parphase]) == 0


def initNone(obj, keys):
    """ initiates a dictionary with a list of members to None if they do not exist.
	"""
    for k in keys:
        if not obj.has_key(k): obj[k] = None

def listfind(l, t):
    try:
        r = l.index(t)
    except:
        r = -1
    return r

def floatOrNone(s):
    if s is None: return None
    try:
        f = float(s)
        return f
    except ValueError:
        return None

def intOrNone(s):
    if s is None: return None
    try:
        f = int(s)
        return f
    except ValueError:
        return None


def defIfNone(v, dv):
    return dv if v is None else v


def rowMap(r, spec):
    res = {}
    if len(r) >= len(spec):
        for e in zip(spec, r):
            if e[0] is None or e[0][0] is None:
                continue
            elif len(e[0]) == 1 or e[0][1] is None:
                v = e[1]
            elif type(e[0][1]) == dict:
                v = e[0][1][e[1]] if e[0][1].has_key(e[1]) else e[1]
            elif type(e[0][1]) == type or hasattr(type(e[0][1]), '__call__'):
                v = e[0][1](e[1])
            res[e[0][0]] = v if not (len(e[0]) < 3 and v is None) else e[0][2]
    return res


def path2url(path):
    return urlparse.urljoin('file:', urllib.pathname2url(path))


def wrap(pre, post):
    def decorate(func):
        def call(*args, **kwargs):
            pre(func, *args, **kwargs)
            result = func(*args, **kwargs)
            post(func, *args, **kwargs)
            return result

        return call

    return decorate


def getLogger(name, logFileName, format='%(levelname)s: %(message)s', lvl=logging.INFO):
    logger = logging.getLogger(name)
    if logFileName == sys.stdout:
        lh = logging.StreamHandler(sys.stdout)
    else:
        lh = logging.FileHandler(logFileName, mode='w')
    lh.setFormatter(logging.Formatter(format))
    logger.addHandler(lh)
    logger.setLevel(lvl)
    return logger

def validateTimestamp(s):
    try:
        dt= dtparser.parse(s)
        return True
    except BaseException as e:
        return False

def delKey(d, k):
    if d.has_key(k): del d[k]


def reKey(d, ok, nk):
    if d.has_key(ok):
        d[nk] = d[ok]
        del d[ok]


def orderedUnique(lst):
    return reduce(lambda l, x: l + [x] if x not in l else l, lst, [])


def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    import unicodedata
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
    value = unicode(re.sub('[-\s]+', '-', value))


if __name__ == '__main__':
    pass
