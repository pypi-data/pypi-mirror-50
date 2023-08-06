#!/usr/bin/python
from ruamel import yaml
import argparse
import sys
from os import path

script_options = {
    "target": {"help": ("Specify the `docker-compose.yml` file that should be "
                        "modified with these volumes.")},
    "--add": {"help": ("A list of absolute volume paths to add to the volume "
                       "mapping for the `clearshare` container. Each item "
                       "should be specified in `docker` syntax, i.e., "
                       "/abs/host/path:/abs/container/path"),
              "nargs": '*'},
    "--rm": {"help": ("Remove volume mappings from the clearshare container. "
                      "Each item should be an absolute path on the host."),
             "nargs": '*'}
}
"""dict: default command-line arguments and their
    :meth:`argparse.ArgumentParser.add_argument` keyword arguments.
"""

def _parser_options():
    """Parses the options and arguments from the command line."""
    pdescr = "ClearShare Container Volume Mapper"
    parser = argparse.ArgumentParser(description=pdescr)
    for arg, options in script_options.items():
        parser.add_argument(arg, **options)

    args = vars(parser.parse_known_args()[0])
    if args is None:
        return

    return args

def run(args):
    """Configures the YML file with the volume mapper changes specified.
    """
    target = path.abspath(path.expanduser(args["target"]))
    if not path.isfile(target):
        sys.stderr.write("Specified `docker-compose.yml` file does not exist.")
        sys.stderr.flush()

    with open(target) as f:
        compose = yaml.load(f, Loader=yaml.RoundTripLoader)

    existing = compose["services"]["clearshare"]["volumes"]
    altered = False
    if args["rm"]:
        remainder = []
        for mapping in existing:
            host, cont = mapping.split(':')
            abshost = path.abspath(path.expanduser(host))
            absrm = [path.abspath(path.expanduser(r)) for r in args["rm"]]
            if abshost not in absrm:
                remainder.append(mapping)
            else:
                altered = True
        existing = remainder

    if args["add"]:
        #Make sure we don't have duplicates by some fluke.
        hostpaths = [path.abspath(path.expanduser(m.split(':')[0]))
                     for m in existing]
        for adder in args["add"]:
            ahost, acont = adder.split(':')
            apath = path.abspath(path.expanduser(ahost))
            if apath not in hostpaths:
                existing.append(adder)
                altered = True

    #Finally, overwrite the docker-compose file with the new volume mappings.
    if altered:
        compose["services"]["clearshare"]["volumes"] = existing
        with open(target, 'w') as f:
            f.write(yaml.dump(compose, Dumper=yaml.RoundTripDumper))

if __name__ == '__main__': # pragma: no cover
    args = _parser_options()
    run(args)
