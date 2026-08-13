# ------------------------------------------------------------------------------
#  Copyright (c) 2026 Dimitri Kroon.
#  This file is part of plugin.audio.bbcsounds.
#  SPDX-License-Identifier: GPL-3.0-or-later
#  See LICENSE.txt or https://www.gnu.org/licenses/gpl-3.0.txt
# ------------------------------------------------------------------------------

import time
import requests

from tests.support import fixtures
fixtures.global_setup()

from unittest import TestCase, skip
from unittest.mock import patch, MagicMock

from resources.lib import (
    account,
    fetch,
    stream
)

from tests import credentials


# noinspection unresolved-references
class MockedCookieJar(requests.cookies.RequestsCookieJar):
    def __init__(self, *_):
        # Drop the filename passed to the constructor
        super().__init__()
    load = MagicMock()
    save = MagicMock()


@patch('resources.lib.fetch.LWPCookieJar', MockedCookieJar)
class TestLogin(TestCase):
    def setUp(self):
        fetch.cookie_jar._cj_ = None

    def test_check_valid_email(self):
        with account.LoginSession() as session:
            result = session.check_email(credentials.uname)
            self.assertTrue(result)
        # noinspection unresolved-references
        fetch.cookie_jar().save.assert_not_called()

    def test_check_invalid_email(self):
        with account.LoginSession() as session:
            result = session.check_email('lshalkjhn')
            self.assertFalse(result)
        # noinspection unresolved-references
        fetch.cookie_jar().save.assert_not_called()

    def test_check_valid_email_but_no_associated_account(self):
        with account.LoginSession() as session:
            result = session.check_email('manneke@pis.be')
            self.assertFalse(result)
        # noinspection unresolved-references
        fetch.cookie_jar().save.assert_not_called()

    def test_login_with_valid_password(self):
        with account.LoginSession() as session:
            session.check_email(credentials.uname)
            result = session.sign_in_with_password(credentials.passw)
        self.assertTrue(result)
        cookie_names = [cookie.name for cookie in fetch.cookie_jar()]
        self.assertTrue('ckns_idtkn' in cookie_names)
        self.assertTrue('ckns_atkn' in cookie_names)
        self.assertTrue('ckns_rtkn' in cookie_names)
        # noinspection unresolved-references
        fetch.cookie_jar().save.assert_called_once()

    def test_login_with_invalid_passw(self):
        with account.LoginSession() as session:
            session.check_email(credentials.uname)
            result = session.sign_in_with_password('lshalkjhn')
        self.assertFalse(result)
        cookie_names = [cookie.name for cookie in fetch.cookie_jar()]
        self.assertFalse('ckns_idtkn' in cookie_names)
        self.assertFalse('ckns_atkn' in cookie_names)
        self.assertFalse('ckns_rtkn' in cookie_names)
        # noinspection unresolved-references
        fetch.cookie_jar().save.assert_not_called()


@skip('This should be done manually')
@patch('resources.lib.fetch.LWPCookieJar', new=MockedCookieJar)
class TestSignInByMagicLink(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session = None

    def setUp(self):
        fetch.cookie_jar._cj_ = None

    def test_login_with_email_link(self):
        session = self.session = account.LoginSession()
        session.check_email(credentials.uname)
        session.request_email_link()
        time.sleep(5)
        result = session.check_magic_link_status()
        self.assertIsNone(result)

    def test_check_magic_link_response(self):
        result = self.session._check_magic_link_response()
        self.assertTrue(result)
        # noinspection unresolved-references
        fetch.cookie_jar().save.assert_called_once()

    def close_session(self):
        if self.session:
            self.session.close()


class TestGetJwt(TestCase):
    def get_jwt_of_live(self):
        pass

    def test_get_jwt_of_podcast(self):
        url = 'https://www.bbc.co.uk/sounds/play/m002yzk8'
        result = stream.get_jwt(url)
        self.assertIsNone(result)
