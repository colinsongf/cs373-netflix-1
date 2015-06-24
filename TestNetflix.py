#!/usr/bin/env python3

# https://docs.python.org/3.4/reference/simple_stmts.html#grammar-token-assert_stmt

# -------
# imports
# -------

from io       import StringIO
from unittest import main, TestCase

from collections import OrderedDict 
from Netflix import netflix_read, netflix_eval, netflix_print, netflix_solve, get_movie_rating, get_customer_rating, predict, get_solutions, calculate_RMSE, netflix_load

# -----------
# TestNetflix
# -----------

class TestNetflix (TestCase) :

    @classmethod
    def setUpClass (self) :
        self.caches = netflix_load()

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

    def test_read_3 (self) :
        s    = "2043:\n1417435\n2312054\n462685\n10851:\n1417435\n1234567\n"
        to_predict = netflix_read(s)
        self.assertEqual(2, len(to_predict))
        self.assertEqual(1417435, (to_predict[2043])[0])
        self.assertEqual(2312054, (to_predict[2043])[1])
        self.assertEqual(462685, (to_predict[2043])[2])
        self.assertEqual(1417435, (to_predict[10851])[0])
        self.assertEqual(1234567, (to_predict[10851])[1])

    """
    because these are simple functions to get values from the cache,
    these are effectively more effectively testing netflix_load
    """

    # ----  
    # get_movie_rating
    # ----

    def test_get_movie_rating_1(self):
        rating = get_movie_rating(self.caches[0], 4335)
        self.assertEqual(3.779, rating)

    def test_get_movie_rating_2(self):
        rating = get_movie_rating(self.caches[0], 4618)
        self.assertEqual(2.7875, rating)

    def test_get_movie_rating_3(self):
        rating = get_movie_rating(self.caches[0], 2736)
        self.assertEqual(3.875, rating)



    # ----     
    # get_customer_rating
    # ----

    def test_get_customer_rating_1(self):
        rating = get_customer_rating(self.caches[1], 1585790)
        self.assertEqual(3.41666667, round(rating, 8))

    def test_get_customer_rating_2(self):
        rating = get_customer_rating(self.caches[1], 1654988)
        self.assertEqual(4.20408163, round(rating, 8))

    def test_get_customer_rating_3(self):
        rating = get_customer_rating(self.caches[1], 958597)
        self.assertEqual(3.27848101, round(rating, 8))

    # ----     
    # get_solutions
    # ----

    def test_get_solutions_1(self):
        solutions_dict = get_solutions(self.caches[2])
        movie_ratings = solutions_dict[1]
        self.assertEqual(4, movie_ratings[0])

    def test_get_solutions_2(self):
        solutions_dict = get_solutions(self.caches[2])
        movie_ratings = solutions_dict[10]
        self.assertEqual(3, movie_ratings[1])

    def test_get_solutions_3(self):
        solutions_dict = get_solutions(self.caches[2])
        movie_ratings = solutions_dict[10016]
        self.assertEqual(2, movie_ratings[0])
        self.assertEqual(2, movie_ratings[2])
        self.assertEqual(5, movie_ratings[4])


    # ----
    # predict
    # ----

    def test_predict_1(self):
        rating = predict(self.caches, 4335, 1585790)
        self.assertEqual(3.5, rating)

    def test_predict_2(self):
        rating = predict(self.caches, 3949, 2484454)
        self.assertEqual(3.9, rating)

    def test_predict_3(self):
        rating = predict(self.caches, 5370, 756299)
        self.assertEqual(3.2, rating)


    # ------------
    # calcualate_RMSE
    # ------------    

    def test_calculate_RMSE_1(self):
        to_predict_dict = OrderedDict([(1585790, [2, 3, 4])])
        solutions_dict = OrderedDict([(1585790, [4, 1, 7])])
        rmse = calculate_RMSE(to_predict_dict, solutions_dict)
        self.assertEqual( 2.38047614285, round(rmse, 11))

    def test_calculate_RMSE_2(self):
        to_predict_dict = OrderedDict([(1585790, [2, 3]), (2484454, [4])])
        solutions_dict = OrderedDict([(1585790, [4, 1]), (2484454, [7])])
        rmse = calculate_RMSE(to_predict_dict, solutions_dict)
        self.assertEqual( 2.38047614285, round(rmse, 11))

    def test_calculate_RMSE_3(self):
        to_predict_dict = OrderedDict([(1585790, [2]), (2484454, [3]),(756299, [4])])
        solutions_dict = OrderedDict([(1585790, [4]), (2484454, [1]),(756299,[7])])
        rmse = calculate_RMSE(to_predict_dict, solutions_dict)
        self.assertEqual( 2.38047614285, round(rmse, 11))


    # ----
    # eval
    # ----

    def test_eval_1 (self) :
        to_predict_dict = OrderedDict([(1234, [1585790, 654988])])
        predictions_dict = netflix_eval(self.caches, to_predict_dict)
        self.assertEqual(1, len(predictions_dict))
        movie_ratings = predictions_dict[1234]
        self.assertEqual(2, len(movie_ratings))
        self.assertTrue(movie_ratings[0] >= 1)
        self.assertTrue(movie_ratings[0] <= 5)
        self.assertTrue(movie_ratings[1] >= 1)
        self.assertTrue(movie_ratings[1] <= 5)

    def test_eval_2 (self) :
        to_predict_dict = OrderedDict([(4335, [1585790, 2484454, 756299])])
        predictions_dict = netflix_eval(self.caches, to_predict_dict)
        self.assertEqual(1, len(predictions_dict))
        movie_ratings = predictions_dict[4335]
        self.assertEqual(3, len(movie_ratings))
        self.assertTrue(movie_ratings[0] >= 1)
        self.assertTrue(movie_ratings[0] <= 5)
        self.assertTrue(movie_ratings[1] >= 1)
        self.assertTrue(movie_ratings[1] <= 5)
        self.assertTrue(movie_ratings[2] >= 1)
        self.assertTrue(movie_ratings[2] <= 5)

    def test_eval_3 (self) :
        to_predict_dict = OrderedDict([(4335, [1585790, 2484454, 756299]), (1234, [1585790, 1654988])])
        predictions_dict = netflix_eval(self.caches, to_predict_dict)
        self.assertEqual(2, len(predictions_dict))
        movie_ratings = predictions_dict[4335]
        self.assertEqual(3, len(movie_ratings))
        self.assertTrue(movie_ratings[0] >= 1)
        self.assertTrue(movie_ratings[0] <= 5)
        self.assertTrue(movie_ratings[1] >= 1)
        self.assertTrue(movie_ratings[1] <= 5)
        self.assertTrue(movie_ratings[2] >= 1)
        self.assertTrue(movie_ratings[2] <= 5)
        movie_ratings = predictions_dict[1234]
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

    def test_print_3 (self) :
        w = StringIO()
        predictions_dict = OrderedDict([(2043, [3.4, 4.1, 1.9]), (10851, [4.3, 1.4, 2.8]), (3367, [3.2, 1.1, 4.5])])
        netflix_print(w, predictions_dict)
        self.assertEqual(w.getvalue(), "2043:\n3.4\n4.1\n1.9\n10851:\n4.3\n1.4\n2.8\n3367:\n3.2\n1.1\n4.5\n")


    # -----
    # solve
    # -----
    def test_solve_1 (self) :
        r = StringIO("1:\n30878\n2647871\n1283744")
        w = StringIO()
        netflix_solve(r, w)
        self.assertEqual(w.getvalue(), "1:\n3.7\n3.3\n3.8\nRMSE: 0.63")
        #4 4 3
        #-.3 .5 .6
        #.09 .25 .36
        #0.2333...
        #0.48304589

    def test_solve_2 (self) :
        r = StringIO("10000:\n2311278\n928262")
        w = StringIO()
        netflix_solve(r, w)
        self.assertEqual(w.getvalue(), "10000:\n3.5\n3.1\nRMSE: 1.23")
        #5 4
        #0.3 .5
        #0.09 .25
        #0.17
        #0.412310

    def test_solve_3 (self) :
        r = StringIO("16575:\n30878\n2647871\n1283744\n2311278")
        w = StringIO()
        netflix_solve(r, w)
        self.assertEqual(w.getvalue(), "16575:\n3.7\n3.7\n3.8\n3.9\nRMSE: 1.07")
        # 5 5 4 5
        #1.3 1.5 1.4 .1 
        #1.69 2.25 1.96 0.01
        #1.4775
        #1.21552
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
