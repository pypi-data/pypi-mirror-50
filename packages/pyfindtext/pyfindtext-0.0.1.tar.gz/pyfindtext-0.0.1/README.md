# pyfindtext
[![Coverage Status](https://coveralls.io/repos/github/lagliam/pyfindtext/badge.svg)](https://coveralls.io/github/lagliam/pyfindtext)
[![Build Status](https://travis-ci.org/lagliam/pyfindtext.svg?branch=master)](https://travis-ci.org/lagliam/pyfindtext)

Find a string of text in any file located in a directory.

Searches through multiple files that are in a directory and returns the file
, line number, and a print out of the row where the text was found.

In the case of multiple hits, a list of lists is returned.

## Installation
Works on Python 3.7+

`pip install pyfindtext`

## Usage

```
import pyfindtext

result = pyfindtext.find(directory=/path/to/dir, text=search_string)
for x in result:
    print(x)
```