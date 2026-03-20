import os
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class QuidClawConfig:
    data_dir: Path = field(default=None)

    def __post_init__(self):
        if self.data_dir is None:
            env = os.environ.get("QUIDCLAW_DATA_DIR")
            self.data_dir = Path(env) if env else Path.home() / ".quidclaw"
        self.data_dir = Path(self.data_dir)

    @property
    def main_bean(self) -> Path:
        return self.data_dir / "main.bean"

    @property
    def accounts_bean(self) -> Path:
        return self.data_dir / "accounts.bean"

    @property
    def prices_bean(self) -> Path:
        return self.data_dir / "prices.bean"

    def year_dir(self, year: int) -> Path:
        return self.data_dir / str(year)

    def month_bean(self, year: int, month: int) -> Path:
        return self.year_dir(year) / f"{year}-{month:02d}.bean"
