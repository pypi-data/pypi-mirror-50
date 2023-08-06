import os
import subprocess

from .env import parse_file


def run(cmd, env_file=None, virtualenv=None):
    run_in_subprocess(
        cmds=[cmd] if virtualenv is None else [virtualenv_activate(virtualenv), cmd],
        env={} if env_file is None else parse_file(env_file),
    )


def run_in_subprocess(cmds, env):
    if "SYSTEMROOT" in os.environ:
        env["SYSTEMROOT"] = os.environ["SYSTEMROOT"]  # Note: Windows needs

    cmd = " && ".join(cmds)

    if hasattr(subprocess, "run"):
        subprocess.run(cmd, shell=True, check=True, env=env)
    else:
        subprocess.check_call(cmd, shell=True, env=env)


def virtualenv_activate(name):
    if os.name == "nt":
        return "%s\\Scripts\\activate" % (name,)
    else:
        return ". %s/bin/activate" % (name,)
