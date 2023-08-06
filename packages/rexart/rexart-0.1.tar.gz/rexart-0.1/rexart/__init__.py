__version__ = "0.1"

from dataclasses import dataclass

@dataclass
class VersionInfo:
    major: int = 0
    minor: int = 0
    level: str = ""

    def __post_init__(self):
        self.major = int(self.major)
        self.minor = int(self.minor)

version_info = VersionInfo(*tuple(__version__.split(".")))

del dataclass
