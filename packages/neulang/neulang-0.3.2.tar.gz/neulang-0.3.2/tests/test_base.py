"""

"""


import pytest

from contextlib import nullcontext as dnr  # does_not_raise

from neulang import base


def pr(*a, **k):
    return pytest.raises(*a, **k)


class TestBaseResolver:
    @pytest.fixture
    def br(self):
        return base.BaseResolver()

    @pytest.mark.parametrize(
        "data, e_res, expect",
        [
            (None, None, pr(AssertionError, match=".+but got NoneType")),
            ("a normal sentence", "a normal sentence", dnr()),
            ("air_random list of head args", "list of head args", dnr()),
        ],
    )
    def test__behead(self, br, data, e_res, expect):
        with expect as exp:
            res = br._behead(data)
            assert res == e_res
        return

    @pytest.mark.parametrize(
        "node, e_res, expect",
        [
            ({"head": "test", "body": []}, "inline", dnr()),
            (None, None, pr(AssertionError, match=".*dict but got NoneType")),
            ({"head": "test", "body": ["has body"]}, "full", dnr()),
            ({"head": "air_test some args", "body": ["has body"]}, "combo", dnr()),
            ({"head": "test bodiless nl", "body": []}, "inline", dnr()),
            ({"head": "test bodied nl", "body": ["has body"]}, "full", dnr()),
            (
                {
                    "head": "add_adapt_handler intent part with a <<name>>",
                    "body": ["has body"],
                },
                "combo",
                dnr(),
            ),
            ({"head": "add_adapt_handler intent no body", "body": []}, "inline", dnr()),
            # ({'head': 'test', 'body': []}),
        ],
    )
    def test__node_type(self, br, node, e_res, expect):
        with expect:
            res = br._node_type(node)
            assert res == e_res
        return

    def test__head_args_rx(self, br):
        rx = br._head_args_rx
        assert rx.search("air_say")
        assert rx.search("air_say some text")
        assert rx.search("add_adapt_handler")
        assert rx.search("add_adapt_handler inline intent parts")
        assert not rx.search("add_123_handler")
        return
