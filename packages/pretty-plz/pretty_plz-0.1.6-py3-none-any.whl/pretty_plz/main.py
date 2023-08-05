import sys

from pretty_plz.env import Env
from pretty_plz.brain import PlzBrain
from pretty_plz.return_codes import ReturnCodes
from pretty_plz.exceptions import CommandNotFound


def main():
  if Env.scripts_path() == None:
    print("Error: set $PLZ_SCRIPTS_PATH!")
    sys.exit(ReturnCodes.NO_PLZ_DIR)

  from argparse import ArgumentParser, REMAINDER
  parser = ArgumentParser()
  parser.add_argument("command")
  parser.add_argument("cli", nargs=REMAINDER)
  args = parser.parse_args()

  try:
    brain = PlzBrain(args.command)
    resolved_cmd = brain.find_command()
    import subprocess
    proc = subprocess.run([*resolved_cmd, *args.cli])
    sys.exit(proc.returncode)
  except CommandNotFound as exc:
    print(f"Error: {exc}")
    sys.exit(ReturnCodes.NOT_FOUND)
  except PermissionError:
    print("Error: command found, but it isn't executable!")
    sys.exit(ReturnCodes.NOT_EXECUTABLE)
