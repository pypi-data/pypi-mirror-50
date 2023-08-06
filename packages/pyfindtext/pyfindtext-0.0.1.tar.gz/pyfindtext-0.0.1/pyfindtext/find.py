"""
This script will search all files in a directory for a regex criteria
defined by search_regex variable.
If found it will exit with status code 2 with the file it was found
If not found it will exit with status code 0 and print, Not found in files

Requires python 3.7
"""

import os
import glob
import re


def find(directory=None, text=None):
    return work(directory, text)


def work(d, t):
    os.chdir(d)
    files = glob.glob('*.*')
    search_regex = r'.{}.'.format(t)
    results = []
    for f in files:
        with open(f, 'rb') as file:
            print('checking ' + str(file.name))
            path = os.path.abspath(file.name)
            line_num = 0
            for row in file:
                line_num += 1
                try:
                    r = row.decode()
                except UnicodeDecodeError as e:
                    print('!------------Error-------------!')
                    print(str(e.reason))
                    print('Error Reading File: '+path+' Skipping')
                    print('!----------End Error-----------!')
                    continue
                found = re.search(search_regex, r)
                if found:
                    results.append([str(path), line_num, r])
                    print('found in file '+str(path))
                    print('Line {num}>>>{row}'.format(
                        num=str(line_num), row=r))
                else:
                    continue
    return results
