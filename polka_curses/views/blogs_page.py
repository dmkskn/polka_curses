import urwid
from urwid import LEFT

from polka_curses.config import Palette as p


class BlogsPage(urwid.ListBox):
    def __init__(self, blogs):
        self.blogs = blogs
        widgets = [BlogItem(b) for b in self.blogs]
        super().__init__(urwid.SimpleFocusListWalker(widgets))

    def get_focused_blog_article(self):
        widget, _ = self.get_focus()
        return widget.blog


class BlogItem(urwid.WidgetWrap):
    def __init__(self, blog):
        self.blog = blog
        body = urwid.Text(self.body)
        body = urwid.Padding(body, left=1, right=1)
        item = urwid.LineBox(body, self.header, LEFT)
        super().__init__(urwid.AttrMap(item, p.frame.name, p.frame_focus.name))

    @property
    def header(self):
        return self.blog.title

    @property
    def body(self):
        return self.blog.short_description

    def selectable(self):
        return True
