import re
from utils import open_file


class SpaceSavingCounter():
    def __init__(self, fname="../datasets/en_bible.txt", epsilon=0.01, stop_words_fname="./stopwords.txt"):
        self.fname = fname

        self.epsilon = epsilon

        self.get_stop_words(stop_words_fname)


    def get_stop_words(self, stopwords_fname):
        self.stop_words = set()
        stop_words_file = open_file(stopwords_fname)
        for line in stop_words_file:
            self.stop_words |= set(line.split(","))


    def __str__(self):
        return "Space Saving Counter"


    '''Reads the whole file
       tokenizes the text by
       splitting words by spaces and removing stopwords
    '''
    def count(self):
        self.k = int(1 / self.epsilon)

        self.word_counter = {}

        file = open_file(self.fname, 'r')

        for line in file:
            tokens = re.sub("[^a-zA-Z]+"," ", line).lower().split()
            for word in tokens:
                if word in self.stop_words:
                    continue
                
                if word in self.word_counter:
                    self.word_counter[word] += 1
                    continue

                if len(self.word_counter) < self.k:
                    self.word_counter[word] = 1
                    continue

                smallest_word_counter = min(self.word_counter, key=self.word_counter.get)
                self.word_counter[word] = self.word_counter.pop(smallest_word_counter) + 1

        file.close


    def sort_words(self):
        return sorted(self.word_counter, key=lambda x: self.word_counter[x], reverse=True)
