from collections import defaultdict
import re
from utils import open_file


class ExactCounter():
    def __init__(self, fname="../datasets/en_bible.txt", stop_words_fname="./stopwords.txt"):
        self.fname = fname

        self.get_stop_words(stop_words_fname)


    def get_stop_words(self, stopwords_fname):
        self.stop_words = set()
        stop_words_file = open_file(stopwords_fname)
        for line in stop_words_file:
            self.stop_words |= set(line.split(","))


    def __str__(self):
        return "Exact Counter"


    '''Reads the whole file
       tokenizes the text by
       splitting words by spaces and removing stopwords
       counts the exact number of occurrences of each word
    '''
    def count(self):
        self.word_counter = defaultdict(int)

        file = open_file(self.fname, 'r')

        for line in file:
            tokens = re.sub("[^a-zA-Z]+"," ", line).lower().split()
            for word in tokens:
                if word not in self.stop_words:
                    self.word_counter[word] += 1

        file.close
        

    def sort_words(self):
        return sorted(self.word_counter, key=lambda x: self.word_counter[x], reverse=True)
