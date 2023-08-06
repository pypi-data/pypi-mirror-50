"""

"""


import pytest

from neulang import utils as u


sample_param_names = [
    "name",
    "type\\_",
    "\\*args",
    "autoincrement",
    "default",
    "doc",
    "key",
    "index",
    "info",
    "nullable",
    "onupdate",
    "primary_key",
    "server_default",
    "server_onupdate",
    "quote",
    "unique",
    "system",
    "comment",
    "dialect_name",
    "argument_name",
    "default",
    "use_proxies",
    "equivalents",
    "op",
    "\\*other",
    "\\**kwargs",
    "other",
    "autoescape",
    "||",
    "as",
    "escape",
    "||",
    "other",
    "autoescape",
    "ESCAPE",
    "as",
    "escape",
    "ESCAPE",
    "other",
    "escape",
    "other",
    "other",
    "escape",
    "other",
    "autoescape",
    "||",
    "as",
    "escape",
    "||",
    "operator",
    "precedence",
    "is_comparison",
    "return_type",
    "bind",
    "column_keys",
    "dialect",
    "inline",
    "compile_kwargs",
]


@pytest.mark.parametrize("s1, s2, e_retv", [("primary key", "primary_key", 2)])
def test_similar(s1, s2, e_retv):
    retv = u.similar(s1, s2)
    assert retv == e_retv
    return


@pytest.mark.parametrize(
    "item, candids, e_retv", [("primary key", None, "primary_key")]
)
def test_get_best_match(item, candids, e_retv):
    if not candids:
        candids = sample_param_names
    retv = u.get_best_match(item, candids)
    assert retv == e_retv
    return


@pytest.mark.parametrize(
    "c, args, kwds, e_retv",
    [
        (
            lambda uid, primary_key=False: (uid, primary_key),
            ["123"],
            {"primary key": "true"},
            (123, True),
        )
    ],
)
def test_call_with_str_args(c, args, kwds, e_retv):
    retv = u.call_with_str_args(c, args, kwds)
    assert retv == e_retv
    return
