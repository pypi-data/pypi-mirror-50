from datacustodian import msg
from datacustodian.base import bparser, exhandler

def examples():
    """Prints examples of using the script to the console using colored output.
    """
    script = "ClearShare REST API for Local Node"
    explain = ("This scripts starts a REST API on the local machine for a "
               "ClearShare decentralized, privatized storage node.")
    contents = [(("Start the local REST API server."),
                 "app.py",
                 "")]
    required = ("")
    output = ("")
    details = ("")
    outputfmt = ("")

    msg.example(script, explain, contents, required, output, outputfmt, details)

script_options = {}
"""dict: default command-line arguments and their
    :meth:`argparse.ArgumentParser.add_argument` keyword arguments.
"""

def _parser_options():
    """Parses the options and arguments from the command line."""
    pdescr = "ClearShare REST API"
    parser = argparse.ArgumentParser(parents=[bparser], description=pdescr)
    for arg, options in script_options.items():
        parser.add_argument(arg, **options)

    args = exhandler(examples, parser)
    if args is None:
        return

    return args

def run(args):
    """Initializes the REST application with all configured component endpoints.
    """
    from clearshare import app, start, stop
    start()

if __name__ == '__main__': # pragma: no cover
    args = _parser_options()
    run(args)
