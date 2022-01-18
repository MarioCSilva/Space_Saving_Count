from collections import defaultdict
from exact_counter import ExactCounter
from space_saving_counter import SpaceSavingCounter
import time
from math import sqrt
from tabulate import tabulate
from utils import *
import matplotlib.pyplot as plt


class Test():
    def __init__(self, fname="datasets/it_book.txt", epsilons=[1, 0.5, 0.1, 0.05, 0.01, 0.005, 0.001]):
        self.fname = fname
        self.epsilons = epsilons

        self.run_test()


    def run_test(self):
        exact_counter, space_saving_counter =\
            ExactCounter(self.fname), SpaceSavingCounter(self.fname)

        self.get_stats(exact_counter, exact_counter=True)
        self.get_stats(space_saving_counter)


    def get_stats(self, counter, exact_counter=False):
        print(f"{counter}\n")

        plot_data = [[], [], []]

        if not exact_counter:
            for epsilon in self.epsilons:
                counter.epsilon = epsilon
                tic = time.time()
                counter.count()
                exec_time = round(time.time() - tic, 3)
                
                total_events = sum(counter.word_counter.values())
                total_words = len(counter.word_counter)
                assert total_words == counter.k
                min_events = min(counter.word_counter.values())
                max_events = max(counter.word_counter.values())
                mean = calc_mean(counter.word_counter.values())

                data = [["Counting Time (s)", avg_time], ["Alphabet Size"], ["Events"], ["Mean"], ["Minimum"], ["Maximum"]]
                headers = ["Measure", "Value"]
                
                plot_data[0].append(epsilon)
                plot_data[1].append(exec_time)
                plot_data[2].append(exec_time)


        if exact_counter:
            self.exact_word_counter = counter.word_counter
            self.exact_top_k_words = counter.top_k_words(self.k)
            self.k = len(self.exact_top_k_words)
            self.alphabet_size = len(counter.word_counter)
            self.total_events = total_countings = sum(counter.word_counter.values())
            self.mean = mean = calc_mean(counter.word_counter.values())
            self.min_events = min_events = min(counter.word_counter.values())
            self.max_events = max_events = max(counter.word_counter.values())
            data[1].append(self.alphabet_size)
            data[2].append(round(self.total_events, 2))
            data[3].append(round(self.mean, 2))
            data[4].append(round(self.min_events, 2))
            data[5].append(round(self.max_events, 2))
        else:
            headers.extend(["Absolute Error", "Relative Error (%)"])
            headers.extend([["Absolute Error"], ["Relative Error (%)"]])
            total_alp_size = round(total_alp_size / self.rep, 2)
            total_countings = round(total_countings / self.rep, 2)
            total_events = round(total_estimated_events / self.rep, 2)
            mean = round(total_means / self.rep, 2)
            min_events = round(total_min_events / self.rep, 2)
            max_events = round(total_max_events / self.rep, 2)
            common_top_k_words = most_frequent(total_word_counter, self.k)

            data[0].extend(['-', '-'])
            data[1].extend([total_alp_size, round(abs(self.alphabet_size - total_alp_size), 2),
                round(abs(self.alphabet_size - total_alp_size) / self.alphabet_size * 100, 2)])
            data[2].extend([total_events, round(abs(self.total_events - total_events), 2),
                round(abs(self.total_events - total_events) / self.total_events * 100, 2)])
            data[3].extend([mean, round(abs(self.mean - mean), 2),
                round(abs(self.mean - mean) / self.mean * 100, 2)])
            data[4].extend([min_events, round(abs(self.min_events - min_events), 2),
                round(abs(self.min_events - min_events) / self.min_events * 100, 2)])
            data[5].extend([max_events, round(abs(self.max_events - max_events), 2),
                round(abs(self.max_events - max_events) / self.max_events * 100, 2)])

        print(f"Results for {self.rep} repetition{'s' if self.rep != 1 else ''}:")
        print(f"Total Elapsed Time: {round(total_time, 3)} s\nTotal Events Counted: {total_countings}")
        print("\nAverage Values for a Repetition:")
        print(tabulate(data, headers=headers))

        print(f"\nTop {self.k} Most Frequent words:")
        if exact_counter:
            print(tabulate(self.exact_top_k_words.items(), headers=["word", "Exact Events"]))
        else:
            relative_precision, right_position_words = 0, 0
            exact_top_k_words = list(self.exact_top_k_words.keys())

            headers = ["word", "Min", "Max", "Mean", "Mean Absolute Error", "Mean Relative Error (%)"]
            data = []
            for i, word_counter in enumerate(common_top_k_words.items()):
                word, occur = word_counter
                mean_occur = calc_mean(occur)
                abs_error = abs(self.exact_word_counter[word] - mean_occur)
                rel_error = round(abs_error / self.exact_word_counter[word] * 100, 2)
                if self.rep > 1:
                    variance = calc_variance(occur, mean=mean_occur)
                    std_dvt = sqrt(variance)
                    headers.extend(["Variance", "Standard Deviation"])
                    data.append([word, min(occur), max(occur), mean_occur, abs_error, rel_error, variance, std_dvt])
                else:
                    data.append([word, min(occur), max(occur), mean_occur, abs_error, rel_error])
                if word == exact_top_k_words[i]:
                    right_position_words += 1
                    relative_precision += right_position_words / (i + 1)

            print(tabulate(data, headers=headers))
            
            avg_relative_precision = relative_precision / self.k * 100
            TP = len([word for word in common_top_k_words.keys() if word in self.exact_top_k_words.keys()])
            FP = self.k - TP
            TN = self.alphabet_size - self.k - FP
            precision = TP / self.k * 100
            accuracy = (TP + TN) / self.alphabet_size * 100

            # recall not appropriate since it is evaluated top n most frequent words
            print(f"Accuracy: {accuracy:.2f} %")
            print(f"Precision: {precision:.2f} %")
            print(f"Average Precision (relative order): {avg_relative_precision:.2f} %")
            
            if self.rep > 1:
                plt.plot(plot_data[0], plot_data[1], label="Total Events Relative Error")
                plt.ylabel("Relative Error (%)")
                plt.xlabel("Repetition")
                plt.title(counter)
                plt.legend()
                plt.show()

                plt.plot(plot_data[0], plot_data[2], label="Mean Relative Error")
                plt.ylabel("Relative Error (%)")
                plt.xlabel("Repetition")
                plt.title(counter)
                plt.legend()
                plt.show()

        print("\n")