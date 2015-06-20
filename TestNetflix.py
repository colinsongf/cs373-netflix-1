#!/usr/bin/env python3

# https://docs.python.org/3.4/reference/simple_stmts.html#grammar-token-assert_stmt

# -------
# imports
# -------

from io       import StringIO
from unittest import main, TestCase

from Netflix import netflix_read, netflix_eval, netflix_print, netflix_solve

# -----------
# TestNetflix
# -----------

class TestNetflix (TestCase) :
    # ----
    # read
    # ----

    def test_read (self) :
        s    = "1 10\n"
        i, j = netflix_read(s)
        self.assertEqual(i,  1)
        self.assertEqual(j, 10)

    # ----
    # eval
    # ----

    def test_eval_1 (self) :
        v = netflix_eval(1, 10)
        self.assertEqual(v, 1)

    def test_eval_2 (self) :
        v = netflix_eval(100, 200)
        self.assertEqual(v, 1)

    def test_eval_3 (self) :
        v = netflix_eval(201, 210)
        self.assertEqual(v, 1)

    def test_eval_4 (self) :
        v = netflix_eval(900, 1000)
        self.assertEqual(v, 1)

    # -----
    # print
    # -----

    def test_print (self) :
        w = StringIO()
        netflix_print(w, 1, 10, 20)
        self.assertEqual(w.getvalue(), "1 10 20\n")

    # -----
    # solve
    # -----

    def test_solve (self) :
        r = StringIO("1 10\n100 200\n201 210\n900 1000\n")
        w = StringIO()
        netflix_solve(r, w)
        self.assertEqual(w.getvalue(), "1 10 1\n100 200 1\n201 210 1\n900 1000 1\n")

# ----
# main
# ----

if __name__ == "__main__" :
    main()

"""
% coverage3 run --branch TestNetflix.py >  TestNetflix.out 2>&1



% coverage3 report -m                   >> TestNetflix.out



% cat TestNetflix.out
.......
----------------------------------------------------------------------
Ran 7 tests in 0.001s

OK
Name          Stmts   Miss Branch BrMiss  Cover   Missing
---------------------------------------------------------
Netflix          18      0      6      0   100%
TestNetflix      33      1      2      1    94%   79
---------------------------------------------------------
TOTAL            51      1      8      1    97%
"""
