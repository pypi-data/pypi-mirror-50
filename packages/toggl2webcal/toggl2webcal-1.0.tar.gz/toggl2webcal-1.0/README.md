# toggl2cal

My tool that exports toggl as webcal file that I serve from my server. 

# Install:

```
    $ pip3 install toggl2webcal --user
```

# Readme

```
usage: toggl2webcal [-h] [-d DAYS] [--no-import] [--no-export] [-o OUT]
                    token database

Export toggl data to webcal file

positional arguments:
  token                 Toggl token
  database              SQL alchemy database connector

optional arguments:
  -h, --help            show this help message and exit
  -d DAYS, --days DAYS  number of days to look back
  --no-import           Don't run import from toggl
  --no-export           Don't run export to webcal
  -o OUT, --out OUT     output path for the webcal file

```

# Example

```
 toggl2webcal TOGGL_TOKEN sqlite:///time.sqlite 
 toggl2webcal TOGGL_TOKEN postgresql://myself@localhost 
```