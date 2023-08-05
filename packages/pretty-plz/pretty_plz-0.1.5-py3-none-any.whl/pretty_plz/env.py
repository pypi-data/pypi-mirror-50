from os import getenv
from functools import wraps


def _env(var_name, default=None, var_type=str):
  def real_decorator(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
      func()
      value = getenv(var_name, default=default)
      if value == default:
        return default
      return var_type(value)
    return wrapped
  return real_decorator


class Env:
  @_env("PLZ_SCRIPTS_PATH")
  def scripts_path():
    pass

  @_env("PLZ_LOCAL_SCRIPTS_PATH")
  def local_scripts_path():
    pass

  @_env("PLZ_IGNORE_DOTENV", default=False, var_type=bool)
  def ignore_dotenv():
    pass
