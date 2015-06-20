#!/usr/bin/env python3

# ------------
# netflix_read
# ------------

def netflix_read (s) :
    """
    read two ints
    s a string
    return a list of two ints, representing the beginning and end of a range, [i, j]
    """
    a = s.split()
    return [int(a[0]), int(a[1])]

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

def netflix_print (w, i, j, v) :
    """
    print three ints
    w a writer
    i the beginning of the range, inclusive
    j the end       of the range, inclusive
    v the max cycle length
    """
    w.write(str(i) + " " + str(j) + " " + str(v) + "\n")

# -------------
# netflix_solve
# -------------

def netflix_solve (r, w) :
    """
    r a reader
    w a writer
    """
    for s in r :
        i, j = netflix_read(s)
        v    = netflix_eval(i, j)
        netflix_print(w, i, j, v)
