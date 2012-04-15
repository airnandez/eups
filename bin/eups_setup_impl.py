#!/usr/bin/env python
#
# The EUPS setup programme
#
import sys, os, re

sys.argv[0] = "eups"

# try to recover from an incomplete PYTHONPATH
try:
    import eups.setupcmd
except ImportError:
    eupsdir = None
    if os.environ.has_key("EUPS_DIR"):
        eupsdir = os.environ["EUPS_DIR"]
    else:
        # the first item on sys.path is the script directory (bin)
        eupsdir = os.path.dirname(sys.path[0])
        if not os.path.isabs(eupsdir):
            eupsdir = os.path.join(os.environ['PWD'], eupsdir)
    if eupsdir:
        sys.path[0] = os.path.join(eupsdir, "python")
    else:
        raise
    import eups.setupcmd

from eups.utils import Color
    
allowedDebugOptions = ["", "raise", "debug"]

# parse the command line
setup = eups.setupcmd.EupsSetup()

# set debugging features
debugOptions = re.split("[:,]", setup.opts.debug)
for do in debugOptions:
    if not do in allowedDebugOptions:
        print >> sys.stderr, "Unknown debug option: %s; exiting" % do
        sys.exit(1)
eups.Eups.allowRaise = "raise" in debugOptions # n.b. may be set in a cmdHook
eups.Eups.debugFlag = "debug" in debugOptions

# load any local customizations
verbosity = setup.opts.verbose
if setup.opts.quiet:
    verbosity = -1
eups.hooks.loadCustomization(verbosity, path=eups.Eups.setEupsPath(dbz=setup.opts.dbz))

# run the command
try:
    # N.b. calling sys.exit here raises SystemExit which is caught...
    status = setup.run()
except Exception, e:
    if eups.Eups.allowRaise:
        raise

    setup.err(Color(e, Color.classes["ERROR"]))
    if hasattr(e, "status"):
        status = e.status
    else:
        status = 9
    print("false")

sys.exit(status)
