import os,sys,inspect

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from tests.test_Hastad import MyTestCase
import statistics

def write_result(file_name, result):
    f = open(file_name, "a")
    f.write(str(result) + "\n")
    f.close()

# Run experiment 100 times and write elapsed time to txt file
# We adjust e and num_users in test_Hastad accordingly
# And epsilon=1/13 for e=11 and epsilon=1/15 for e=13 in small_roots(epsilon=...) in Hastad
def run_experiment():
    for i in range(100):
        experiment = MyTestCase()
        elapsed_time = experiment.test_Hastad_BCA()
        write_result("hastad_e13.txt", elapsed_time)

# We calculate statistics over the results
def calculate_statistics():
    f = open("hastad_e13.txt", 'r')
    lines = f.readlines()
    results = []
    for line in lines:
        results.append(float(line.strip()))

    print("The mean is: " + str(statistics.mean(results)))
    print("The STD is: " + str(statistics.stdev(results)))


#run_experiment()

calculate_statistics()