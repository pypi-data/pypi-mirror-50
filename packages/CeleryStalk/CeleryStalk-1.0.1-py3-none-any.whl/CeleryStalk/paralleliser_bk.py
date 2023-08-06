from __future__ import absolute_import, unicode_literals
from celery_config import app
# from celery.task.control import inspect

import os
import sys
import pdb
import time
import emoji
import traceback
import subprocess
from itertools import chain
from argparse import ArgumentParser


class Runner:
    def __init__(self, task_filepath, ip_loc, op_loc):
        """

        :param task_filepath:
        :param ip_loc:
        :param op_loc:
        :param log_level:
        """
        self.ip_loc = ip_loc
        self.op_loc = op_loc
        self.task_filepath = task_filepath
        
    def setup(self):
        """

        :return:
        """
        print("Starting setup ...")

        # ==== LOAD TASK MODULE ==== #
        if self.task_filepath not in sys.path:
            sys.path.append(self.task_filepath)
        filename = self.task_filepath.split("/")[-1] if "/" in self.task_filepath else self.task_filepath
        module_name = filename.replace(".py", "")
        self.module = __import__(module_name)
        print("Task module loaded")
        # pdb.set_trace()
        print(self.module.app.__dict__["main"])

        # ==== START REDIS SERVER ==== #
        cmd = "nohup redis-server&"
        returned_value = subprocess.call(cmd, shell=True)
        print("\nRedis server started with status =", returned_value)

        # ==== START REDIS SERVER ==== #
        cmd = "celery worker -A %(app)s -E -n CeleryStalkWorker -l INFO --detach "%{"app": self.module.app.__dict__["main"]}
        returned_value = subprocess.call(cmd, shell=True)
        print("Celery worker threads started with status =", returned_value)

        time.sleep(0.1)
        print(emoji.emojize(":triangular_flag_on_post: SETUP COMPLETE \n", use_aliases=True))

    def load_input_files(self):
        """
        importlib module import doesn't work well with dill serialisation, not sure why.
        Hence using sys.path.append
        :return:
        """

        self.module.master_run(self.op_loc, self.ip_loc)
        return

    def execute(self):
        """

        :return:
        """
        start = time.time()
        self.load_input_files()
        print(emoji.emojize(":triangular_flag_on_post: EXECUTION COMPLETE \n", use_aliases=True))
        print('TIME TAKEN ::', time.time()-start)
        
    def teardown(self):
        """

        :return:
        # """

        cmd = "ps aux | grep python | grep 'CeleryStalkWorker' | grep -v 'grep'| awk '{print $2}' | xargs kill"
        returned_value = subprocess.call(cmd, shell=True)
        print("Celery workers shutdown with status =", returned_value)

        ps = subprocess.Popen("ps aux | grep python | grep 'CeleryStalkWorker' | grep -v 'grep'| awk '{print $2}'", shell=True, stdout=subprocess.PIPE)
        process_status = ps.stdout.read().decode("utf-8")
        while process_status != "":
            print("Celery processes are shutting down. Sleeping for 1 sec ... zzZ")
            time.sleep(1)
            ps = subprocess.Popen("ps aux | grep python | grep 'CeleryStalkWorker' | grep -v 'grep'| awk '{print $2}'", shell=True, stdout=subprocess.PIPE)
            process_status = ps.stdout.read().decode("utf-8")

        cmd = "pkill -f redis-server"
        returned_value = subprocess.call(cmd, shell=True)
        print("Redis Server shutdown with status =", returned_value)

        if os.path.exists("nohup.out"):
            os.remove("nohup.out")
        if os.path.exists("dump.rdb"):
            os.remove("dump.rdb")

        sys.path.remove(self.task_filepath)
        time.sleep(0.1)
        print(emoji.emojize(":triangular_flag_on_post: TEARDOWN COMPLETE \n", use_aliases=True))
        
    def _process(self):
        """

        :return:
        """
        # -- SETUP --#
        try:
            self.setup()
        except Exception as e:
            print(emoji.emojize(":x: Error encountered in SETUP block.\nError = %(e)s.\nTraceback = %(t)s" % {"e": str(e),
                                                                                                              "t": str(traceback.format_exc())}, use_aliases=True))
            return

        # -- EXECUTE -- #
        try:
            self.execute()
        except Exception as e:
            print(emoji.emojize(":x: Error encountered in EXECUTE block.\nError = %(e)s.\nTraceback = %(t)s" % {"e": str(e),
                                                                                                                "t": str(traceback.format_exc())}, use_aliases=True))
            return

    def main(self):
        """

        :return:
        """
        self._process()
        self.teardown()
        print(emoji.emojize("Done :thumbs_up: \n", use_aliases=True))


if __name__ == "__main__":

    parser = ArgumentParser(description='Parallel processing framework built on top of Celery.')
    parser.add_argument('--task_file', required=True, dest="task_file",
                        help='task file containing function to be parallelised.')
    parser.add_argument('--ip_loc',  required=True, dest='ip_loc',
                        help='input folder location')
    parser.add_argument('--op_loc', required=True, dest='op_loc',
                        help='output folder location')

    args = parser.parse_args()
    r = Runner(args.task_file, args.ip_loc, args.op_loc)
    r.main()
