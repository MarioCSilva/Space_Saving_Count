from collections import defaultdict
from exact_counter import ExactCounter
from space_saving_counter import SpaceSavingCounter
import time
from math import sqrt
from tabulate import tabulate
from utils import *
import matplotlib.pyplot as plt


class Test():
    def __init__(self, fname="datasets/it_book.txt", epsilons=[0.0001, 0.001, 0.005, 0.01, 0.05, 0.1, 0.5]):
        self.fname = fname
        self.epsilons = sorted(epsilons, reverse=True)

        self.run_test()


    def run_test(self):
        exact_counter, space_saving_counter =\
            ExactCounter(self.fname), SpaceSavingCounter(self.fname)

        self.get_stats(exact_counter, exact_counter=True)
        self.get_stats(space_saving_counter)


    def get_stats(self, counter, exact_counter=False):
        print(f"{counter}\n")

        plot_data = [[], [], [], [], []]
        headers = ["Measure"]
        data = [["Time"], ["Total Words"], ["Events"], ["Mean"],\
            ["Minimum"], ["Maximum"]]

        if not exact_counter:
            data.extend([["Accuracy"], ["Precision"], ["Average Precision"]])
            for epsilon in self.epsilons:
                counter.epsilon = epsilon
                tic = time.time()
                counter.count()
                exec_time = round(time.time() - tic, 2)

                total_events = sum(counter.word_counter.values())
                total_words = len(counter.word_counter)
                min_events = min(counter.word_counter.values())
                max_events = max(counter.word_counter.values())
                mean = calc_mean(counter.word_counter.values())

                headers.append(f"Epsilon {epsilon}")
                data[0].append(exec_time)
                data[1].append(total_words)
                data[2].append(total_events)
                data[3].append(mean)
                data[4].append(min_events)
                data[5].append(max_events)

                plot_data[0].append(epsilon)
                plot_data[1].append(exec_time)

                relative_precision, right_position_words, TP = 0, 0, 0
                exact_top_k_words = list(self.exact_top_k_words.keys())
                top_words = counter.sort_words()
                for i, word in enumerate(top_words):
                    if word in self.exact_top_k_words:
                        TP += 1
                    if word == exact_top_k_words[i]:
                        right_position_words += 1
                        relative_precision += right_position_words / (i + 1) 
                avg_relative_precision = round(relative_precision / total_words * 100, 2)
                FP = total_words - TP
                TN = self.total_words - total_words - FP
                precision = round(TP / total_words * 100, 2)
                accuracy = round((TP + TN) / self.total_words * 100, 2)
                # recall not appropriate since it is evaluated top n most frequent words

                data[6].append(accuracy)
                data[7].append(precision)
                data[8].append(avg_relative_precision)
                plot_data[2].append(accuracy)
                plot_data[3].append(precision)
                plot_data[4].append(avg_relative_precision)

            print(tabulate(data, headers=headers))

            plt.plot(plot_data[0], plot_data[1], label="Execution Time")
            plt.ylabel("Time (s)")
            plt.xlabel("Epsilon")
            plt.title(counter)
            plt.legend()
            plt.show()

            plt.plot(plot_data[0], plot_data[2], label="Accuracy (%)")
            plt.plot(plot_data[0], plot_data[3], label="Precision (%)")
            plt.plot(plot_data[0], plot_data[4], label="Average Precision (%)")
            plt.ylabel("Percentage (%)")
            plt.xlabel("Epsilon")
            plt.title(counter)
            plt.legend()
            plt.show()
            return

        tic = time.time()
        counter.count()
        exec_time = round(time.time() - tic, 3)
        self.exact_top_k_words = counter.sort_words()
        self.total_words = len(counter.word_counter)
        total_events = sum(counter.word_counter.values())
        min_events = min(counter.word_counter.values())
        max_events = max(counter.word_counter.values())
        mean = calc_mean(counter.word_counter.values())

        headers.append("Value")
        data[0].append(exec_time)
        data[1].append(self.total_words)
        data[2].append(total_events)
        data[3].append(mean)
        data[4].append(min_events)
        data[5].append(max_events)

        print(f"{tabulate(data, headers=headers)}\n")