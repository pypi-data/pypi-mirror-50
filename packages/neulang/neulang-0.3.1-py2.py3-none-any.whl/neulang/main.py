#! /usr/bin/env python3

"""
Neulang: Executable org-formatted pseudocode embedded in Python.
Usage:
    neu [options] [<file>|(--command=<cmd>)]  [(--org-path=<op>)] [-m<modules>] [--to-py]

-v, --version   Print version info.
-i              Open interpreter after executing command.
-o, --org-path=<op>
                Internal traversal path as list of regexes or indices, using sed format (works with <file>).
-m, --modules=<mods>
                List of modules to import, separated by ":".
--command=<cmd>
                Execute a command.
--to-py         Convert code to Python source.
"""


import traceback as tb

import sys
from os.path import exists, join, dirname

from docopt import docopt

from neulang import Neulang, Callee, __meta__
from neulang.neudoc import Neudoc


__all__ = ("run",)
__author__ = __meta__.author
__version__ = __meta__.version


def _run():
    # catch assert errors

    try:
        run()

    except AssertionError as ae:
        tb.print_exc()
        sys.exit(1)
    return


def run():
    opt = docopt(__doc__)
    src_file = opt.get("<file>") or ""
    q_cmd = opt.get("--command") or None
    org_path = opt.get("--org-path") or ""
    org_path = (
        org_path.split(org_path[1])[1:]
        if org_path.startswith("s") and len(org_path) > 2
        else None
    )
    mods = opt.get("--modules") or []
    gen_py = opt.get("--to-py") or None
    if mods:
        mods = mods.split(":")
    neulang = Neulang()
    callee = Callee(namespace=neulang.ns)
    help = Neudoc().help
    neulang.update_namespace(help=help, **callee.to_dict())

    for mod in mods:
        if not exists(mod):
            raise OSError(f'"{mod}" not found.')
        neulang.load(mod)
        neulang.eval()

    if q_cmd:
        if not q_cmd.startswith("* "):
            q_cmd = f"* {q_cmd}"
        neulang.loads(q_cmd)
        neulang.eval()

    if src_file:
        neulang.org_path(org_path)
        neulang.load(src_file)

        if not gen_py:
            neulang.eval()

        else:
            try:
                code = neulang.to_py()
                print(code)

            except Exception as e:
                print(f"{repr(e)}")

    if not (src_file or mods) or opt.get("-i"):
        # enter REPL
        level = 1
        accum = []
        i_char = "\\"
        d_char = "/"
        q_words = ["*quit*", "*exit*"]
        print(f"Neulang {__version__}")
        print(f'Use "{i_char}" or "{d_char}" to indent and deindent nodes.')
        print(f"Evaluate code by entering an empty node after.")
        print(
            f'Type "help" for more information, "{q_words[0]}", "{q_words[1]}" or "CTRL+d" to quit.\n'
        )

        while True:
            # basic interpreter
            rv = ""
            stars = "*" * level
            prompt = f"{stars} "

            try:
                inp = get_inp(prompt).strip()

                if inp == "help":
                    print(
                        "Type help() for interactive help, or help(object) for help about object."
                    )
                    continue

            except KeyboardInterrupt:
                print("\nKeyboardInterrupt")
                continue

            except EOFError:
                print("")
                break

            except StopIteration:
                break

            if inp in q_words:
                break

            if accum and not inp:

                try:
                    neulang.loads("\n".join(accum))

                    if gen_py:
                        code = neulang.to_py()
                        print(f"{code}")

                    try:
                        if not len(accum) == 1:
                            raise SyntaxError("execute instead of evaluate")
                        rv = neulang.eval("eval")
                        if rv is None:
                            rv = ""

                    except (SyntaxError, TypeError) as e:
                        not_expr_msg = "expected some sort of expr"
                        if isinstance(e, TypeError) and not_expr_msg not in e.args[0]:
                            raise
                        neulang.eval()

                    else:
                        print(rv)

                except KeyboardInterrupt:
                    continue

                except Exception as e:
                    tb.print_exc()

                finally:
                    level = 1
                    accum = []
                continue

            if inp is i_char or inp.endswith(i_char):
                inp = inp.rstrip(i_char)
                level += 1

            elif inp is d_char or inp.endswith(d_char):
                inp = inp.rstrip(d_char)
                level -= 1
                if level < 1:
                    level = 1
            if inp:
                accum.append(f"{prompt}{inp}")

    elif opt.get("--version", None):
        print(f"Neulang {__version__}")
    return


def get_inp(*args, **kwds):
    return input(*args, **kwds)


if __name__ == "__main__":
    run()
