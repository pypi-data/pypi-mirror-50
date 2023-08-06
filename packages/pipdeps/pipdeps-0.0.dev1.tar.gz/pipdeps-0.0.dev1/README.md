# pipdeps

Pipdeps shows/upgrades outdated packages with respect to existing dependencies.

Python 2.7 is required.

## Usage

```console
$ pipdeps.py --help
usage: pipdeps.py [-h] (-l | -u | -s SHOW [SHOW ...])

Pipdeps shows/upgrades outdated packages with respect to existing
dependencies.

optional arguments:
  -h, --help            show this help message and exit
  -l, --list            show upgradeable packages and versions
  -u, --upgrade         upgrade upgradeable packages
  -s SHOW [SHOW ...], --show SHOW [SHOW ...]
                        show detailed info about upgradeable packages
```
