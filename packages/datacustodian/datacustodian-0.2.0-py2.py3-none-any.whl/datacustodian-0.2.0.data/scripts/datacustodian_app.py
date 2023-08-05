#!python
import logging.config
import argparse
import signal
from os import path
from flask import Flask, Blueprint

from datacustodian.base import testmode
from datacustodian.settings import load, specs
from datacustodian import msg
from datacustodian.utility import relpath, import_fqn
from datacustodian.base import bparser, exhandler
from datacustodian.api import create_api, ServerThread
from datacustodian.writers import component_write
from datacustodian.ipfs import configure as configure_ipfs

app = None
"""flask.Flask: for the overall application.
"""
apis = {}
"""dict: keys are component names; values are the :class:`flask_restplus.Api`
instances for the component.
"""
server = None
"""datacustodian.api.ServerThread: server for the REST API.
"""

logging.config.fileConfig(relpath('datacustodian/templates/logging.conf'))
log = logging.getLogger(__name__)

def examples():
    """Prints examples of using the script to the console using colored output.
    """
    script = "DataCustodian REST API for Local Node"
    explain = ("This scripts starts a REST API on the local machine for each "
               "of the application configuration specifications. See examples "
               "in `docs/configs/*.yml`.")
    contents = [(("Start the local REST API server for two applications."),
                 "app.py records.yml consent.yml",
                 "Each application will run on the same port, but under a "
                 "different URL prefix, as specified in the configuration for the app.")]
    required = ("'app.yaml' file with REST application configuration.")
    output = ("")
    details = ("")
    outputfmt = ("")

    msg.example(script, explain, contents, required, output, outputfmt, details)

script_options = {
    "appspecs": {"help": "File containing the root endpoint specifications.",
                "nargs": '+'},
    "--overwrite": {"help": ("Recreate generated *module* files from scratch."
                             "This does *not* overwrite any package files, "
                             "like setup.py, __init__.py, etc. Use "
                             "--reset-package to do that."),
                "action": "store_true"},
    "--generate": {"help": ("Generate the package code; when not specified, "
                            "only the server will run on existing code."),
                "action": "store_true"},
    "--reset-package": {"help": ("Recreates package files like setup.py, "
                                 "__init__.py, conftest.py from scratch. This nukes "
                                 "*your* changes to the files!"),
                        "action": "store_true"},
    "--norun": {"help": "Don't start the application server.",
                "action": "store_true"}
    }
"""dict: default command-line arguments and their
    :meth:`argparse.ArgumentParser.add_argument` keyword arguments.
"""

def _parser_options():
    """Parses the options and arguments from the command line."""
    pdescr = "Data Custodian REST API"
    parser = argparse.ArgumentParser(parents=[bparser], description=pdescr)
    for arg, options in script_options.items():
        parser.add_argument(arg, **options)

    args = exhandler(examples, parser)
    if args is None:
        return

    return args

def _get_subspec(key, d, ref=None, source=None):
    """Retrieves a sub-specification from the `d`

    Args:
        key (str): name of the attribute to retrieve, if it exists.
        d (dict): specification dictionary to check attributes for.
        ref: if specified and not `None`, then a warning will be printed that
            the attribute is being overridden.
        source (str): source of `d` to use in the warning message if generated.

    Returns:
        The reference object `ref` if the key does not exist; this avoids
        overwriting previous specs that were good with `None`.
    """
    if key in d:
        if ref is not None:
            wmsg = "{} specification is overridden by {}"
            log.warning(wmsg.format(key.capitalize(), source))
        #We use the getattr call here so that a :class:`AttrDict` is returned
        #regular key access returns a regular dict.
        return getattr(d, key)
    else:
        return ref

def _stop_server(signal, frame): # pragma: no cover
    """Cleans up the serial communication and logging.
    """
    global server
    msg.warn("SIGINT >> cleaning up API server.", -1)
    server.shutdown()

def stop():
    """Stops the application server.
    """
    global server
    log.debug("Stopping server with :meth:`shutdown`.")
    server.shutdown()

def start():
    """Starts the server for the application.
    """
    global server
    #Now that the cleanup code is done, we can start the server thread.
    server.start()

def run(appspecs=None, generate=False, overwrite=False, reset_package=False,
        debug=False, norun=False, **args):
    """Initializes the REST application with all configured component endpoints.
    """
    if appspecs is None:
        return

    #Read the global application specification recursively and then update
    #the main flask app's parameters.
    global app
    app = Flask('datacustodian.app')
    srvspec, packspec, appspec, ipfsspec = None, None, None, None

    for compfile in appspecs:
        aspec = load(compfile)
        srvspec = _get_subspec("server", aspec, ref=srvspec, source=compfile)
        packspec = _get_subspec("package", aspec, packspec, compfile)
        appspec = _get_subspec("app", aspec, appspec, compfile)
        ipfsspec = _get_subspec("ipfs", aspec, ipfsspec, compfile)
        if "components" in aspec:
            for compspec in aspec.components:
                specs[compspec.name] = compspec

    if srvspec is not None:
        app.config.update(srvspec)

    #Now, iterate over the components defined for the application and create
    #a python namespace for each, then configure them on the global flask
    #application object at their registered URL prefixes.
    for compname, compspec in specs.items():
        #Create the API object to connect the component to. It is cached in
        #datacustodian.api and datacustodian.app
        api = create_api(appspec, compspec)
        apis[compspec.name] = api
        if generate:
            component_write(appspecs, packspec, compspec, overwrite=overwrite,
                            reset=reset_package)
        if args.get("testing", False):
            #Make sure that a second call without overwrite enabled triggers the
            #right logic paths in the code.
            component_write(appspecs, packspec, compspec, overwrite=False, reset=False)

        #Import the blueprint object that has been initialized for the component.
        fqn = "{}.{}.blueprint".format(packspec.name, compname)
        mod, obj = import_fqn(fqn)
        log.debug("Registering blueprint %r from %s.", obj, fqn)
        app.register_blueprint(obj)

    #If there is an IPFS spec for the cluster, configure the cluster.
    if ipfsspec is not None:
        log.debug("Configuring IPFS with %r", ipfsspec)
        configure_ipfs(**ipfsspec)

    global server
    app.debug = appspec.get("debug", False) or debug

    server = ServerThread(app, srvspec.SERVER_NAME)
    signal.signal(signal.SIGINT, _stop_server)
    if not norun:
        start()

    return app

if __name__ == '__main__': # pragma: no cover
    args = _parser_options()
    run(**args)
