# word_count.py
# ===================================================
# Tiffanie Alcaide
# CS 261
#
# Implement a word counter that counts the number of
# occurrences of all the words in a file. The word
# counter will return the top X words, as indicated
# by the user.
# ===================================================

import re
from hash_map import HashMap

"""
This is the regular expression used to capture words. It could probably be endlessly
tweaked to catch more words, but this provides a standard we can test against, so don't
modify it for your assignment submission.
"""
rgx = re.compile("(\w[\w']*\w|\w)")

def hash_function_2(key):
    """
    This is a hash function that can be used for the hashmap.
    """

    hash = 0
    index = 0
    for i in key:
        hash = hash + (index + 1) * ord(i)
        index = index + 1
    return hash

def top_words(source, number):
    """
    Takes a plain text file and counts the number of occurrences of case insensitive words.
    Returns the top `number` of words in a list of tuples of the form (word, count).

    Args:
        source: the file name containing the text
        number: the number of top results to return (e.g. 5 would return the 5 most common words)
    Returns:
        A list of tuples of the form (word, count), sorted by most common word. (e.g. [("a", 23), ("the", 20), ("it", 10)])
    """

    keys = set()

    ht = HashMap(2500,hash_function_2)

    # This block of code will read a file one word as a time and
    # put the word in `w`. It should be left as starter code.
    with open(source) as f:
        for line in f:
            words = rgx.findall(line)
            for w in words:
                w = w.lower() # make everything lower case

                # if the word is already in keys, get and increase the count.
                if w in keys:
                    count = ht.get(w)
                    count += 1
                    ht.put(w, count) # update the count

                # otherwise add the new word to the hashmap with count of 1
                else:
                    ht.put(w, 1)
                    keys.add(w)

    count_list = [] # list of tuples of keys and counts

    # for each key, get the value, and add these pairs as tuples to count_list
    for k in keys:
        val = ht.get(k)
        pair = (k, val)
        count_list.append(pair)

    # sort count_list with a lambda function using sorted(). Reverse the list for descending order
    count_list = sorted(count_list, key=lambda x: x[1], reverse=True) # where x is a tuple and x[1] is the word count

    # return the appropriate number of top words
    return count_list[:number]




#print(top_words("alice.txt",10))  # COMMENT THIS OUT WHEN SUBMITTING TO GRADESCOPE

