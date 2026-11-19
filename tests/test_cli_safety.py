from types import SimpleNamespace

import pytest

import cli


def test_run_cmd_uses_argument_vector_and_disables_shell(monkeypatch):
    observed = {}

    def fake_run(args, **kwargs):
        observed["args"] = args
        observed.update(kwargs)
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(cli.subprocess, "run", fake_run)
    assert cli.run_cmd(["git", "status", "-sb"]) == 0
    assert observed["args"] == ["git", "status", "-sb"]
    assert observed["shell"] is False


def test_run_cmd_rejects_empty_command():
    with pytest.raises(ValueError):
        cli.run_cmd([])
