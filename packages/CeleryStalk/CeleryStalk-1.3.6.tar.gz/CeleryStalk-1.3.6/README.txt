======================
Celery Stalk v1.0
======================

Celery Stalk provides users a way to quickly mutate values in extremely large CSV files using parallel processing. Celery performs operations as fast as multithreading/multiprocessing out of the box with python, but is resilient to errors and outages and reallocated tasks across CPUs. You might find it useful for data cleaning tasks. Typical usage often looks like this::

	NOTEBOOK
	
import CeleryStalk
from CeleryStalk.paralleliser import Runner

#r = Runner(Task_file_Path, CSVPAth, Output Folder Path)
r= Runner('/Users/rudyvenguswamy/Desktop/test_folder/parallelised_pandas_apply.py', '/Users/rudyvenguswamy/Desktop/test_folder/samplecsv.csv', '/Users/rudyvenguswamy/Desktop/test_folder/')
r.main()
    
#to modify function called on CSV, modify the task file

	COMMAND LINE INTERFACE
    EXAMPLE CMD: python3 paralleliser.py --task_file parallelised_pandas_apply.py --ip_loc /Users/rudyvenguswamy/Coding/samplecsv.csv 
    --op_loc /Users/rudyvenguswamy/Coding/
    
Example Broken Down:
    You will always run paralleliser.py (the function that sets up the workers)
        --task file: the .py file containing the tasks that will be parallelized. Parallelised_pandas_apply.py is an example of a task, applied to pandas apply. If you make your own task file, it will require modifying paralleliser.py to have the `master_run()` function take the inputs your function requires (+ modifying the argument parser to take your inputs from command line if desired)
        --ip_loc: location of the CSV file for input
        --op_loc: where the resulting CSV will be placed
        
        CeleryStalk uses the 'examplefn' inside the parallelised_pandas_apply.py by default. Don't worry it prints out a line letting you know it's using the default function. However, if you'd like to apply your own function, write it inside the task file (parallelised_pandas_apply.py) and pass it as an argument to master_run.
    
    
**To report any bugs, email rvenguswamy@vmware.com**


When to Use Celery Stalk
============================

Celery Stalk should be used when:

* You have large data sets (personal testing shows it's better to just do the mutation [via Pandas.read_csv > mutate > pd.to_csv] when the data set is small.

* This library is especially useful if the computation performed on rows is intensive

* If your computer has at least a few CPUs (If your computer does not and you're working with extremely large data set computation, I recommend reconsidering your hardware choices or using a cloud GPU/CPU service).

Benchmark
============================
Parallelizing the apply function on pandas improves performance significantly. A 705MB CSV file takes about 20:40 minutes to run the example function, which adds a value to a numerical column of a dataframe that ingests the CSV file.

With `CeleryStalk` on a 12 Logical Cores computer (6 Physical CPU Cores x2), the process takes 4:50 minutes.

