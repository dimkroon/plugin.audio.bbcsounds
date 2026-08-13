# ------------------------------------------------------------------------------
#  Copyright (c) 2026 Dimitri Kroon.
#  This file is part of plugin.audio.bbcsounds.
#  SPDX-License-Identifier: GPL-3.0-or-later
#  See LICENSE.txt or https://www.gnu.org/licenses/gpl-3.0.txt
# ------------------------------------------------------------------------------

import time
from datetime import datetime

try:
    from zoneinfo import ZoneInfo
except ImportError:
    # python < 3.9
    from backports.zoneinfo import ZoneInfo


def strptime(dt_str: str, format: str) -> datetime:
    """A bug-free alternative to `datetime.datetime.strptime(...)`"""
    return datetime(*(time.strptime(dt_str, format)[0:6]))


