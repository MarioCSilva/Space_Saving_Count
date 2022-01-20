import sys

def open_file(fname, option="r", encoding='utf-8'):
    try:
        return open(fname, option, encoding=encoding)
    except FileNotFoundError:
        print(f"The file {fname} does not exist")
        sys.exit(1)

def calc_mean(word_count):
    return sum(word_count) / len(word_count)
