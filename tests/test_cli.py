from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from bernard.cli import app


def test_init_creates_state_dir_and_config(tmp_path: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(app, ["init", str(tmp_path)])

    assert result.exit_code == 0
    assert (tmp_path / ".bernard").exists()
    assert (tmp_path / ".bernard" / "config.toml").exists()


def test_help_lists_commands() -> None:
    runner = CliRunner()
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "init" in result.stdout
    assert "connect" in result.stdout
    assert "schema" in result.stdout
    assert "profile" in result.stdout
    assert "chat" in result.stdout
    assert "ask" in result.stdout
