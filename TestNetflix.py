#!/usr/bin/env python3

# https://docs.python.org/3.4/reference/simple_stmts.html#grammar-token-assert_stmt

# -------
# imports
# -------

from io       import StringIO
from unittest import main, TestCase

from collections import OrderedDict 
from Netflix import netflix_read, netflix_eval, netflix_print, netflix_solve

# -----------
# TestNetflix
# -----------

class TestNetflix (TestCase) :
    # ----
    # read
    # ----

    def test_read_1 (self) :
        s    = "2043:\n1417435\n"
        to_predict = netflix_read(s)
        self.assertEqual(1, len(to_predict))
        self.assertEqual(1417435, (to_predict[2043])[0])

    def test_read_2 (self) :
        s    = "2043:\n1417435\n2312054\n462685\n"
        to_predict = netflix_read(s)
        self.assertEqual(1, len(to_predict))
        self.assertEqual(1417435, (to_predict[2043])[0])
        self.assertEqual(2312054, (to_predict[2043])[1])
        self.assertEqual(462685, (to_predict[2043])[2])

    def test_read_2 (self) :
        s    = "2043:\n1417435\n2312054\n462685\n10851:\n1417435\n1234567\n"
        to_predict = netflix_read(s)
        self.assertEqual(2, len(to_predict))
        self.assertEqual(1417435, (to_predict[2043])[0])
        self.assertEqual(2312054, (to_predict[2043])[1])
        self.assertEqual(462685, (to_predict[2043])[2])
        self.assertEqual(1417435, (to_predict[10851])[0])
        self.assertEqual(1234567, (to_predict[10851])[1])

    # ----  
    # get_movie_rating
    # ----

    def test_get_movie_rating_1(self):
        

    # ----
    # eval
    # ----

    def test_eval_1 (self) :
        to_predict_dict = OrderedDict([(2043, [1417435, 2312054, 462685])])
        predictions_dict = netflix_eval(to_predict_dict)
        self.assertEqual(1, len(predictions_dict))
        movie_ratings = predictions_dict[2043]
        self.assertEqual(3, len(movie_ratings))
        self.assertTrue(movie_ratings[0] >= 1)
        self.assertTrue(movie_ratings[0] <= 5)
        self.assertTrue(movie_ratings[1] >= 1)
        self.assertTrue(movie_ratings[1] <= 5)
        self.assertTrue(movie_ratings[2] >= 1)
        self.assertTrue(movie_ratings[2] <= 5)

    def test_eval_2 (self) :
        to_predict_dict = OrderedDict([(2043, [1417435, 2312054, 462685]), (10851, [1417435, 1234567])])
        predictions_dict = netflix_eval(to_predict_dict)
        self.assertEqual(2, len(predictions_dict))
        movie_ratings = predictions_dict[2043]
        self.assertEqual(3, len(movie_ratings))
        self.assertTrue(movie_ratings[0] >= 1)
        self.assertTrue(movie_ratings[0] <= 5)
        self.assertTrue(movie_ratings[1] >= 1)
        self.assertTrue(movie_ratings[1] <= 5)
        self.assertTrue(movie_ratings[2] >= 1)
        self.assertTrue(movie_ratings[2] <= 5)
        movie_ratings = predictions_dict[10851]
        self.assertEqual(2, len(movie_ratings))
        self.assertTrue(movie_ratings[0] >= 1)
        self.assertTrue(movie_ratings[0] <= 5)
        self.assertTrue(movie_ratings[1] >= 1)
        self.assertTrue(movie_ratings[1] <= 5)

    # -----
    # print
    # -----

    def test_print_1 (self) :
        w = StringIO()
        predictions_dict = OrderedDict([(2043, [3.4, 4.1, 1.9])])
        netflix_print(w, predictions_dict)
        self.assertEqual(w.getvalue(), "2043:\n3.4\n4.1\n1.9\n")

    def test_print_2 (self) :
        w = StringIO()
        predictions_dict = OrderedDict([(2043, [3.4, 4.1, 1.9]), (10851, [4.3, 1.4, 2.8])])
        netflix_print(w, predictions_dict)
        self.assertEqual(w.getvalue(), "2043:\n3.4\n4.1\n1.9\n10851:\n4.3\n1.4\n2.8\n")

    # -----
    # solve
    # -----
    '''
    def test_solve (self) :
        r = StringIO("1 10\n100 200\n201 210\n900 1000\n")
        w = StringIO()
        netflix_solve(r, w)
        self.assertEqual(w.getvalue(), "1 10 1\n100 200 1\n201 210 1\n900 1000 1\n")
    '''
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