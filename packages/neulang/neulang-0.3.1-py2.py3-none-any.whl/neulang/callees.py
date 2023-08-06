"""
Python keywords made callable.
"""


from importlib import import_module


class CalleeException(Exception):
    """ """

    pass


class BreakException(CalleeException):
    """ """

    pass


class ContinueException(CalleeException):
    """ """

    pass


class NotADefaultValue(CalleeException):
    """ """

    def __repr__(self):
        return self.__class__.__name__


NotADefaultValue = NotADefaultValue()


class Callee:
    """ """

    def __init__(self, *, namespace=None):
        if not isinstance(namespace, (dict, type(None))):
            raise ValueError('"namespace" must be a dict or None')
        self._vars = namespace or {}
        return

    @property
    def ns(self):
        """Return the namespace."""
        return self._vars

    def x_setv(self, *names, value=NotADefaultValue):
        """Associate 1+ names with a value.

        Callable alternative to Python's `name = value` statement,
        returns the set value. `NotADefaultValue` is used to ensure
        that `value` is provided, while allowing the call format to
        remain flexible.

        **Limitations**:
          - Unpacking is not supported.

        :param *names: names to be associated
        :param value: value to associate
          (Default value = NotADefaultValue)
        :type names: tuple(str)
        :raise NameError: if all the names aren't valid identifiers
        :raise ValueError: if `value` isn't given
        :return: the associated value
        :rtype: object

        :Example:
        * x_setv('my_num', 15)
        *
        15
        * my_num
        *
        15
        """
        names = list(names)
        if value is NotADefaultValue and len(names) > 1:
            value = names.pop(-1)
        if not all([isinstance(n, str) and n.isidentifier() for n in names]):
            raise NameError(f"names must be valid identifier(s)")
        if value is NotADefaultValue:
            raise ValueError("no value to set")
        for name in names:
            self._vars[name] = value
        return value

    def x_getv(self, *names):
        """Lookup 1+ names.

        If a single defined name is given, the value is returned;
        if 2+ names are given, a tuple of the values are returned.

        :param *names: names to lookup
        :type names: tuple(str)
        :raise NameError: if no names are given, all the names aren't
          valid identifiers or any name is undefined
        :return: value(s) associated with the given name(s)
        :rtype: object or tuple(object)
        """
        if not names:
            raise NameError("no name to get")
        if not all([isinstance(n, str) and n.isidentifier() for n in names]):
            raise NameError(f"names must be valid identifier(s)")
        values = []
        vars = self._vars

        for name in names:
            if name not in vars:
                raise NameError(f'name "{name}" is not defined')
            values.append(vars[name])
        return tuple(values) if len(values) > 1 else values[0]

    def x_delv(self, *names):
        """Delete 1+ names.

        :param *names: name(s) to delete
        :type names: tuple(str)
        :raise NameError: if no names are given, all the names aren't
          valid identifiers or any name is undefined
        :return: value(s) associated with the given name(s)
        :rtype: object or tuple(object)

        :Example:
        * x_setv('my_num', 15)
        *
        15
        * my_num
        *
        15
        * x_delv('my_num')
        *
        (15,)
        * my_num
        *
        Traceback (most recent call last):
          ...
        NameError: name 'my_num' is not defined
        """
        if not names:
            raise NameError("no names to delete")
        if not all([isinstance(n, str) and n.isidentifier() for n in names]):
            raise NameError("must be valid identifier(s)")
        values = []
        vars = self._vars

        for name in names:
            if not name in vars:
                raise NameError(f'name "{name}" is not defined')
            values.append(vars.pop(name))
        return tuple(values)

    def x_if(self, test, body, orelse=None, **ctx):
        """Perform conditional execution.

        Alternative to Python's `if test: body` statement, returns the return value of the executed branch.

        **Limitations**:
          - Only supports 2 branches.

        :param test: 
        :param body: 
        :param orelse:  (Default value = None)
        :param **ctx: 
        """
        if not orelse:

            def orelse(**ctx):
                return retv

        if isinstance(test, str):

            def test(**ctx):
                return eval(test, globals(), ctx)

        if not all([callable(f) for f in [test, body, orelse]]):
            raise Exception("All must be callables")
        retv = None

        if test(**ctx):
            retv = body(**ctx)

        else:
            retv = orelse(**ctx)
        return retv

    def x_for(self, target, seq, body, orelse=None, **ctx):
        """Execute an expression for each element in a sequence.

        `target` must be an identifier or multiple `, `- separated identifiers.

        :param target: Identifier to which each element is assigned
        :param seq: An iterable object
        :param body: Main expression
        :param orelse:  (Default value = None)
        :param **ctx: Context
        :type target: str
        :type seq: collections.Iterable
        :type body: collections.Callable
        :type orelse: None or collections.Callable
        :type ctx: dict
        """
        if (
            not isinstance(target, str)
            or not target.isidentifier()
            and not all([s.isidentifier() for s in target.split(", ")])
        ):
            raise ValueError(
                '"target" must be a string identifier or comma separated identifiers'
            )
        iter(seq)
        if orelse is None:

            def orelse(**ctx):
                return retv

        if not all([callable(f) for f in [body, orelse]]):
            raise ValueError("All must be callables")
        locs = {"seq": seq, "body": body, "orelse": orelse, "retv": None, "ctx": ctx}

        f_loop = f"""
for {target} in seq:
    try:
        retv = body({target}, **ctx)

    except BreakException:
        break

    except ContinueException:
        continue

else:
    retv = orelse(**ctx)"""
        exec(f_loop, globals(), locs)
        return locs.get("retv")

    def x_while(self, test, body, orelse=None, **ctx):
        """Repeatedly execute an expression as long as a test is true.

        :param test: Test to evaluate
        :param body: Expression to execute
        :param orelse: Execute if the loop ended without a `break`
          (Default value = None)
        :param **ctx: Context
        :type test: str or collections.Callable
        """
        if orelse is None:

            def orelse(**ctx):
                return retv

        if isinstance(test, str):
            test_str = test

            def test(**ctx):
                return eval(test_str, globals(), ctx)

        if not all([callable(f) for f in [test, body, orelse]]):
            raise Exception("All must be callables")
        retv = None
        breakout = False

        while test(**ctx):
            try:
                retv = body(**ctx)

            except BreakException:
                breakout = True
                break

            except ContinueException:
                continue

        else:
            if not breakout:
                retv = orelse(**ctx)
        return retv

    def x_break(self, *args, **kwds):
        """Break out of a callable loop.

        Alternative to Python's `break` used by `x_for` and `x_while`.

        :param *args: not used
        :param **kwds: not used
        :raise BreakException: to signal breaking
        """
        raise BreakException()

    def x_continue(self, *args, **kwds):
        """Continue a callable loop.

        Alternative to Python's `continue` used by `x_for` and `x_while`.

        :param *args: not used
        :param **kwds: not used
        :raise ContinueException: to signal continuing
        """
        raise ContinueException()

    def x_do(self, *funcs, **ctx):
        """Run 1+ callables in series, passing context to subsequents.

        The callables must take the context dict as the only argument.
        A good way to do this for callables which take other arguments
        is to use the `functools.partial` decorator to prepare their
        main arguments for passing. The return value of each callable
        is placed in `ctx["return"]` for use by the next callable.

        **Caution**:
          - Care must be taken not to pass a name in the context that
              is also used in a callable's main args.

        :param *funcs: callables to run
        :param **ctx: context to pass
        :type funcs: tuple(collections.Callable)
        :type ctx: dict
        :raise ValueError: if any non-callable is given
        :return: return value of the last callable

        :Example:
        * x_import('functools')
        *
        <module 'functools' from '/.../lib/python3.7/functools.py'>
        * x_setv('fp', functools.partial)
        *
        <class 'functools.partial'>
        * x_setv('add', lambda val, **ctx: val + ctx.get('return', 0))
        *
        <function <lambda> at 0x7f0662f3ea60>
        * x_do(fp(add, 1), fp(add, 2), fp(add, 3))
        *
        6
        """
        if not funcs:
            return None
        funcs = list(funcs)
        if isinstance(funcs[-1], dict) and not ctx:
            ctx = funcs.pop(-1)
        if not all([callable(f) for f in funcs]):
            raise ValueError("Must all be callables")
        retv = None

        for func in funcs:
            retv = func(**ctx)
            ctx["return"] = retv
        return retv

    def x_import(self, *names, packages=None, aliases=None):
        """Import 1+ modules, with optional corresponding aliases.

        This uses Python's `importlib.import_module` to resolve the imports. Modules are bound by alias or name in the active namespace.

        :param *names: name(s) to import
        :param packages: anchor for relative name (Default value = None)
        :param aliases: alias(es) of the name(s) (Default value = None)
        :type names: tuple(str)
        :type packages: None or str or list(None or str)
        :type aliases: None or str or list(None or str)
        :raise NameError: if no names given
        :raise ImportError: if `packages` or `aliases` types are invalid
        :return: imported module(s)
        :rtype: module or tuple(module)

        :Example:
        * x_import('os', 'sys')
        *
        (<module 'os' from '/.../lib/python3.7/os.py'>, <module 'sys' (built-in)>)
        * sys
        *
        <module 'sys' (built-in)>
        """
        if not names:
            raise NameError("no names to import")
        if packages is None:
            packages = [None] * len(names)
        if isinstance(packages, str):
            packages = [packages]
        if not (
            isinstance(packages, (list, tuple))
            and len(packages) == len(names)
            and all([isinstance(p, (str, type(None))) for p in packages])
        ):
            raise ImportError(
                '"packages" must be a string or list of strings for packages corresponding to given names'
            )
        if aliases is None:
            aliases = [None] * len(names)
        if isinstance(aliases, str):
            aliases = [aliases]
        if not (
            isinstance(aliases, (list, tuple))
            and len(aliases) == len(names)
            and all([isinstance(a, (str, type(None))) for a in aliases])
        ):
            raise ImportError(
                '"aliases" must be a string or list of strings for aliases corresponding to given names'
            )
        mods = []
        vars = self._vars

        for name, package, alias in zip(names, packages, aliases):
            mod = import_module(name, package)
            mods.append(mod)
            if alias is None:
                alias = name
            vars[alias] = mod
        return tuple(mods) if len(mods) > 1 else mods[0]

    def x_with(self, *items, body=None, **ctx):
        """Wrap an expression with methods defined by a context manager.

        :param *items: 1+ context expressions
        :param body: Main expression to execute (Default value = None)
        :param **ctx: Any additional context
        :type items: tuple(collections.Callable, None or str)
        :type body: collections.Callable
        :type ctx: dict
        :raise ValueError: if no items are given, they are in an invalid format or body is not a callable
        :return: return value of the wrapped expression
        """
        if not items:
            raise ValueError("no items to create context")
        items = list(items)
        if body is None:
            body = items.pop(-1)
        if (
            len(items) == 2
            and callable(items[0])
            and isinstance(items[1], (str, type(None)))
        ):
            items = [items]
        if all(
            [
                (
                    isinstance(i, (list, tuple))
                    and len(i) == 2
                    and callable(i[0])
                    and isinstance(i[1], (str, type(None)))
                )
                for i in items
            ]
        ):
            items = {i[1]: i[0] for i in items}
        if not (
            isinstance(items, dict)
            and all([isinstance(n, (str, None)) for n in items.keys()])
            and all([callable(i) for i in items.values()])
        ):
            raise ValueError("Bad items format")
        if not callable(body):
            raise ValueError('"body" must be callable')
        header = ", ".join(
            [f"{v.__name__}()%s" % (f" as {k}" if k else "") for k, v in items.items()]
        )
        w_args = ", ".join([k for k in items if isinstance(k, str)])
        if w_args:
            w_args += ", "
        e_ctx = {c.__name__: c for c in items.values()}
        locs = {"body": body, "retv": None, "ctx": ctx, **e_ctx}
        w_ctx = f"""
with {header}:
    retv = body({w_args}**ctx)
        """
        exec(w_ctx, globals(), locs)
        return locs.get("retv")

    def x_class(self, name, attrdict, bases=None, decorators=None):
        """Define a class object.

        :param name: Name to give the class
        :param attrdict: Attributes to attach
        :param bases: Class(es) to inherit from (Default value = None)
        :param decorators:  (Default value = None)
        :type name: str
        :type attrdict: dict
        :type bases: None or tuple(type)
        :type decorators: None or list(collections.Callable)
        """
        retv = None
        if not (
            isinstance(attrdict, dict)
            and all([isinstance(k, str) and k.isidentifier() for k in attrdict])
        ):
            raise ValueError("Class attrdict must be a dict of attribs")
        if bases is None:
            bases = ()
        if decorators is None:
            decorators = []
        cls = type(name, bases, attrdict)

        for d in decorators:
            cls = d(cls)
        return cls

    def x_try(self, body, *handlers, orelse=None, finalbody=None, **ctx):
        """Specify exception handlers or cleanup code for an expression.

        :param body: Expression to try
        :param *handlers: Exceptions to handle
        :param orelse: Execute if no exception raised and it is a callable (Default value = None)
        :param finalbody: Always execute at the end if is a callable (Default value = None)
        :param **ctx: Context

        """
        if not callable(body):
            raise ValueError('"body" must be callable')
        if not (
            isinstance(handlers, (list, tuple))
            and all(
                [
                    (
                        isinstance(h, (list, tuple))
                        and len(h) == 2
                        and (
                            isinstance(h[0], Exception)
                            or hasattr(h[0], "with_traceback")
                        )
                        and callable(h[1])
                    )
                    for h in handlers
                ]
            )
        ):
            raise ValueError(
                '"handlers" must be a list or tuple of exception, callable handler lists/tuples'
            )
        if orelse is None:

            def orelse(**ctx):
                return retv

        if finalbody is None:

            def finalbody(**ctx):
                return retv

        if ctx is None:
            ctx = {}
        retv = None

        try:
            retv = body(**ctx)

        except Exception as exc:
            for h in handlers:
                if type(exc) == h[0]:
                    retv = h[1](exc, **ctx)
                    break

            else:
                raise

        else:
            retv = orelse(**ctx)

        finally:
            retv = finalbody(**ctx)
        return retv

    def x_raise(self, exc, *args, **kwds):
        """Raise an exception.

        Exception can either be given as a class or instance. If the former then `args` and `kwds` are used to construct the instance.

        **Limitations**:
          - Re-raising is not supported.

        :param exc: Exception to raise
        :param *args: 
        :param **kwds: 
        :type exc: BaseException
        :raise TypeError: if `exc` is not an exception class or instance
        """
        if callable(exc) and isinstance(exc(), BaseException):
            exc = exc(*args, **kwds)
        if not isinstance(exc, BaseException):
            raise TypeError("exceptions must derive from BaseException")
        raise exc

    def to_dict(self):
        """Return the "x_" methods as a dict."""
        cs = {}

        for name in dir(self):
            if name.startswith("x_"):
                cs[name] = getattr(self, name)
        return cs
