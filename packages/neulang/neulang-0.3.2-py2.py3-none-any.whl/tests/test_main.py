"""

"""


import pytest

from neulang import main


@pytest.mark.parametrize(
    "inp, e_outp",
    [
        (
            [
                "add_adapt_handler\\",
                "intent_parts\\",
                "say <<req_text>>/",
                "body\\",
                "print(text)",
                "",
                "say success",
                "",
            ],
            "success",
        ),
        (["help"], "Type help()"),
        (['help("__test__")', ""], "neulang.neudoc.Neudoc"),
    ],
)
def test_run_repl(inp, e_outp, mocker, monkeypatch, capsys):
    inp_mock = mocker.Mock(side_effect=inp)
    monkeypatch.setattr(main, "get_inp", inp_mock)
    monkeypatch.setattr(main.sys, "argv", [main.sys.argv[0]])
    main.run()
    captured = capsys.readouterr()
    assert e_outp in captured.out
    return
