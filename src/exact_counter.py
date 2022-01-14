from collections import defaultdict
import re
from utils import open_file


class ExactCounter():
    def __init__(self, fname="../datasets/en_bible.txt"):
        self.fname = fname

    
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
        text = file.read()
        file.close

        tokens = re.sub("[^0-9a-zA-Z]+"," ", text).lower().split()

        for word in tokens:
            self.word_counter[word] += 1
        

    def top_k_words(self, k=10):
        return {word: occur for word, occur in \
            sorted(self.word_counter.items(), key=lambda x: x[1], reverse=True)[:k]}
