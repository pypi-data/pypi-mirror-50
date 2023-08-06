# Neulang
Coding for humans.

## Description
Neulang is a natural language enabling layer embedded in Python. It takes scripts containing pseudocode in [Org](http://orgmode.org/) format and runs them.

## Why?
As the easiest programming language for anyone to learn, Python is awesome.
But there's still that curve that continues to shut many out of the coding world.
People shouldn't have to learn another language to code, especially in this age of smart devices, IoT and AI.
Let's bring coding to the people, not the people to coding.
Oh, and I have a lot of pseudocode in Org format that I'd like to make executable.

## Installing
* `pip install neulang`

or clone the latest version from [GitLab](https://gitlab.com/skeledrew/neulang).

## Features
* Command line mode
  * `neu [options] --command="* neu command"`
* Interactive mode
  * `neu [options] [-i]`
  * Exit with `*exit*`, `*quit*` or `CTRL+d`
* Importable from module as an object instance
  * `from neulang import Neulang`
  * `n = Neulang()`
  * `script = "* air_say 'hello world'"`
  * `n.loads(script)`
  * `n.eval()`
* Run script files
  * `neu [options] /path/to/script.neu`
* Run a single node in a script file
  * `neu [options] script.neu -o"s/org/path/as/regex/or/index"`
* Import other Neulang modules from the command line
  * `neu [options] -m"path/to/first/module.neu:another/module.neu"`
* Python-style module access
  * `* include("neulang.natural.basics")` via script
  * `n.load_module("neulang.natural.basics")` via instance
* Transpile Neu to Python source (requires [astor](https://pypi.org/project/astor/))
  * `n.to_py()` via instance
  * `neu script.neu --to-py` via CLI

## Usage
* **NB: This is beta software.**
* For the best experience, use a text editor which supports org-mode. Preferably Emacs as it is used for the project. A sibling project, the NAIC IDE, is also currently under development.
* Activate org-mode on a new buffer (`ALT+x org-mode ENTER`) and write a script as organized pseudocode.
* Modify your pseudocode so it adheres to the operations available in `tests/tests.neu`. The following operational layers are currently available:
  * Regular [Python expression](https://docs.python.org/3/reference/expressions.html) nodes:
    * `* print("Hello world")`
    
    A provisional subset of Python statement-oriented features are also reimplemented as callables to ease transition. These are all prefixed with `x_`:
      * `* x_setv('os', x_import('os'))`
  * ASTIR (Abstract Syntax Tree Intermediate Representation) nodes as a drop-in for statements and expressions (not all are implemented as yet). It is distinguished by keywords beginning with `air_`. The rest tends to, in most cases, correspond to the Python-native name of the operation (though not in this example):
    * `* air_setv`
    * `** my_string`
    * `** This is a string`
    * `* air_call print my_string`
  * Natural language nodes parsed via the [Mycroft Adapt](https://github.com/MycroftAI/adapt) intent parser:
    * The `intent_parts` section takes 1+ valid regular expressions which uses dict groups to enable parsing into an intent. For convenience, named groups can be denoted by double angles, eg. `<<req_my_name>>` expands to `(?P<req_my_name>.+)`.
    * The `body` section is made of any of the layers, and also expands the named groups as individual name-bindings.
    * NB: see `tests.neu` for example usage.
* Run your script: `neu script.neu`
* Provide feedback on your experience, bugs and suggestions for improvement.

## Org-Mode Primer
Org-mode is a rich plain-text system for keeping notes, planning projects and a variety of other organizational tasks. It uses a hierarchial tree structure denoted by stars which can be easily manipulated with keyboard shortcuts. Parts of the text can be folded to show only the general structure and parts currently being worked on. 

These core features are inherited by Neulang, which will in time make coding more a matter of organizing natural phrases/sentences which describe desired operations. Specifically, the org-mode features (and their Emacs bindings) which make Neulang easily manipulable are:
* Create a new node
  * `ALT+ENTER`
* Move a single node up/down
  * `ALT+UP/DOWN`
* Indent/deindent a single node
  * `ALT+LEFT/RIGHT`
* Indent/deindent a node and its children
  * `ALT_SHIFT+LEFT/RIGHT`
* Cycle parent node folding
  * `TAB`

## License
GNU AGPLv3+. See [LICENSE](LICENSE.md).

## Contributing
See [CONTRIBUTING](CONTRIBUTING.md).

## Release Notes
See [CHANGELOG](CHANGELOG.md).

## To Do
* Documentation
* Implement remaining core Python features in AST
* More...

## News and Community
For more information, follow the [Neulang Dev](https://t.me/neulang) channel ([preview here](https://t.me/s/neulang)). Also join the official [Neulang Chat](https://t.me/neulang_chat) on [Telegram](https://telegram.org/) and/or the bridged [Matrix](https://matrix.org/) room at [#neulang:matrix.org](https://matrix.to/#/#neulang:matrix.org).
