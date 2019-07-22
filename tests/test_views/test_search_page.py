import pytest

from polka_curses.views.search_page import (
    SearchPage,
    SearchResultsPage,
    SearchResults,
    SearchResultItem,
)


@pytest.fixture
def search_page():
    return SearchPage()


@pytest.fixture
def search_results_page(model):
    return SearchResultsPage(model.search("грибоедов"))


@pytest.fixture
def search_results(search_results_page):
    return search_results_page.results


@pytest.fixture
def search_result_item(search_results):
    return search_results.results[0]


def test_get_search_query(search_page):
    assert search_page.get_search_query() == ""
    search_page.search.edit_text = "abc"
    assert search_page.get_search_query() == "abc"


def test_get_focused_result(search_results):
    focused_object = search_results.get_focused_result()
    assert search_results.results[0].result.object == focused_object


def test_search_result_item_is_selectable(search_result_item):
    assert search_result_item.selectable()
