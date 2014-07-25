#!/usr/bin/env python

# Script to untrust all the built-in Firefox root CA's.
# Usage: python untrustFF.py [path to FF profile directory]
# If the FF directory is unspecified, this will default to
# ~/.mozilla/firefox/*default

import os
import sys
import glob
import urllib2
import re
import subprocess

#exename = r"certutil"
exename = r"C:\EXTRACT\NSS-3.14.2\NSS-3.14.2\certutil.exe"


if len(sys.argv) > 1:
    PROFILEDIR = sys.argv[1]
else:
    defaults = glob.glob(os.path.join(os.getenv('APPDATA'), "Mozilla/Firefox/Profiles/*default")) if sys.platform.startswith("win") else glob.glob(os.path.expanduser("~/.mozilla/firefox/*default"))
    if len(defaults) >= 1:
        PROFILEDIR = defaults[0]
        sys.stderr.write("using default Firefox profile %s\n" % PROFILEDIR)
    else:
        sys.stderr.write("must specify a Firefox profile directory\n")
        sys.exit(1)

FF_URL = 'https://mxr.mozilla.org/mozilla/source/security/nss/lib/ckfw/builtins/certdata.txt?raw=1F'

def get_CA_names():
    try:
        f = urllib2.urlopen(FF_URL)
    except:
        sys.stderr.write("Could not open %s" % FF_URL)
        sys.exit(1)
    pattern = r'(?:# Certificate )"([^"]*)"'
    for line in f:
        m = re.search(pattern, line)
        if m:
            #print line
            yield m.group(1)

def revoke_trust():
    for name in get_CA_names():
        try:
            #print name
            #subprocess.call(['certutil', '-A', '-n', name,
            #                 '-t', 'c,c,c', '-d', PROFILEDIR])
            print '%s -M -n "Builtin Object Token:%s" -t p,p,p -d %s' % (exename, name, PROFILEDIR)
            #subprocess.call([exename, '-M', '-n', 'Builtin Object Token:%s' % name, '-t', 'p,p,p', '-d', PROFILEDIR])
        except OSError:
            sys.stderr.write("Could not edit FF cert file; is libnss3-tools installed?")
            sys.exit(1)
    sys.stderr.write('List CA:\n%s -L -h "Builtin Object Token" -d %s' % (exename, PROFILEDIR))

revoke_trust()
