# SPDX-License-Identifier: Apache-2.0

import enum

from dataclasses import dataclass, field
from typing import Annotated, Any, Protocol, Self

from dataclass_settings import Env, load_settings

__all__ = ["Configuration", "Environment", "LogLevel", "Logging", "get"]


class LogLevel(enum.StrEnum):
    Debug = "DEBUG"
    Info = "INFO"
    Warning = "WARNING"
    Error = "ERROR"
    Critical = "CRITICAL"


@dataclass(frozen=True, kw_only=True)
class Logging:
    level: Annotated[LogLevel, Env("LOG_LEVEL")] = LogLevel.Info


class Environment(enum.StrEnum):
    production = "production"
    development = "development"


@dataclass(frozen=True, kw_only=True)
class Configuration:
    logging: Logging = field(default_factory=Logging)

    @classmethod
    def load(cls) -> Self:
        return load_settings(cls)


_PYRAMID_CONFIG_KEY = "warehouse.config"


class _RegistryHaver(Protocol):
    registry: Any


def get(rh: _RegistryHaver) -> Configuration:
    return rh.registry[_PYRAMID_CONFIG_KEY]


def with_config[T: _RegistryHaver](rh: T, config: Configuration) -> T:
    rh.registry[_PYRAMID_CONFIG_KEY] = config
    return rh
