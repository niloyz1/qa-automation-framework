"""Environment-aware configuration.

Values come from config/environments.yaml (selected by TEST_ENV) and can be
overridden by environment variables, which is how CI injects settings.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONFIG_FILE = ROOT / "config" / "environments.yaml"
DATA_DIR = ROOT / "data"


@dataclass(frozen=True)
class Settings:
    env: str
    portfolio_url: str
    saucedemo_url: str
    api_url: str
    default_timeout_ms: int
    navigation_timeout_ms: int
    mobile: dict[str, Any]


def _env_override(key: str, default: Any) -> Any:
    return os.environ.get(key.upper(), default)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    env = os.environ.get("TEST_ENV", "prod")
    all_envs = yaml.safe_load(CONFIG_FILE.read_text(encoding="utf-8"))
    if env not in all_envs:
        raise ValueError(f"Unknown TEST_ENV '{env}'. Choose one of: {', '.join(all_envs)}")
    cfg = all_envs[env]
    return Settings(
        env=env,
        portfolio_url=_env_override("portfolio_url", cfg["portfolio_url"]).rstrip("/"),
        saucedemo_url=_env_override("saucedemo_url", cfg["saucedemo_url"]).rstrip("/"),
        api_url=_env_override("api_url", cfg["api_url"]).rstrip("/"),
        default_timeout_ms=int(_env_override("default_timeout_ms", cfg["timeouts"]["default_ms"])),
        navigation_timeout_ms=int(_env_override("navigation_timeout_ms", cfg["timeouts"]["navigation_ms"])),
        mobile=cfg["mobile"],
    )


def load_data(name: str) -> Any:
    """Load a YAML file from the data/ folder (test data lives outside the tests)."""
    return yaml.safe_load((DATA_DIR / name).read_text(encoding="utf-8"))
