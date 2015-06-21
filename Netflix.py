#!/usr/bin/env python3
import json
from collections import OrderedDict 

# ------------
# netflix_read
# ------------

def netflix_read (input) :
    """
    read two ints
    input a string
    return a list of two ints, representing the beginning and end of a range, [i, j]
    """
    to_predict_dict = OrderedDict()
    a = input.split()
    customer_id = -1
    for s in a:
        if s[(len(s) - 1):] == ':' :
            try:
                customer_id = int(s[0:len(s)-1])
            except:
                raise 

            to_predict_dict[customer_id] = []

        else:
            try:
                movie_id  = int(s)
            except:
                raise

            to_predict_dict[customer_id].append(movie_id)

    return to_predict_dict 


# ------------
# get_movie_rating
# ------------

def get_movie_rating(movie_id) :
    cache = json.loads("/u/ll9338/cs373/netflix-tests/BRG564-Average_Movie_Rating_Cache.json")



    return cache[movie_id]


# ------------
# get_customer_rating
# ------------

def get_customer_rating(customer_id) :
    cache = json.loads("/u/ll9338/cs373/netflix-tests/ezo55-Average_Viewer_Rating_Cache.json")

    

    return cache[customer_id]


# ------------
# predict
# ------------

def predict (customer_id, movie_id) :
    return 1

# ------------
# netflix_eval
# ------------

def netflix_eval (to_predict_dict) :
    """
    i the beginning of the range, inclusive
    j the end       of the range, inclusive
    return the max cycle length of the range [i, j]
    """
    predictions_dict = to_predict_dict.copy()
    for customer_id in predictions_dict :
        movies = predictions_dict[customer_id]
        for i in range(0, len(movies)) :
            movie_id = movies[i]
            movies[i] = predict(customer_id, movie_id)

    return predictions_dict

# -------------
# netflix_print
# -------------

def netflix_print (w, predictions_dict) :
    """
    print three ints
    w a writer
    i the beginning of the range, inclusive
    j the end       of the range, inclusive
    v the max cycle length
    """
    
    for key in predictions_dict:
        w.write(str(key) + ':\n')
        for value in predictions_dict[key]:
            w.write(str(value) + '\n')

# -------------
# netflix_solve
# -------------

def netflix_solve (r, w) :
    """
    r a reader
    w a writer
    """
    '''
    for s in r :
        i, j = netflix_read(s)
        v    = netflix_eval(i, j)
        netflix_print(w, i, j, v)
    '''