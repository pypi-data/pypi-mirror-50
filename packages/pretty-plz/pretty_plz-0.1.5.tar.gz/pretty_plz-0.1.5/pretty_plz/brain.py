import sys

from pathlib import Path

from pretty_plz.env import Env
from pretty_plz.exceptions import CommandNotFound
from pretty_plz.dotenv import DotEnv, find_project_root


runnable_extensions = (
  ".exe", ".bat", ".cmd", ".sh", ".zsh", ".bash",
)


interpreter_extensions = {
  ".py": sys.executable,
  ".js": "node",
  ".ts": "ts-node",
  ".pl": "perl",
}


class PlzBrain:
  def __init__(self, command):
    DotEnv.load_and_apply()
    self.command = Path(command)
    self.search_paths = [Path(Env.scripts_path())]
    if Env.local_scripts_path():
      self.search_paths.append(find_project_root() / Env.local_scripts_path())

  def runnable_candidates(self):
    for spath in self.search_paths:
      yield spath / self.command
      for ext in runnable_extensions:
        yield spath / (str(self.command) + ext)

  def interp_candidates(self):
    for spath in self.search_paths:
      for ext, interp in interpreter_extensions.items():
        yield (spath / (str(self.command) + ext), interp, )

  def find_command(self):
    for item in self.runnable_candidates():
      if item.exists():
        return (str(item),)
    for item, interp in self.interp_candidates():
      if item.exists():
        return (interp, str(item), )
    raise CommandNotFound(f"Could not find command `{str(self.command)}`")
