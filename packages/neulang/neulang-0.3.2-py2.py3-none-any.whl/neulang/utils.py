"""
Helper functions.
"""


from inspect import signature
from pydoc import render_doc
from importlib import util
from functools import wraps


class BetterPartial:
    """Partial allowing flexible use.
    """

    def __init__(self, *args, **kwds):
        args = list(args)
        fst = args.pop(0)
        self._func = func = fst if callable(fst) else args.pop(0)
        a_sig, k_sig = get_sig(func)

        for k, v in kwds.items():
            break
            if fst is False:
                break
            if k not in k_sig and k not in a_sig:
                raise KeyError(f'"{k}" not in call signature')
        self._args = args
        self._kwds = kwds
        self._a_sig = a_sig
        self._k_sig = k_sig
        return

    def __repl__(self):
        cn = self.__class__.__name__
        fn = self._func.__name__
        a = self._args
        k = self._kwds
        return f"{cn}({fn}, *{a}, **{k})"

    def __call__(self, *args, **kwds):
        func = self._func
        p_args = self._args
        p_kwds = self._kwds
        a_sig = self._a_sig
        k_sig = self._k_sig

        for k, v in kwds.items():
            if k in p_kwds:
                raise KeyError(f'"{k}" already exists in the partial')
            # if k not in k_sig and k not in a_sig:
            #    raise KeyError(f'"{k}" not in call signature')
        # p_args.extend(args)
        # p_kwds.update(kwds)
        return func(*(p_args + list(args)), **{**p_kwds, **kwds})


def similar(s1, s2):
    """Simple and naiive calculation of how similar 2 strings are."""
    assert all([isinstance(s, str) for s in [s1, s2]])
    matches = 0
    sf1_list = s1.lower().split(" ")
    sf2_list = s2.lower().split(" ")

    for sf1 in sf1_list:
        for sf2 in sf2_list:
            if sf1 == sf2 or (len(sf2) > len(sf1) and sf1 in sf2) or sf1 in sf2_list:
                matches += 1
    return matches


def get_best_match(item, candids):
    """Compare a string with a list of strings to get the most similar."""
    assert isinstance(candids, list) and all(
        [isinstance(i, str) for i in [item] + candids]
    )
    matches_list = [(similar(item, e), e) for e in candids]
    matches_list.sort(key=lambda i: i[0])
    return matches_list[-1][1]


def call_with_str_args(c, args, kwds):
    """Inspect callable signature and do fixups before calling."""
    assert (
        callable(c) and isinstance(args, list) and isinstance(kwds, dict)
    ), "Bad argument type given"
    types = {"string": str, "integer": int, "boolean": bool, "float": float}

    try:
        sig = signature(c)

    except ValueError:
        print(f"unable to get signature for {c.__name__}")
        sig = None
    docstr = render_doc(c)
    n_args, n_kwds = [], {}

    def try_cast(a):
        if not isinstance(a, str):
            return type(a), a
        a_type, _, a_value = a.partition(" ")

        if a_type in types and a_value:
            # type given
            a_type = types[a_type]
            a_value = a_type(a_value)

        else:
            a_type, a_value = None, a

        if not a_type:
            # guess at type conversion

            if a_value == "false":
                a_type = bool
                a_value = False

            elif a_value == "true":
                a_type = bool
                a_value = True

            elif a_value.isdigit():
                a_type = int
                a_value = int(a_value)

            elif "." in a_value and a_value.replace(".", "", 1).isdigit():
                a_type = float
                a_value = float(a_value)
        return a_type, a_value

    param_names = []
    if sig:
        param_names.extend(sig.parameters.keys())
    doc_params = [
        l.split(":")[1].split(" ")[1] for l in docstr.split("\n") if ":param " in l
    ]
    param_names.extend(doc_params)

    for a in args:
        _, a_val = try_cast(a)
        n_args.append(a_val)

    for k, a in kwds.items():
        _, a_val = try_cast(a)

        if param_names:
            a_key = get_best_match(k, param_names)

        else:
            a_key = a_key.replace(" ", "_")
        n_kwds[a_key] = a_val
    # print(f'{c}({n_args}, {n_kwds})')
    return c(*n_args, **n_kwds)


def load_python_source(path, name=None):
    """Load a Python module from source file."""
    if not name:
        name = name.split(op_sep)[-1].partition(".")[0].replace("-", "_")
    if not name.isidentifier():
        raise NameError(f'"{name}" in not a valid name')
    spec = util.spec_from_file_location(name, path)
    mod = util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def get_sig(func):
    """Get the call signature of a callable."""
    a_sig, k_sig = [], {}

    try:
        sig = signature(func)

    except:
        return None, None

    for k, v in sig.parameters.items():
        if v.default == v.empty:
            a_sig.append(k)

        else:
            k_sig[k] = v
    return a_sig, k_sig


def partial(func, *args, **kwds):
    """Create a partial callable from any arg combination.

    Checks if a key is in the callable signature. First argument should be the callable used for the partial creation or `False`. If `False` then the second arg must be the callble and the check is cancelled.
    """
    if not callable(func):
        raise TypeError("first argument must be a callable")
    if "__new_funcname__" in kwds:
        # 19-08-14_1: lambdas hack
        func.__name__ = kwds["__new_funcname__"]
        del kwds["__new_funcname__"]
    return wraps(func)(BetterPartial(func, *args, **kwds))


def pass_return(func, **ctx):
    """Get the return from context and pass to given callable."""
    return func(ctx["x_return"])


def discard_context(func, **ctx):
    """Call a callable unable to handle context."""
    return func()


def to_var(s):
    """Replace spaces in a string to make a valid name."""
    return s.replace(" ", "_")
