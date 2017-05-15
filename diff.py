#!/usr/bin/python
import os

for root, dirs, files in os.walk('.'):
    for fname in files:
        fullpath = os.path.join(root, fname)
        print 'find : ', fullpath
