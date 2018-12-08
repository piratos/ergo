import sys
import os
import logging as log

from ergo.project import Project


def create_args(subparsers, name, desc):
    parser = subparsers.add_parser(name, description=desc)
    parser.add_argument("project_path", help="new project path")
    parser.set_defaults(func=action_create)

def action_create(args):

    path = args.project_path

    if os.path.exists(path):
        log.error("path %s already exists" % path)
        quit()
    
    log.info("creating %s ..." % path) 
    os.makedirs(path, exist_ok=True)

    Project.create(path)
