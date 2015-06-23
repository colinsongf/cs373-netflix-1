#!/usr/bin/env python3
import json
import pickle
from collections import OrderedDict 
from urllib.request import urlopen
from math import sqrt

url = urlopen("http://www.cs.utexas.edu/~ebanner/netflix-tests/BRG564-Average_Movie_Rating_Cache.json")
average_movie_ratings = json.loads(url.read().decode(url.info().get_param('charset') or 'utf-8'))
url.close()
url = urlopen("http://www.cs.utexas.edu/~ebanner/netflix-tests/ezo55-Average_Viewer_Rating_Cache.json")
average_customer_ratings = json.loads(url.read().decode(url.info().get_param('charset') or 'utf-8'))
url.close()
url =urlopen("http://www.cs.utexas.edu/~ebanner/netflix-tests/mb39822-user_info.p")
user_info = pickle.load(url)
url.close()
url =urlopen("http://www.cs.utexas.edu/~ebanner/netflix-tests/mb39822-movie_info.p")
movie_info = pickle.load(url)
url.close()

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
    movie_id = -1
    for s in a:
        if s[(len(s) - 1):] == ':' :
            movie_id = int(s[0:len(s)-1])
            to_predict_dict[movie_id] = []

        else:
            customer_id  = int(s)
            to_predict_dict[movie_id].append(customer_id)

    return to_predict_dict 


# ------------
# get_movie_rating
# ------------

def get_movie_rating(movie_id) :
    return movie_info.get(movie_id).get('avg')
    #return average_movie_ratings[str(movie_id)]


# ------------
# get_customer_rating
# ------------

def get_customer_rating(customer_id) :
    #return user_info.get(customer_id).get('avg')
    return average_customer_ratings[str(customer_id)]


# ------------
# get_solutions
# ------------

def get_solutions() :
    with open("/u/ll9338/cs373/netflix-tests/jmt3675-probe_solution.txt") as f:
        cache = netflix_read(f.read())
    return cache


# ------------
# predict
# ------------

def predict (movie_id, customer_id) :
    return round((get_movie_rating(movie_id) + get_customer_rating(customer_id) ) / 2, 1)


# ------------
# calcualate_RMSE
# ------------    
def calculate_RMSE( predictions_dict, solutions_dict):
    sum = 0
    count = 0
    for movie_id in predictions_dict:
        for i in range(len(predictions_dict[movie_id])):
            diff = solutions_dict[movie_id][i] - predictions_dict[movie_id][i]
            sum += diff ** 2
            count += 1

    mean = sum / count
    rmse = sqrt(mean)

    return rmse


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
    for movie_id in predictions_dict :
        movies = predictions_dict[movie_id]
        for i in range(0, len(movies)) :
            customer_id = movies[i]
            movies[i] = predict(movie_id, customer_id)

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
    
    to_predict_dict = netflix_read(r.read())
    predictions_dict = netflix_eval(to_predict_dict)
    netflix_print(w, predictions_dict)
    solutions_dict = get_solutions()
    rmse = calculate_RMSE(predictions_dict, solutions_dict)
    w.write("RMSE: " + str(round(rmse, 2)))