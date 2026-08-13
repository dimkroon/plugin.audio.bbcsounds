# ------------------------------------------------------------------------------
#  Copyright (c) 2026 Dimitri Kroon.
#  This file is part of plugin.audio.bbcsounds.
#  SPDX-License-Identifier: GPL-3.0-or-later
#  See LICENSE.txt or https://www.gnu.org/licenses/gpl-3.0.txt
# ------------------------------------------------------------------------------

from tests.support import fixtures
fixtures.global_setup()

from unittest import TestCase

from resources.lib import stream


class TestGetJwt(TestCase):
    def get_jwt_of_live(self):
        pass

    def test_get_jwt_of_podcast(self):
        """Audio on demand should not need a JWT."""
        # rise and fall of the smiths, episode 1
        url = 'https://www.bbc.co.uk/sounds/play/m002yzk8'
        result = stream.get_jwt(url)
        self.assertIsNone(result)

    def test_get_jwt_of_live(self):
        """Live streams should need a JWT."""
        url = 'https://www.bbc.co.uk/sounds/play/live/bbc_radio_one'
        result = stream.get_jwt(url)
        self.assertGreater(len(result), 36)