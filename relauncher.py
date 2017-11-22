#!/usr/bin/env python

import subprocess
import time
import numpy
import os
import argparse
import ipdb

from collections import OrderedDict

def main(command, user):

    list_commandAndOptions = []
    for opt in command:
        opt_split = opt.split()
        for i, split in enumerate(opt_split):
            opt_split[i] = os.path.normpath(split) # If the arg value is a path, remove the final '/' if there is one at the end.
        list_commandAndOptions += [opt_split]

    # Generate the list of jobs with all the possible combination of the given values
    list_jobs_str = ['']
    for argument in list_commandAndOptions:
        list_jobs_tmp = []
        list_folderName_tmp = []
        for valueForArg in argument:
            for job_str in list_jobs_str:
                list_jobs_tmp += [job_str + ' ' + valueForArg]
        list_jobs_str = list_jobs_tmp

    commands = [job.strip() for job in list_jobs_str]
    job_ids_dict = OrderedDict()
    for command in commands:
        job_ids_dict[command] = -1

    while True:
        squeue = subprocess.check_output('squeue -u ' + user, shell=True)
        running_jobs = [int(job.strip().split()[0]) for job in squeue[:-1].split('\n')[1:]]
        
        for command, job_id in job_ids_dict.items():
            if job_id not in running_jobs:
                output = subprocess.check_output(command, shell=True)
                job_id = int(output[:-1].strip().split()[-1])
                job_ids_dict[command] = job_id
                print command, job_id
        time.sleep(600 + numpy.random.randint(-120,120))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--user', default='sebastien')
    parser.add_argument("command", nargs=argparse.REMAINDER)

    args = parser.parse_args()

    main(args.command, args.user)
