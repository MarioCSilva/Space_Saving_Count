from collections import defaultdict
import re
from utils import open_file
from random import random, seed


class SpaceSavingCounter():
    def __init__(self, fname="../datasets/en_bible.txt", epsilon=0.01):
        seed(93430)

        self.fname = fname

        self.epsilon = epsilon


    def __str__(self):
        return f"Space Saving Counter with Epsilon {self.epsilon}"


    '''Reads the whole file
       tokenizes the text by
       splitting words by spaces and removing stopwords
    '''
    def count(self):
        self.k = 1 / self.epsilon

        self.word_counter = defaultdict(int)

        file = open_file(self.fname, 'r')
        text = file.read()
        file.close

        tokens = re.sub("[^0-9a-zA-Z]+"," ", text).lower().split()


        for word in tokens:
            if word in self.word_counter:
                self.word_counter[word] += 1
                continue

            if len(self.word_counter) < self.k:
                self.word_counter[word] = 1
                continue

            smallest_word_counter = min(self.word_counter, key=self.word_counter.get)
            self.word_counter[word] = self.word_counter.pop(smallest_word_counter) + 1


    def top_k_words(self, k=10):
        return {word: occur for word, occur in \
            sorted(self.word_counter.items(), key=lambda x: x[1], reverse=True)[:k]}
