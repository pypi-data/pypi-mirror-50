from os import path, mkdir
import sys
from jinja2 import Environment, PackageLoader

def package_init(packspec, reset=False):
    """Initializes the generated package folder structure, if it doesn't already
    exist.

    Args:
        packspec (AttrDict): specification for the overall application, which
            includes path information for the generated component.
        reset (bool): when True, reset the package files like setup.py,
            __init__.py, conftest.py to auto-generated status. This nukes the
            local changes made manually.

    Returns:
        tuple: `(root, coderoot, testroot)`, where root is the repository root folder,
        and `coderoot` is the sub-directory where python code is stored. `testroot`
        is the directory to the `tests` directory for unit testing.
    """
    root = path.abspath(path.expanduser(packspec.root))
    #Make sure that the repository root path is in the python path for dynamic
    #imports of the generated package.
    if root not in sys.path:
        sys.path.insert(0, root)
    coderoot = path.join(root, packspec.name)
    testroot = path.join(root, "tests")

    if not path.isdir(root): # pragma: no cover
        mkdir(root)
    if not path.isdir(coderoot): # pragma: no cover
        mkdir(coderoot)
    if not path.isdir(testroot): # pragma: no cover
        mkdir(testroot)

    setup = path.join(root, "setup.py")
    init = path.join(coderoot, "__init__.py")
    conftest = path.join(testroot, "conftest.py")

    env = Environment(loader=PackageLoader('datacustodian', 'templates'))
    t_setup = env.get_template("setup.py")
    t_init = env.get_template("init.py")
    t_tests = env.get_template("conftest.py")

    if not path.isfile(setup) or reset:
        with open(setup, 'w') as f:
            f.write(t_setup.render(**packspec))
    if not path.isfile(init) or reset:
        with open(init, 'w') as f:
            f.write(t_init.render(**packspec))
    if not path.isfile(conftest) or reset:
        with open(conftest, 'w') as f:
            f.write(t_tests.render(**packspec))

    return root, coderoot, testroot

def component_write(packspec, compspec, overwrite=False, reset=False):
    """Writes the python code file for the specified component specification so
    that a :class:`flask.Blueprint` can be created via direct import.

    Args:
        packspec (AttrDict): specification for the derived package, which
            includes path information for the generated component.
        compspec (AttrDict): component specification to create.
        overwrite (bool): when True, overwrite the module file if it already
            exists.
        reset (bool): when True, reset the package files like setup.py,
            __init__.py, conftest.py to auto-generated status. This nukes the
            local changes made manually.
    """
    root, coderoot, testroot = package_init(packspec, reset=reset)
    target = path.join(coderoot, "{}.py".format(compspec.name))
    if path.isfile(target) and not overwrite:
        return

    env = Environment(loader=PackageLoader('datacustodian', 'templates'))
    template = env.get_template("component.py")
    cpspec = compspec.copy()
    cpspec["package"] = packspec

    if not path.isfile(target) or overwrite:
        with open(target, 'w') as f:
            f.write(template.render(**cpspec))

    #Also create the unit tests for this component with all specified HTTP
    #methods already coded (albeit without the data to make them work).
    testfile = path.join(testroot, "test_{}.py".format(compspec.name))
    t_test = env.get_template("t_component.py")
    if not path.isfile(testfile) or overwrite:
        with open(testfile, 'w') as f:
            f.write(t_test.render(**cpspec))
