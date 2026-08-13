# ------------------------------------------------------------------------------
#  Copyright (c) 2026 Dimitri Kroon.
#  This file is part of plugin.audio.bbcsounds.
#  SPDX-License-Identifier: GPL-3.0-or-later
#  See LICENSE.txt or https://www.gnu.org/licenses/gpl-3.0.txt
# ------------------------------------------------------------------------------

from tests.support import fixtures
fixtures.global_setup()

from unittest import TestCase
from unittest.mock import patch

from resources.lib import account

from tests.support.testutils import open_doc, HttpResponse
from tests.web.test_account import MockedCookieJar


# noinspection PyPep8Naming
setUpModule = fixtures.setup_local_tests
tearDownModule = fixtures.tear_down_local_tests


class TestLoginStatus(TestCase):
    def test_login_status(self):
        signed_in = account.LoginStatus.SIGNED_IN
        self.assertIs(signed_in, account.LoginStatus.SIGNED_IN)
        self.assertIsNot(signed_in, 4)
        self.assertEqual(signed_in, 4)


@patch('resources.lib.fetch.cookie_jar', new=MockedCookieJar)
class TestLoginSession(TestCase):
    @patch('requests.sessions.Session.post',
           return_value=HttpResponse(text=open_doc('signin/response_email_check_with_valid_email.html')()))
    def test_check_email(self, p_post):
        with account.LoginSession() as login:
            login._state = account.LoginStatus.INITIALISED
            result = login.check_email('nlabla')
            p_post.assert_called_once()
            self.assertTrue(result)
            self.assertEqual(account.LoginStatus.EMAIL_ADDR_CHECKED, login.status)

    @patch('requests.sessions.Session.post',
           return_value=HttpResponse(text=open_doc('signin/response_email_check_with_invalid_email.html')()))
    def test_check_email_with_invalid_address(self, p_post):
        with account.LoginSession() as login:
            login._state = account.LoginStatus.INITIALISED
            result = login.check_email('nlabla')
            p_post.assert_called_once()
            self.assertFalse(result)
            self.assertEqual(account.LoginStatus.FAILED, login.status, )

    @patch('requests.sessions.Session.post',
           return_value=HttpResponse(text=open_doc('signin/response_send_email_link.html')()))
    def test_send_email_link(self, p_post):
        with account.LoginSession() as login:
            login._state = account.LoginStatus.EMAIL_ADDR_CHECKED
            login.request_email_link()
            p_post.assert_called_once()
            self.assertEqual(account.LoginStatus.EMAIL_LINK_SENT, login.status)
