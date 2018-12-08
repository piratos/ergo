#!/usr/bin/python3

# https://stackoverflow.com/questions/37558271/python-sklearn-deprecation-warning
def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

# https://stackoverflow.com/questions/47068709/your-cpu-supports-instructions-that-this-tensorflow-binary-was-not-compiled-to-u
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import sys
import collections
import logging as log
import argparse

log.basicConfig(format = '[%(asctime)s] (%(levelname)s) %(message)s', level = log.INFO)

from ergo.core.action import Action

from ergo.actions.info import info_args
from ergo.actions.create import create_args
from ergo.actions.optimize import optimize_args
from ergo.actions.train import train_args
from ergo.actions.clean import clean_args
from ergo.actions.view import view_args
from ergo.actions.compare import compare_args
from ergo.actions.serve import serve_args
from ergo.actions.to_fdeep import tofdeep_args

def get_pad(l):
    pad = 0
    for name in l:
        if len(name) > pad:
            pad = len(name)
    return pad

ACTIONS = collections.OrderedDict([
    ("info", Action("info", "Print library versions and hardware info.", info_args)),
    ("create", Action("create", "Create a new project.", create_args)),
    ("optimize-dataset", Action("optimize-dataset", "Perform dataset optimization (removes duplicates and keep a given amount from the main dataset).", optimize_args)),
    ("train", Action("train", "Train a model (use --dataset /path/file.csv to import a dataset the first time).", train_args)),
    ("clean", Action("clean", "Clean a project from temporary datasets (use --all to reset a project state).", clean_args)),
    ("view", Action("view", "View a model structure and accuracy metrics over training.", view_args)),
    ("cmp", Action("cmp", "Evaluate performances of two models against a given dataset.", compare_args)),
    ("serve", Action("serve", "Serve a pretrained model via a REST API.", serve_args)),
    ("to-fdeep", Action("to-fdeep", "Convert a Keras model to fdeep format.", tofdeep_args))
])


def main():
    parser = argparse.ArgumentParser()
    # print help message if we run ergo without argument
    parser.set_defaults(func=lambda x: parser.print_help())
    subparsers = parser.add_subparsers(title="Available commands")

    # add parser from all the actions
    for action in ACTIONS.values():
        action.cb(subparsers, name=action.name, desc=action.description)

    # parse args and run the appropriate function
    args = parser.parse_args()

    try:
        args.func(args)
    except Exception as e:
        log.critical("%s", e)
    return 
