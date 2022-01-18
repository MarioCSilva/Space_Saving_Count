import sys

def open_file(fname, option="r", encoding='utf-8'):
    try:
        return open(fname, option, encoding=encoding)
    except FileNotFoundError:
        print(f"The file {fname} does not exist")
        sys.exit(1)


def most_frequent(total_top_k_letters, k):
    return {letter: occur for letter, occur in \
        sorted(total_top_k_letters.items(), key=lambda x: sum(x[1]), reverse=True)[:k]}


def calc_mean(letter_occur):
    return sum(letter_occur) / len(letter_occur)


def calc_variance(letter_occur, mean):
    dvts = [(x - mean) ** 2 for x in letter_occur]
    return sum(dvts) / len(letter_occur)