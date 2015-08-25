# OSU CSEPrint
A tool for printing local files to printers on stdlinux/faclinux
*cseprint has no dependencies outside of the python standard library*

## Setting up SSH keys
It's **strongly** recommended that you set up SSH keys to avoid entering your password every time an SSH command gets executed by the script.

## Installation Instructions:
* `git clone` the repository
* `cd` into the cloned directory
* Run `python setup.py install` (You may have to sudo this depending on your python environment setup)
* `cseprint` should now be an available command on your system

## Usage
Usage of the script is fairly straightforward, it takes three arguments: a domain, a printer, and a local file.  You can also optionally provide the script with a username if your stdlinux/faclinux username differs from your local username.
```
usage: cseprint [-h] [--user USER] [-v] [--version] {faclinux,stdlinux} printer file

Print anything you want to any cse printer.

positional arguments:
  {faclinux,stdlinux}  Subdomain you are printing to.
  printer              Printer you would like to send to.
  file                 The file to send to the printer.

optional arguments:
  -h, --help           show this help message and exit
  --user USER          stdlinux/faclinux username if different from your local one.
  -v, --verbose        Enable verbose logging.
  --version            show program's version number and exit
```
