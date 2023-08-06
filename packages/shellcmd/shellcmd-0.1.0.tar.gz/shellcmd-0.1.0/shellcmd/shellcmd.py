# -*- coding: utf-8 -*-
"""Pyloco shell command execution task"""

import sys
import tempfile
import subprocess
from pyloco import Task
from pyloco.util import pyloco_shlex, strdecode

PY3 = sys.version_info >= (3, 0)

if sys.platform in ("linux", "linux2"):
    OS = "linux"
elif sys.platform == "darwin":
    OS = "osx"
elif sys.platform == "win32":
    OS = "windows"


class ShellCmd(Task):
    "A shell command library"

    _name_ = "shellcmd"
    _version_ = "0.1.0"

    def system(self, cmd, **kwargs):

        if OS == "windows":
            kwargs["shell"] = True
            if isinstance(cmd, (tuple, list)):
                cmd = " ".join(cmd)
        else:
            if not isinstance(cmd, (tuple, list)):
                cmd = pyloco_shlex.split(cmd)

        tmpout = False
        tmperr = False

        stdout = kwargs.pop("stdout", None)
        stderr = kwargs.pop("stderr", None)

        if stdout is None:
            stdout = tempfile.TemporaryFile()
            tmpout = True

        if stderr is None:
            stderr = tempfile.TemporaryFile()
            tmperr = True

        popen = subprocess.Popen(cmd, stdout=stdout, stderr=stderr,
                                 **kwargs)

        retval = popen.wait()

        if tmpout:
            stdout.seek(0)
            out = strdecode(stdout.read())
            stdout.close()

        else:
            out = stdout

        if tmperr:
            stderr.seek(0)
            err = strdecode(stderr.read())
            stderr.close()

        else:
            err = stderr

        return retval, out, err


    def isystem(self, cmd, **kwargs):

        if OS == "windows":
            kwargs["shell"] = True

            if isinstance(cmd, (tuple, list)):
                cmd = " ".join(cmd)
        else:
            if not isinstance(cmd, (tuple, list)):
                cmd = pyloco_shlex.split(cmd)

        kwargs.pop("stdout", None)
        kwargs.pop("stderr", None)

        p = subprocess.Popen(cmd, stderr=subprocess.PIPE)

        while True:

            out = p.stderr.read(1)
            # if out == '' and p.poll() is not None:
            if out == '' or p.poll() is not None:
                break

            if out != '':
                if PY3:
                    sys.stdout.write(out.decode("utf-8"))

                else:
                    sys.stdout.write(out)

                sys.stdout.flush()

        retval = p.wait()

        return retval

    def __init__(self, parent):

        self.add_data_argument("command", type=str, help="input command")

        self.add_option_argument("-i", "--interactive", action="store_true", help="interactive mode")
        self.add_option_argument("-o", "--option", metavar="param-list", param_parse=True, evaluate=True, help="execution option")

        self.register_forward("retval", type=int, help="return value")
        self.register_forward("stdout", type=str, help="standard output")
        self.register_forward("stderr", type=str, help="standard error")

    def perform(self, targs):

        retval = 0
        stdout = ""
        stderr = ""

        cmd = targs.command
        opts = targs.option.kwargs if targs.option else {}

        if targs.interactive:
            retval = self.isystem(cmd, **opts)

        else:
            retval, stdout, stderr = self.system(cmd, **opts)

        self.add_forward(retval=retval)
        self.add_forward(stdout=stdout)
        self.add_forward(stderr=stderr)
