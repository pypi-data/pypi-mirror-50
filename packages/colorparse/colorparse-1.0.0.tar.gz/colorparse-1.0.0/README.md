# colorparse

``colorparse`` is a python package that will read and parse strings with defined color codes, showing their respective colors in the terminal. This way, a string can be easily colored, simplifying the work for the user. For the complete documentation, please visit the [github page](https://github.com/tubi-carrillo/colorparse).


# Installation

To install, use this command:
```
  $ pip install colorparse
```

After this, the package should be ready to use. To upgrade or uninstall, use the following:
```
   $ pip install --upgrade colorparse
   $ pip uninstall colorparse
```
# Change Log

\* *the prefixes [t] and [m] refer to terminal and module only changes, respectively.* *

``` diff
# version 1.0.0   (2019 - 07 - 30)
+ [t] The use of `colorparse` without arguments, results in the usage help being displayed.
+ [t] Grouped the option arguments `-v` and `-c` as mutually exclusive arguments.
+ [t] Added new optional argument for reading strings from input file(s) with `-i` or `--input-file`.
+ [t] Replaced the optional argument `-f` for `-o` (`--output-file`).
+ [t] Changed the optional argument for `overflow` to `-O` (uppercase o) or `--overflow`.
+ [t] Added support for special characters to be read from the terminal input `-r` or `--read-special`.

# version 0.0.2   (2019 - 07 - 29)
+ Fixed Windows script file

# release version 0.0.1   (2019 - 07 - 29)
```
