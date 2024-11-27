import sys
import os
from io import StringIO
from gcms import GCMS
from object import Color
from exceptions import NoBinFoundException
import time
import traceback

reverse_color_dict = {0: Color.BLUE, 1: Color.YELLOW, 2: Color.RED, 3: Color.GREEN}

PATH = "C:\Users\sanju\Downloads\Compress_tc" # put the path of test case directory in this string 

testcases = {
    PATH + "complex/tc0.txt": PATH + "complex/tc0_sol.txt",
    PATH + "complex/tc1.txt": PATH + "complex/tc1_sol.txt",
    PATH + "complex/tc2.txt": PATH + "complex/tc2_sol.txt",
    PATH + "add_bin/tc0.txt": PATH + "add_bin/tc0_sol.txt",
    PATH + "add_bin/tc1.txt": PATH + "add_bin/tc1_sol.txt",
    PATH + "add_bin/tc2.txt": PATH + "add_bin/tc2_sol.txt",
    PATH + "add_bin_object/tc0.txt": PATH + "add_bin_object/tc0_sol.txt",
    PATH + "add_bin_object/tc1.txt": PATH + "add_bin_object/tc1_sol.txt",
    PATH + "add_bin_object/tc2.txt": PATH + "add_bin_object/tc2_sol.txt",
    PATH + "add_object/tc0.txt": PATH + "add_object/tc0_sol.txt",
    PATH + "add_object/tc1.txt": PATH + "add_object/tc1_sol.txt",
    PATH + "add_object/tc2.txt": PATH + "add_object/tc2_sol.txt",
    PATH + "bin_object_del/tc0.txt": PATH + "bin_object_del/tc0_sol.txt",
    PATH + "bin_object_del/tc1.txt": PATH + "bin_object_del/tc1_sol.txt",
    PATH + "bin_object_del/tc2.txt": PATH + "bin_object_del/tc2_sol.txt",
    PATH + "exception/tc0.txt": PATH + "exception/tc0_sol.txt",
    PATH + "exception/tc1.txt": PATH + "exception/tc1_sol.txt",
}

timeouts = {
    PATH + "complex/tc0.txt": 1,
    PATH + "complex/tc1.txt": 2,
    PATH + "complex/tc2.txt": 15,
    PATH + "add_bin/tc0.txt": 1,
    PATH + "add_bin/tc1.txt": 1,
    PATH + "add_bin/tc2.txt": 15,
    PATH + "add_bin_object/tc0.txt": 1,
    PATH + "add_bin_object/tc1.txt": 3,
    PATH + "add_bin_object/tc2.txt": 15,
    PATH + "add_object/tc0.txt": 1,
    PATH + "add_object/tc1.txt": 5,
    PATH + "add_object/tc2.txt": 25,
    PATH + "bin_object_del/tc0.txt": 1,
    PATH + "bin_object_del/tc1.txt": 3,
    PATH + "bin_object_del/tc2.txt": 15,
    PATH + "exception/tc0.txt": 1,
    PATH + "exception/tc1.txt": 1,
}

def run_testcase(testcase_file_path, testcase_sol_file_path):
    sol_ind = 0
    try:
        gcms = GCMS()

        with open(testcase_file_path, "r") as tf, open(testcase_sol_file_path, "r") as tsf:
            lines = tf.readlines()
            sol_lines = tsf.readlines()
            sol_ind = 0
            for line in lines:
                line = line.strip().split()
                if line[0] == "0":
                    gcms.add_bin(int(line[1]), int(line[2]))
                elif line[0] == "1":
                    try:
                        gcms.add_object(int(line[1]), int(line[2]), reverse_color_dict[int(line[3])])
                    except:
                        continue
                elif line[0] == "2":
                    gcms.delete_object(int(line[1]))
                elif line[0] == "3":
                    if f"{gcms.bin_info(int(line[1]))}\n" != sol_lines[sol_ind]:
                        return 0  # Incorrect
                    sol_ind += 1
                elif line[0] == "4":
                    if f"{gcms.object_info(int(line[1]))}\n" != sol_lines[sol_ind]:
                        return 0  # Incorrect
                    sol_ind += 1
        return 1  # Correct
    except Exception as e:
        # print(e)
        return -2  # Import or other error

import resource
import multiprocessing
import time

def run_testcase_with_dynamic_timeout(testcase, sol_file, timeout):
    def target_function(result_queue):
        try:
            start_time = resource.getrusage(resource.RUSAGE_SELF).ru_utime
            result = run_testcase(testcase, sol_file)
            end_time = resource.getrusage(resource.RUSAGE_SELF).ru_utime
            cpu_time_used = end_time - start_time
            result_queue.put((result, cpu_time_used))
        except Exception as e:
            result_queue.put((-2, 0))

    result_queue = multiprocessing.Queue()
    process = multiprocessing.Process(target=target_function, args=(result_queue,))

    process.start()

    start = time.time()
    while process.is_alive():
        current_time = time.time()
        if (current_time - start) >= timeout:
            process.terminate()
            process.join()
            return -1 
        time.sleep(0.1) 

    # Retrieve result if available
    if not result_queue.empty():
        return result_queue.get()[0]
    else:
        return -2

def run_all_testcases(testcases, timeouts):
    results = {}

    original_stdout = sys.stdout
    sys.stdout = open(os.devnull, 'w')

    try:
        for testcase in testcases.keys():
            start_time = time.time()
            timeout = timeouts.get(testcase, 5)  # Default to 5 seconds

            try:
                result = run_testcase_with_dynamic_timeout(testcase, testcases[testcase], timeout)
            except Exception as e:
                # print(e)
                result = -2  # Import or other error
                end_time = time.time()
                time_taken = 0
            else:
                end_time = time.time()
                time_taken = end_time - start_time

            results[testcase] = (result, time_taken)
    finally:
        sys.stdout.close()
        sys.stdout = original_stdout

    return results

print(run_all_testcases(testcases, timeouts))