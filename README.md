# ListDriversWin
ListDriversWin outputs a list of drivers in JSON format.

## usage
```
usage: ListDriversWin.py [-h] outfile_abs_path

KModules lists the kernel modules with SHA1 and outputs JSON.

positional arguments:
  outfile_abs_path  Absulote path of the output JSON file

optional arguments:
  -h, --help        show this help message and exit
```
## Release
Latest release [here](https://github.com/alwashmi/ListDriversWin/releases/latest)

## output
JSON list of drivers [{}, {}, {}, ...]
Keys:
['Module Name', 'Display Name', 'Description', 'Driver Type', 'Start Mode', 'State', 'Status', 'Accept Stop', 'Accept Pause', 'Paged Pool(bytes)', 'Code(bytes)', 'BSS(bytes)', 'Link Date', 'Path', 'Init(bytes)', '@timestamp', 'SHA1']

## version
1.0

## todo:
check signature

## author
Abdulaziz Alwashmi (@AlwashmiA)
