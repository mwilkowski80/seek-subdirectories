# seek-subdirectories

This tool allows you to find common subdirectories. I created it when made a copy of a Dropbox folder (including shared directories) and needed to find which directories were shared by other Dropbox account (being effectively duplicates).

This software works on the `find` command line output.

## Getting started

Just run:

```
python3 setup.py install
# or: sudo python3 setup.py install 
```

Run `find` against directories that you want to compare

```
find /path/to/directory1 >find-output1.txt
find /path/to/directory2 >find-output2.txt
```

Run this tool to compare outputs:

```
seek-subdirectories --find-output-filepath1 find-output1.txt --find-output-filepath2 find-output2.txt >comparison-result.csv
```

and then check results in LibreOffice or any other CSV editor of your choice.

## FAQ

#### Why a manual step of running `find`? Why the software does not run it automatically?

Because I needed to compare outputs from different machines, so I needed to work on `find` output anyway. I consider this option more powerful than running `find` locally. I would need option to parse `find` output anyway and I am a bit too lazy to make it so configurable :).
