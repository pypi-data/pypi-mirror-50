#! /usr/bin/env python3
"""
Access or generate Neu documentation.
"""


import pydoc
import re
import sys


__all__ = ("Neudoc",)


class PydocWrapper:
    def __init__(self, exclude=None):
        exclude = exclude or []

        for attr in dir(pydoc):
            if attr.startswith("_") or attr in exclude:
                continue
            setattr(self, attr, getattr(pydoc, attr))
        return


class Rewriter:
    """Intercept and transform text sent to objects with a .write method"""

    def __init__(self, outp, patterns):
        self._outp = outp
        self._patterns = patterns
        return

    def write(self, text):
        n_text = text

        for seek, reps in self._patterns.items():
            if not re.search(seek, text):
                continue

            for rep in reps:
                n_text = re.sub(rep[0], rep[1], n_text)
        return self._outp.write(n_text)


class Neudoc:
    def __init__(self, *, pubsub=None):
        self._pw = pw = PydocWrapper()
        self._help = h = pw.help
        self._ps = pubsub
        trans_rx = {
            ".*help utility!.*": [
                ("Python .{3,7}'s", "Neu's"),
                ("Python", "Neu"),
                ("https.*tutorial/", "https://neulang.readthedocs.io/en/latest/"),
            ],
            ".*now leaving help.*": [("Python", "Neu")],
        }
        outp = h.output
        self._rw = rw = Rewriter(outp, trans_rx)
        self._rw_stdout = None

        if outp is sys.stdout:
            for attr in dir(outp):
                if hasattr(rw, attr):
                    continue

                try:
                    setattr(rw, attr, getattr(outp, attr))

                except AttributeError:
                    pass
            self._rw_stdout = sys.stdout

        else:
            h._output = Rewriter(outp, trans_rx)
        return

    def help(self, *args, **kwds):
        if args and args[0] == "__test__":
            return f"Testing {repr(self)}"
        rws = self._rw_stdout

        if rws is not None:
            sys.stdout = self._rw
        retv = self._help(*args, **kwds)
        if rws is not None:
            sys.stdout = rws
        return retv

    def cli(self, *args, **kwds):
        return self._pw.cli(*args, **kwds)

    def get_doc(
        self, thing, title="Neu Library Documentation: %s", forceload=0, renderer=None
    ):
        """Render text documentation, given an object or a path to an object."""
        return self._pw.render_doc(thing, title, forceload, renderer)


if __name__ == "__main__":
    Neudoc().cli()
