import re

def get_words_dict(text):
    '''
    This functions gets a string text,
    and returns a dictionary where the keys
    are one of each word in the text and the values
    are the number of times they appeared.

    @returns - dictionary.
    '''
    # empty dictionary for mapping
    if (not isinstance(text, str)):

        # returns Attribure error
        return "Attribure Error: Invalid input of type {}".format(type(text))
    word_dict = {}

    # Make an array of all the words in the text
    words = re.findall("[^\W_]+", text)

    # for each word count the number of appearances
    for word in words:
        if (word not in word_dict.keys()):
            word_dict[word] = 1
        else:
            word_dict[word] += 1

    # returns the result dectionary
    return word_dict
