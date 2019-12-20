import pytest

from polka_curses.views.podcasts_page import PodcastsPage, PodcastItem


@pytest.fixture
def podcastspage(podcasts):
    return PodcastsPage(podcasts)


@pytest.fixture
def podcastitem(podcast):
    return PodcastItem(podcast)


def test_get_podcasts_from_page(podcastspage):
    assert podcastspage.podcasts


def test_get_focused_podcast(podcastspage, model):
    first_focused = podcastspage.get_focused_podcast()
    podcastspage.set_focus(1)
    second_focused = podcastspage.get_focused_podcast()
    assert model.is_podcast(first_focused)
    assert model.is_podcast(second_focused)
    assert first_focused != second_focused


def test_podcast_item_is_selectable(podcastitem):
    assert podcastitem.selectable()
