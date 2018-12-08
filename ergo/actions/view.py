import os
import logging as log

from ergo.project import Project

def view_args(subparsers, name, desc):
    parser = subparsers.add_parser(name, desc)
    parser.add_argument("project_path", help="project path to view info about")
    parser.set_defaults(func=action_view)

def action_view(args):

    prj = Project(args.project_path)
    err = prj.load()
    if err is not None:
        log.error("error while loading project: %s", err)
        quit()

    prj.view()
