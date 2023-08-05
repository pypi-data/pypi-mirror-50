import re

from pathlib import Path

from pretty_plz.env import Env


DOTENV_RGX = r"(?:export)?(?P<key>\w+)=(?P<value>.*)"


def find_project_root(indicators=None):
  def find_up(path):
    path = Path(path)
    last_dir = ".."
    current_dir = last_dir
    while True:
      full_path = (current_dir / path).resolve(strict=False)
      if full_path.exists():
        return full_path
      last_dir = current_dir
      current_dir = (current_dir / "..").resolve() # pylint: disable=E1101
      if last_dir == current_dir:
        return None

  root_indicators = indicators or (".git", ".hg", ".svn", ".env")
  for indicator in root_indicators:
    if Path(Path.cwd() / indicator).exists():
      return Path.cwd()
    path = find_up(indicator)
    if path:
      return path.parent
  raise RuntimeError("Couldn't find project root")


class DotEnv:
  def __init__(self, filename):
    self.data = {}
    with open(filename) as dfile:
      for line in dfile:
        match = re.match(DOTENV_RGX, line)
        if match:
          self.data[match.group("key")] = match.group("value")

  def apply(self):
    import os
    os.environ.update(self.data)

  @staticmethod
  def load_and_apply():
    if Env.ignore_dotenv():
      return
    try:
      root = find_project_root()
      filename = root / ".env"
      dotenv = DotEnv(filename)
      dotenv.apply()
    except RuntimeError:
      pass
