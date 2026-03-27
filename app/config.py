"""Application configuration models."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field


class BrowserConfig(BaseModel):
    """Browser runtime configuration."""

    headless: bool = True
    slow_mo_ms: int = Field(default=0, ge=0)
    screenshot_dir: Path = Path("logs")


class SafetyConfig(BaseModel):
    """Safety policy configuration."""

    allow_high_risk_actions: bool = False
    max_steps: int = Field(default=12, ge=1, le=100)


class AppConfig(BaseModel):
    """Top-level application configuration."""

    browser: BrowserConfig = BrowserConfig()
    safety: SafetyConfig = SafetyConfig()

    @property
    def headless(self) -> bool:
        return self.browser.headless

