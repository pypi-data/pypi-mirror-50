"""

"""


import pytest

from neulang import neudoc


class TestNeudoc:
    @pytest.fixture
    def nd(self):
        nd_ = neudoc.Neudoc()
        return nd_

    @pytest.mark.xfail(reason="broken")
    def test_help_output(self, nd, mocker, monkeypatch):
        import sys

        text = "some text"
        n_text = "some string"
        trans_rx = {"some": [["text", "string"]]}
        outp_mock = mocker.Mock()
        monkeypatch.setattr(nd._rw, "_outp", outp_mock)
        monkeypatch.setattr(nd._rw, "_patterns", trans_rx)
        nd._rw._outp.write(text)
        outp_mock.write.assert_called_with(n_text)
        return

    def test_get_doc(self, nd):
        import sys

        sh = nd.get_doc(sys)
        assert isinstance(sh, str) and "built-in module sys" in sh
        return
