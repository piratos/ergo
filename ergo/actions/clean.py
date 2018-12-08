import os
import argparse

from ergo.project import Project

def clean_args(subparsers, name, desc):
    parser = subparsers.add_parser(name, description="cleaner")
    parser.add_argument("project_path", help="project path")
    parser.add_argument("-a", "--all", dest = "all", action = "store_true", default = False, help = "Remove model weights and training data.")
    parser.set_defaults(func=action_clean)

def action_clean(args):
    Project.clean(args.project_path, args.all)
