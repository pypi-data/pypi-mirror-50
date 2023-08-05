import yaml
from os import path
from attrdict import AttrDict

from datacustodian.utility import relpath
from datacustodian.io import read

specs = {}
"""dict: keys are component names; values are a `dict` with component specs.
"""

def load(specfile, asattr=True):
    """Recursively loads the specificied specfile into a :class:`attrdict.AttrDict`.

    Args:
        specfile (str): path to the specification YML file; may be relative.
        asattr (bool): when True, return the spec as a :class:`AttrDict`;
            otherwise, return as-is.
    """
    context, sfile = path.split(path.abspath(specfile))
    spec = read(context, path.splitext(sfile)[0])

    if asattr:
        return AttrDict(spec)
    else:
        return spec
