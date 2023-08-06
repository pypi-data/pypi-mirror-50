[![Build Status](https://travis-ci.org/Frechetta/DataXplorer.svg?branch=master)](https://travis-ci.org/Frechetta/DataXplorer) [![codecov](https://codecov.io/gh/Frechetta/DataXplorer/branch/master/graph/badge.svg)](https://codecov.io/gh/Frechetta/DataXplorer)

# DataXplorer

Requires Python 3.7

Install with `pip install datax`, then run with `dx [OPTIONS] [FILES]...`.

Options:
```
  -v, --verbose      Print verbose messages.
  -i, --interactive  Enter into an interactive loop to query data.
  -q, --query TEXT   The query string.
  --help             Show this message and exit.
```

Example:

`dx -q "search n>5" file.txt`

where `file.txt` looks like

```
{"event": 1, "k": "v", "ip": 7, "type": "geoip"}
{"event": 2, "k": "v", "ip": 10, "type": "geoip"}
{"event": 3, "k": "v", "ip": 15, "type": "geoip"}
```

`-q TEXT` is not required if using interactive mode (`-i`). When in interactive mode, you will enter an input loop, allowing you to repeatedly query data without having to execute the command again. This is faster because the data is kept in memory and doesn't have to be loaded from disk each query. Type `exit`, `quit`, or enter `CTRL+C` to quit. Type `search <query-string>` to search the data. If the `-q` and `-i` options are used together, the query will be executed, results will be printed, then you will enter into an input loop.

DataXplorer also accepts data from a pipe. Example: `cat file.txt | dx -q "search n>5"`.

DataXplorer uses [DXQL](https://github.com/Frechetta/DXQL) to search through the data. See the DXQL readme to learn how to search.
