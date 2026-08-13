# ------------------------------------------------------------------------------
#  Copyright (c) 2026 Dimitri Kroon.
#  This file is part of plugin.audio.bbcsounds.
#  SPDX-License-Identifier: GPL-3.0-or-later
#  See LICENSE.txt or https://www.gnu.org/licenses/gpl-3.0.txt
# ------------------------------------------------------------------------------
from __future__ import annotations
from tests.support import fixtures
fixtures.global_setup()

from unittest.mock import patch

from resources.lib import menu

from tests.support.testutils import open_doc, HttpResponse


# noinspection PyPep8Naming
setUpModule = fixtures.setup_local_tests
tearDownModule = fixtures.tear_down_local_tests


class TestPages(fixtures.AddonRunner):
    @patch('resources.lib.fetch.get')
    def test_main_page(self, p_req):
        self.run_addon(['plugin://plugin.audio.bbcsounds', '1', '', 'resume:false'], items_count=6)
        p_req.assert_not_called()

    @patch('resources.lib.fetch.get', return_value=HttpResponse(text=open_doc('homepage.html')()))
    def test_home_page(self, p_req):
        argv = self.create_argv('menu', 'list_page', page_url='https://www.bbc.co.uk/sounds/home')
        self.run_addon(argv, p_req, items_count=10)

    @patch('resources.lib.fetch.get', return_value=HttpResponse(text=open_doc('music.html')()))
    def test_music_page(self, p_req):
        argv = self.create_argv('menu', 'list_page', page_url='https://www.bbc.co.uk/sounds/muscic')
        self.run_addon(argv, p_req, items_count=8)

    @patch('resources.lib.fetch.get', return_value=HttpResponse(text=open_doc('podcasts.html')()))
    def test_podcast_page(self, p_req):
        argv = self.create_argv('menu', 'list_page', page_url='https://www.bbc.co.uk/sounds/podcasts')
        self.run_addon(argv, p_req, items_count=11)

    @patch('resources.lib.fetch.get', return_value=HttpResponse(text=open_doc('my-sounds.html')()))
    def test_mysounds_page(self, p_req):
        argv = self.create_argv('menu', 'list_page', page_url='https://www.bbc.co.uk/sounds/my')
        self.run_addon(argv, p_req, items_count=4)


class ContainerContent(fixtures.AddonRunner,):
    @patch('resources.lib.fetch.get', return_value=HttpResponse(text=open_doc('news-summary.json')()))
    def test_news_summary_page(self, p_req,):
        argv = self.create_argv('menu', 'list_container_content', urn='urn:bbc:radio:brand:p0ddbgqd')
        collector = self.run_addon(argv, p_req, items_count=32)
        self.assertEqual('Short Clips', collector.list_item(-1).getLabel())

        p_req.reset_mock()
        argv = self.create_argv('menu', 'list_container_content', urn='urn:bbc:radio:brand:p0ddbgqd', list_clips='true')
        self.run_addon(argv, p_req, items_count=2)

    @patch('resources.lib.fetch.get', return_value=HttpResponse(text=open_doc('collection.json')()))
    def test_collection_content(self, p_req):
        argv = self.create_argv('menu', 'list_container_content', urn='urn:bbc:radio:collection:c0000001')
        self.run_addon(argv, p_req, items_count=20)


class TestRail(fixtures.AddonRunner):
    def test_main_page_rail_content(self):
        for rail_id in (
                'listen_live',
                'continue_listening',
                'unmissable_speech',
                'unmissable_music',
                'latest_playables_for_curation-m001bm45',
                'editorial_collection',
                'local_rail',
                'collections',
                'categories',):
            argv = self.create_argv('menu', 'list_rail', page_url='https://www.bbc.co.uk/sounds', rail_id=rail_id)

            with patch('resources.lib.fetch.get',
                       return_value=HttpResponse(text=open_doc('homepage.html')())) as p_req:
                self.run_addon(argv, p_req, items_min=6)

    def test_music_page_rail_content(self):
        for rail_id in (
                'music_page_curations',
                'music_page_featured_rail',
                'music_page_unmissable_music',
                'mood_categories',
                'container_list_feel_good_tunes',
                'container_list_dance',
                'container_list_chill',
                'music_page_music_categories',
                ):
            with patch('resources.lib.fetch.get', return_value=HttpResponse(text=open_doc('music.html')())) as p_req:
                argv = self.create_argv('menu', 'list_rail', page_url='https://www.bbc.co.uk/music', rail_id=rail_id)
                self.run_addon(argv, p_req, items_min=6)

    def test_podcasts_rail_content(self):
        for rail_id in (
                'speech_page_curations',
                'speech_page_featured_rail',
                'speech_page_recommended_podcasts-we-love',
                'speech_page_recommended_all-time-favourites',
                'container_list_podcasts_factual-crimeandjustice-truecrime',
                'container_list_podcasts_factual-lifestories',
                'container_list_podcasts_factual-history',
                'container_list_podcasts_factual-scienceandnature',
                'container_list_podcasts_comedy',
                'container_list_podcasts_sport',
                'container_list_podcasts',):
            argv = self.create_argv('menu', 'list_rail', page_url='https://www.bbc.co.uk/sounds', rail_id=rail_id)
            with patch('resources.lib.fetch.get',
                       return_value=HttpResponse(text=open_doc('podcasts.html')())) as p_req:
                self.run_addon(argv, p_req, items_min=6)

    def test_rail_by_url(self):
        url = ('https://rms.api.bbc.co.uk/v2/programmes/tleo/playable?all-categories=podcasts,factual-history'
               '&sort=popular&experience=domestic')
        with patch('resources.lib.fetch.get',
                   return_value=HttpResponse(text=open_doc('podcasts_history.json')())) as p_req:
            self.run_callback(menu.list_rail_by_url,
                              {'rail_url': url, 'slug': 'Podcasts / History'},
                              p_req,
                              items_count=104)  # a Next Page item is added because this listing is larger than normally allowed


@patch('resources.lib.search.SearchHistory.update_last_used')
class Search(fixtures.AddonRunner):
    @patch('resources.lib.fetch.get', return_value=HttpResponse(text=open_doc('search_smiths.json')()))
    def test_search_results(self, p_req, _):
        argv = self.create_argv('search', 'do_search', keyword='smiths')
        self.run_addon(argv, p_req, items_count=20)

    @patch('resources.lib.fetch.get', return_value=HttpResponse(text=open_doc('search_no_results.json')()))
    def test_search_without_results(self, p_req, _):
        argv = self.create_argv('search', 'do_search', keyword='blablabla')
        self.run_addon(argv, p_req, items_count=0)
