#!/usr/bin/env python3
import json
import pickle
import socket
from collections import OrderedDict 
from urllib.request import urlopen
from math import sqrt

# ------------
# netflix_load
# ------------

def netflix_load () :
    """
    load the movie and user info, and probe solutions caches
    return a list of three dictionaries, the movie info, user info, and solutions
    """
    # open the caches from the public test repo

    url = open("./mb39822-movie_info.p", 'rb')
    movie_info = pickle.load(url)
    url.close()

    url = open("./mb39822-user_info.txt", 'rb')
    user_info = pickle.load(url)
    url.close()

    url = open("./jmt3675-probe_solution.txt", 'rb')
    solutions = url.read()
    url.close()

    return [movie_info, user_info, solutions]

# ------------
# netflix_read
# ------------

def netflix_read (input) :
    """
    read a string of the full input on which to predict ratings
    input a string
    return a dictionary where the keys are movie ids and each value is a list of customer ids
            for which to predict their rating of that movie, or a list of ratings which those
            customers have given that movie
    """
    to_predict_dict = OrderedDict()
    a = input.split()
    movie_id = -1
    for s in a:
        if ':' in s :
        #if s[(len(s) - 1):] == ':' :
            # s should contain a movie id, so make it a key
            movie_id = int(s[0:len(s)-1])
            to_predict_dict[movie_id] = []

        else:
            # s should contain a customer id or rating, so add it to this movie's list
            customer_id  = int(s)
            to_predict_dict[movie_id].append(customer_id)

    return to_predict_dict 


# ------------
# get_movie_rating
# ------------

def get_movie_rating(movie_info, movie_id) :
    """
    find the average rating for a movie
    movie_info the dictionary which contains info of movies
    movie_id an int, the id of the movie
    return an int, the average rating of that movie
    """
    return movie_info[movie_id]['avg']


# ------------
# get_customer_rating
# ------------

def get_customer_rating(user_info, customer_id) :
    """
    find the average rating a customer gives
    user_info the dictionary which contains info of users
    customer_id an int, the id of the customer
    return an int, the average rating that customer gives
    """
    return user_info[customer_id]['total'] / user_info[customer_id]['count']


# ------------
# get_solutions
# ------------

def get_solutions(solutions) :
    """
    give the actual answers for the probe input
    solutions a string of an input file with solutions in it
    return a dictionary where the keys are movie ids and each value is a list of ratings
    """
    return netflix_read(solutions)


# ------------
# predict
# ------------

def predict (caches, movie_id, customer_id) :
    """
    make a prediction of what a customer will rate a movie
    caches a list of the movie user info caches
    movie_id an int, the movie to predict the rating of
    customer_id an int, the customer whose rating is to be predicted
    return an int, the predicted rating of the customer for the movie
    """
    # average the average customer rating, rating for that decade, movie rating, movie for customer's year
    movie_info = caches[0]
    user_info = caches[1]

    avg_movie_rating = get_movie_rating(movie_info, movie_id)
    avg_customer_rating = get_customer_rating(user_info, customer_id)
    movie_decade = movie_info[movie_id]['premiere'] - (movie_info[movie_id]['premiere'] % 10)
    decade_info = user_info[customer_id]['favorites'][movie_decade]
    decade_rating = decade_info['total'] / decade_info['count']
    return round(( avg_movie_rating + decade_rating) / 2, 1)


# ------------
# calcualate_RMSE
# ------------    
def calculate_RMSE( predictions_dict, solutions_dict):
    """
    calculate the RMSE for the ratings present in a dictionary of predictions and
    those present in the dictionary of solutions
    predictions_dict a dictionary where keys are movie ids and values are lists of predicted ratings
    solutions_dict a dictionary where keys are movie ids and values are lists of actual ratings
    return the RMSE of the predicted ratings from the actual ratings
    """
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

def netflix_eval (caches, to_predict_dict) :
    """
    create a dictionary of predictions from a dictionary of customers and movies for which
    caches a list of the movie user info caches
    ratings must be predicted
    to_predict_dict a dictionary where keys are movie ids and values are lists of customer ids
    return a dictionary where keys are movie ids and values are lists of ratings
            corresponding to the input dictionary's customer ids
    """
    predictions_dict = to_predict_dict.copy()
    # for every customer for every movie, replace the customer id with their predicted rating
    for movie_id in predictions_dict :
        movies = predictions_dict[movie_id]
        for i in range(0, len(movies)) :
            customer_id = movies[i]
            movies[i] = predict(caches, movie_id, customer_id)

    return predictions_dict

# -------------
# netflix_print
# -------------

def netflix_print (w, predictions_dict) :
    """
    print a dictionary of predicted ratings
    w a writer
    predictions_dict the dictionary to be printed
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
    solve the netflix problem given input from r and outputting to w
    r a reader
    w a writer
    """
    caches = netflix_load()
    movie_info = caches[0]
    user_info = caches[1]
    solutions = caches[2]
    to_predict_dict = netflix_read(r.read())
    predictions_dict = netflix_eval(caches, to_predict_dict)
    netflix_print(w, predictions_dict)
    solutions_dict = get_solutions(solutions)
    rmse = calculate_RMSE(predictions_dict, solutions_dict)
    w.write("RMSE: " + ('%.2f' % (int(rmse*100)/float(100))))
    