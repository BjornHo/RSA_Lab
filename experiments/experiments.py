import os,sys,inspect

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from tests.test_Hastad import MyTestCase as hastad_Test
from tests.test_Franklin_Reiter import MyTestCase as fr_Test
import statistics
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

def write_result(file_name, result):
    f = open(file_name, "a")
    f.write(str(result) + "\n")
    f.close()

# Run experiment 100 times and write elapsed time to txt file
# We adjust e and num_users in test_Hastad accordingly
# And epsilon=1/13 for e=11 and epsilon=1/15 for e=13 in small_roots(epsilon=...) in Hastad
def run_experiment_hastad():
    for i in range(100):
        experiment = hastad_Test()
        elapsed_time = experiment.test_Hastad_BCA()
        write_result("hastad_e.txt", elapsed_time)

# Run experiment 100 times for Franklin-Reiter
def run_experiment_fr():
    for i in range(100):
        experiment = fr_Test()
        elapsed_time = experiment.test_Franklin_Reiter()
        write_result("fr_e.txt", elapsed_time)

# We calculate statistics
def calculate_statistics(values):
    mean = statistics.mean(values)
    std = statistics.stdev(values)
    return mean, std

def make_plots_hastad():
    file_e_list = [3, 7, 11, 13]
    mean_values = []
    std_values = []

    # Loop through all hastad_e<nr>.txt files and get the results for each e.
    for current_e in file_e_list:
        f = open("hastad_e" + str(current_e) + str(".txt"), "r")
        lines = f.readlines()
        results = []
        for line in lines:
            results.append(float(line.strip()))

        # Calculate mean and std for each e
        mean, std = calculate_statistics(results)
        mean_values.append(mean)
        std_values.append(std)
        f.close()

    # Code to plot the graph
    x = np.array(file_e_list)
    y = np.array(mean_values)
    e = np.array(std_values)

    plt.errorbar(x, y, e, linestyle='None', marker='.')
    plt.xlabel("Public exponent e")
    plt.ylabel("Mean runtime in seconds")
    plt.title("Runtime performance for Hastad Broadcast Attack")
    plt.xticks(x, x)
    plt.savefig("Hastad_runtime.pdf")
    #plt.plot()



#run_experiment_hastad()
#make_plots_hastad()
#run_experiment_fr()