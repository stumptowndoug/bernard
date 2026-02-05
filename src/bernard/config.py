from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

DEFAULT_CONFIG = """[app]
name = "bernard"
metadata_store = "duckdb"

[llm]
provider = "openai"
chat_model = "gpt-4.1-mini"
metadata_model = "gpt-4.1-mini"
"""


@dataclass(frozen=True)
class BernardPaths:
    root: Path
    state_dir: Path
    config_file: Path

    @classmethod
    def from_root(cls, root: Path) -> BernardPaths:
        state_dir = root / ".bernard"
        config_file = state_dir / "config.toml"
        return cls(root=root, state_dir=state_dir, config_file=config_file)


def initialize_project(root: Path) -> BernardPaths:
    paths = BernardPaths.from_root(root)
    paths.state_dir.mkdir(parents=True, exist_ok=True)
    if not paths.config_file.exists():
        paths.config_file.write_text(DEFAULT_CONFIG, encoding="utf-8")
    return paths
