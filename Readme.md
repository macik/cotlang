# Cotonti Langfile Tools

This repo contains a set of command-line tools which can help translators
to keep localization files up2date.

## Requirements

These tools are written in Python and require Python 2.7 or later to be installed.

## Usage

Common syntax is:

```
python <path_to_script.py> <arguments>
```

### cotlangcp.py

This script can be used to copy only language files from one source tree to another. Type

```
python cotlangcp.py -h
```

to see all options. Example usage:

```
python cotlangcp.py ~/htdocs/cotonti ~/proj/cot-i18n -l ru
```

### cotlangtx.py

This tool is used to generate a config file for our [project on Transifex](https://www.transifex.com/projects/p/cotonti/). It is currently experimental.

Help:

```
python cotlangtx.py -h
```

Example usage:

```
python cotlangtx.py ~/proj/cot-i18n
```

### cotlangfix.py

This tool is used to modify Cotonti lang files and solve incompatibilities with Transifex. It does the following:

* converts array entries into flat entries in several ways;
* detects multiline entries for manual conversion;

Help:

```
python cotlangfix.py -h
```

Example usage:

```
python cotlangfix.py ~/htdocs/cotonti ~/temp/fixed-langs
```

or to modify source tree directly:

```
python cotlangfix.py ~/htdocs/cotonti
```
