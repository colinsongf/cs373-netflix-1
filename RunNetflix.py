#!/usr/bin/env python3

# -------
# imports
# -------

import sys

from Netflix import netflix_solve

# ----
# main
# ----

if __name__ == "__main__" :
    netflix_solve(sys.stdin, sys.stdout)

"""
% cat RunNetflix.in
1 10
100 200
201 210
900 1000



% RunNetflix.py < RunNetflix.in > RunNetflix.out



% cat RunNetflix.out
1 10 1
100 200 1
201 210 1
900 1000 1



% pydoc3 -w Netflix
# That creates the file Netflix.html
"""
