#!/usr/bin/env python
# coding: utf-8
"""
Authors: Simrat Hanspal and Rudy Venguswamy
CeleryStalk Framework v1.0.1
Contact: simrath@vmware.com, rudy@ischool.berkeley.edu

"""
from __future__ import absolute_import, unicode_literals
from celery import group
from celery import Celery
from celery.utils.log import get_task_logger

import gc
import os
import csv
import pdb
import time
import dill as dill
import pandas as pd
import multiprocessing
import jsonpickle as jp

from celery.task.control import inspect
"""
Initiates the celery app identifying process
"""

app = Celery('CeleryStalk',
             broker='redis://localhost:6379/0',
             backend='redis',
             include=[])


#logs celery tasks
logger = get_task_logger(__name__)

# Optional configuration, see the application user guide for celery.
app.conf.update(
    result_expires=3600,
)


@app.task
def readtodf(jsonfn, workdirectory, filenamed):
    """
    takes a chunk of the CSV, which is a piece of the original CSV, split, reads it to a dataframe, applies the function, and returns it to CSV
    :param jsonfn: json version of a function
    :param workdirectory: where splitCSV and processedCSV (intermediate CSV files) get stored
    :param filenamed: name of CSV to be processed
    """
    url = workdirectory + '/SplitCSV/' + filenamed
    df = pd.read_csv(url)
    # unpack the lambda function from json to pickle to function
    picklefn = jp.decode(jsonfn)
    func = dill.loads(picklefn)
    df = df.apply(func, axis=1)
    os.chdir(workdirectory + 'SplitCSVProcessed/')
    print('Function Applied. Now Saving Results')
    df.to_csv(filenamed + 'processed.csv', encoding='utf-8')
    return 'Done Processing CSVs. Merging them...'


#takes all processed CSV files and joins them together
@app.task
def concatdf(workdirectory):
    """
    Takes all the files in a directory and concatenates them into one CSV
    :param workdirectory: directory where the folder SplitCSVProcessed exists, used for the merge into a final large, processed csv
    """
    os.chdir(workdirectory)
    fout = open("out.csv", 'ab')
    # first file:
    first = True
    os.chdir(workdirectory + '/SplitCSVProcessed')
    print('JOINING FILES')
    for f in os.listdir(workdirectory + '/SplitCSVProcessed'):
        with open(f, 'rb') as f:
            for line in f:
                fout.write(line)
    fout.close()

    return 'Done with Function'


def splitcsv(workdirectory, file, num_cores=multiprocessing.cpu_count()):
    """
    splits a large CSV into smaller CSVs to allow for parallel processing
    :param workdirectory: file location for intermediate CSV folders (splitCSV, SplitCSVprocessed) to be created
    :param file: file to be processed via parallelization
    :param num_cores: number of cpus that can be used for parallelizing pandas apply.
    """
    os.chdir(workdirectory)
    with open(file, 'r') as f:
        csvfile = f.readlines()
    print('NUM_CORES USED FOR PARALLELIZING: ', num_cores)
    csvlen = len(csvfile)
    linesPerFile = int(csvlen / num_cores) + 1
    filename = 1
    os.chdir(workdirectory + '/SplitCSV')
    for i in range(0, csvlen, linesPerFile):
        with open(str(filename) + '.csv', 'w+') as f:
            f.writelines(csvfile[i:i + linesPerFile])
        filename += 1
    return 'CSV Split into Chunks for Processing...'


def examplefn(vec):
    """
    example function that will be applied across CSV chunks
    :param vec: a row of a data frame, used inside a pandas.apply(function, axis = 1)
    """
    vec[0] = vec[0] + 1000
    return vec


def c_apply(workdirectory, csvdirectory, lambdafn=examplefn):
    """
    creates a directory for Split CSVs, processes SPLIT CSVs and initiates the entire parallel process
    :param workdirectory: file location for intermediate CSV folders (splitCSV, SplitCSVprocessed) to be created
    :param csvdirectory: location of the file to be processed in parallel
    :param lambdafn: function to be applied across a pandas dataframe 
    """
    # turns function into celery passable object
    picklefn = dill.dumps(lambdafn)
    jsonfn = jp.encode(picklefn)

    if not os.path.exists(workdirectory + '/SplitCSV'):
        os.makedirs(workdirectory + '/SplitCSV')

    if not os.path.exists(workdirectory + '/SplitCSVProcessed'):
        os.makedirs(workdirectory + '/SplitCSVProcessed')

    print(splitcsv(workdirectory, csvdirectory))
    print('Reading and Modifying Files')

    filelist = []
    for filename in os.listdir(workdirectory + '/SplitCSV'):
        filelist.append(filename)
    i = inspect()
    print('TASK REGISTER',i.registered_tasks())
    #The following 3 lines execute the parallel process: run the readtodf method in parallel, and then after all are executed, concat the CSVS into one big CSV again
    c3 = (group(readtodf.si(jsonfn, workdirectory, filename) for filename in filelist) | concatdf.si(workdirectory))

    res = c3()
    value = res.get()
    del res
    gc.collect()
    return value
    

def master_run(workdirectory, csvdirectory):
    """
    Redundant method that calls c_apply but allows for a generic framework that eliminates the need to modify parallelise.py if c_apply is modified.
    :param workdirectory: file location for intermediate CSV folders (splitCSV, SplitCSVprocessed) to be created
    :param csvdirectory: location of the file to be processed in parallel
    """
    c_apply(workdirectory, csvdirectory, examplefn)
    return
