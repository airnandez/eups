#!/usr/bin/env python
#
# The main eups programme
#
import sys, os, re

sys.argv[0] = "eups"

# try to recover from an incomplete PYTHONPATH
try:
    import eups.cmd
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

import eups.cmd
import eups.hooks
import eups.utils as utils

allowedDebugOptions = ["", "raise", "debug"]

# parse the command line
cmd = eups.cmd.EupsCmd()

# set debugging features
debugOptions = re.split("[:,]", cmd.opts.debug)
for do in debugOptions:
    if not do in allowedDebugOptions:
        print >> utils.stderr, "Unknown debug option: %s; exiting" % do
        sys.exit(1)
eups.Eups.allowRaise = "raise" in debugOptions # n.b. may be set in a cmdHook
eups.Eups.debugFlag = "debug" in debugOptions

# load any local customizations
verbosity = cmd.opts.verbose
if cmd.opts.quiet:
    verbosity = -1
eups.hooks.loadCustomization(verbosity, path=eups.Eups.setEupsPath(path=cmd.opts.path, dbz=cmd.opts.dbz))

# run the command
try:
    # N.b. calling sys.exit here raises SystemExit which is caught...
    status = cmd.run() 
except Exception, e:
    if eups.Eups.allowRaise:
        raise

    cmd.err(str(e))
    if hasattr(e, "status"):
        status = e.status
    else:
        status = 9

sys.exit(status)
