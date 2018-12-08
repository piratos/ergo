import os
import argparse
import logging as log

from ergo.dataset import Dataset

def probability(x):
    x = float(x)
    if x < 0 or x > 1:
        raise argparse.ArgumentTypeError("%r not in range [0.0 - 1.0]" % x )
    return x


def optimize_args(subparsers, name, desc):
    parser = subparsers.add_parser(name, description=desc)
    parser.add_argument("project_path", help="project path to optimize its dataset")
    parser.add_argument("-r", "--reuse-ratio", dest = "reuse", action = "store", type = probability, default = 0.15)
    parser.add_argument("-o", "--output", dest = "output", action = "store", type = str, default = None)
    parser.set_defaults(func=action_optimize_dataset)

def action_optimize_dataset(args):

    path = os.path.abspath(args.project_path)
    if not os.path.exists(path):
        log.error("dataset file %s does not exist", path)
        quit()

    Dataset.optimize(path, args.reuse, args.output) 
