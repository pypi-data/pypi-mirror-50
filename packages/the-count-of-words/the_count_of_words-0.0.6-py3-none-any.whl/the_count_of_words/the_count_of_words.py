import os
import re
import PyPDF2
import docx2txt

def validate_str(func):
    '''
    This function is a decorator that
    validates all arguments are of type str.
    '''
    def validate(*args, **kwargs):
        for arg in args:
            if not isinstance(arg, str):
                # returns Attribure error
                raise Exception("ATTRIBUTE ERROR: Invalid input - Expected str got {}.".format(type(arg)))
        return func(*args, **kwargs)
    return validate

def validate_ext(func):
    '''
    This function is a decorator that
    validates all arguments are of type str.
    '''
    @validate_str
    def validate(*args, **kwargs):
        formats = ['pdf', 'docx', 'txt']
        if args[0] not in formats:
            # returns Attribure error
            raise Exception("EXTENSION ERROR: Invalid file extension - Expected [pdf|docx|txt] got {}.".format(args[0]))
        return func(*args, **kwargs)
    return validate

def validate_path(func):
    '''
    This function is a decorator that
    validates all arguments are of type str.
    '''
    @validate_str
    def validate(*args, **kwargs):
        for arg in args:
            if not os.path.exists(arg):
                # returns Attribure error
                raise Exception("FILE NOT FOUND ERROR: Could not find file from path: {}.".format(arg))
        return func(*args, **kwargs)
    return validate

@validate_str
def get_count_of_words(text):
    '''
    This functions gets a string text,
    and returns a dictionary where the keys
    are one of each word in the text and the values
    are the number of times they appeared.

    @returns - dictionary.
    '''
    word_dict = {}

    # Make an array of all the words in the text
    words = re.findall("[^\W_]+", text)

    # for each word count the number of appearances
    for word in words:
        word = word.lower()
        if (word not in word_dict.keys()):
            word_dict[word] = 1
        else:
            word_dict[word] += 1

    # returns the result dectionary
    return word_dict

@validate_path
def read_txt_file(path):
    '''
    This function read a text file.
    '''
    with open(path, 'r') as file:
        text = file.read().replace('\n', '')
    print(text)
    return text

@validate_path
def read_docx_file(path):
    '''
    '''
    text = docx2txt.process(path)
    print(text)
    return text

@validate_path
def read_pdf_file(path):
    '''
    '''
    text = ''
    pdfFileObject = open(path, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObject)
    count = pdfReader.numPages
    for i in range(count):
        page = pdfReader.getPage(i)
        print(page.extractText())
        text += page.extractText() + ' '
    return text

@validate_str
def get_file_ext(file_path):
    '''
    This function get a file path and
    return its extension.
    '''
    file_extension = os.path.splitext(file_path)[1].split('.')[-1]
    return file_extension

@validate_ext
def get_file_txt(file_ext, path):
    '''
    This function returns the file tfile_.
    '''
    text = globals()['read_' + file_ext + '_file'](path)
    return text

@validate_str
def execute_count(path):
    '''
    This file takes a file path and returns
    the count of words for it.
    '''
    file_ext = get_file_ext(path)
    text = get_file_txt(file_ext, path)
    words_dict = get_count_of_words(text)
    return words_dict








