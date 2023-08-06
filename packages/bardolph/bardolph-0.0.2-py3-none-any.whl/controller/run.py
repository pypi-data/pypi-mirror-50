#!/usr/bin/env python

import argparse
import logging

import lib.injection as injection
import lib.job_control as job_control
import lib.settings as settings

import controller.light_module as light_module
import controller.config_values as config_values
from controller.script_runner import ScriptRunner

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file", help="name of the script file", nargs='+')
    ap.add_argument(
        "-f", "--fakes", help="use fake lights", action="store_true")
    ap.add_argument(
        "-r", "--repeat", help="repeat until key pressed", action="store_true")
    ap.add_argument(
        "-v", "--verbose", help="verbose output", action="store_true")
    args = ap.parse_args()
    
    injection.configure()   
    settings.using_base(config_values.functional).configure()
    overrides = {
        'log_date_format': "%I:%M:%S %p",
        'log_format': '%(asctime)s %(filename)s(%(lineno)d): %(message)s',
        'log_level': logging.DEBUG if args.verbose else logging.INFO,
        'log_to_console': True,
        'sleep_time': 0.1
    }
    if args.fakes:
        overrides['use_fakes'] = True
        
    settings.specialize(overrides)
    light_module.configure()

    jobs = job_control.JobControl(args.repeat)   
    for file_name in args.file:
        jobs.add_job(ScriptRunner.from_file(file_name))


if __name__=="__main__":
    main()
