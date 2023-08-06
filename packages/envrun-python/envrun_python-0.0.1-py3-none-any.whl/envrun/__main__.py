import sys
from argparse import ArgumentParser
from .runner import run

cmd = ArgumentParser(description="Run with environment variables specified in a file")
cmd.add_argument("cmd", help="Command to run")
cmd.add_argument(
    "-f",
    "--env-file",
    default=None,
    help="Environment variables file (.env or YAML or JSON)",
)
cmd.add_argument(
    "-e",
    "--python-virtualenv",
    default=None,
    help="Python virtualenv to run within (optional)",
)


def main(argv=sys.argv):
    args = cmd.parse_args(argv)
    run(env_file=args.env_file, virtualenv=args.python_virtualenv, cmd=args.cmd)


if __name__ == "__main__":
    main()
