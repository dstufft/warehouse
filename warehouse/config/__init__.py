# SPDX-License-Identifier: Apache-2.0

import enum

__all__ = ["Environment"]


class Environment(enum.StrEnum):
    production = "production"
    development = "development"
