#!/usr/bin/env python3

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
# netflix_eval
# ------------

def netflix_eval (i, j) :
    """
    i the beginning of the range, inclusive
    j the end       of the range, inclusive
    return the max cycle length of the range [i, j]
    """
    # <your code>
    return 1

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