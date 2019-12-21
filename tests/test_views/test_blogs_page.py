import pytest

from polka_curses.views.blogs_page import BlogsPage, BlogItem


@pytest.fixture
def blogspage(blogs):
    return BlogsPage(blogs)


@pytest.fixture
def blogitem(blog):
    return BlogItem(blog)


def test_get_blogs_from_page(blogspage):
    assert blogspage.blogs


def test_get_focused_blog_article(blogspage, model):
    first_focused = blogspage.get_focused_blog_article()
    blogspage.set_focus(1)
    second_focused = blogspage.get_focused_blog_article()
    assert model.is_blog(first_focused)
    assert model.is_blog(second_focused)
    assert first_focused != second_focused


def test_blog_item_is_selectable(blogitem):
    assert blogitem.selectable()
