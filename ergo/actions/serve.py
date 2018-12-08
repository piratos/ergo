import os
import argparse
import logging as log

import pandas as pd
from flask import Flask, request, jsonify

from ergo.project import Project

prj = None
app = Flask(__name__)

@app.route('/')
def route():
    global prj

    x = request.args.get('x')
    if x is None:
        return "Missing 'x' parameter.", 400

    try:
        x = prj.logic.prepare_input(x)
        y = prj.model.predict(x)
        return jsonify(y.tolist())
    except Exception as e:
        #log.exception("error while predicting on %s", x)
        log.error("%s", e)
        return str(e), 400

def serve_args(subparsers, name, desc):
    parser = subparsers.add_parser(name, description=desc)
    parser.add_argument("project_path", help="Path to the trained project")
    parser.add_argument("--host", dest = "host", action = "store", type = str, help="serve address")
    parser.add_argument("--port", dest = "port", action = "store", type = int, default = 8080, help="serve port")
    parser.add_argument("--debug", dest = "debug", action = "store_true", default = False, help="activate debug mode")
    parser.set_defaults(func=action_serve)

def action_serve(args):
    global prj, app

    print(args.project_path, type(args.project_path))
    prj = Project(args.project_path)
    err = prj.load()
    if err is not None:
        log.error("error while loading project: %s", err)
        quit()
    elif not prj.is_trained():
        log.error("no trained Keras model found for this project")
        quit()

    app.run(host=args.host, port=args.port, debug=args.debug)
