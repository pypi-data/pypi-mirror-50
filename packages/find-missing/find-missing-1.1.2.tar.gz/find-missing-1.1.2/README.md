# FIND-MISSING
Find files missing in a folder. This tool is intended to be used with [pipx](https://pipxproject.github.io/pipx/) as a normal command line tool.

## Installation with PIPX
```shell script
pip install pipx
pipx install find-missing
```

## Usage with pipx
```shell script
find-missing "foo, bar, spam.jpg"
```

A file `foolitzer.jpg` will be a match without the `--exact` flag.

### Options

```shell script
find-missing "foo, bar" --exact
```

Looks for exact match, otherwise looks for partial match, so in the above example a file `foo.jpg` will be a match, and a file `foolitzer.jpg` will not.
