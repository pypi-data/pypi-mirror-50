## pretty_plz, the script command launcher

Put all those useful utility scripts into a central location and
have them magically work from anywhere as simple commands.

1. `pip install pretty-plz`
1. Set `PLZ_SCRIPTS_PATH` to the directory where you store your scripts
1. Call any of your scripts with or without extension from anywere as
   `plz [command] [args]`.

`plz` also automatically reads a project-level `.env` file (unless told not
to do that via the environment).

The intended usage is to set PLZ_SCRIPTS_PATH in your shell, and optionally
set PLZ_LOCAL_SCRIPTS_PATH in the project-level `.env` file.

### Environment variables

`PLZ_SCRIPTS_PATH`

The global home for your utility scripts.

`PLZ_LOCAL_SCRIPTS_PATH`

Project-level home of your utility scripts.

`PLZ_IGNORE_DOTENV`

When set, `plz` will ignore the project-level `.env` file.
