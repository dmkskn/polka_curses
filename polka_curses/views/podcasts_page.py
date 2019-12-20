import urwid
from urwid import LEFT

from polka_curses.config import Palette as p


class PodcastsPage(urwid.ListBox):
    def __init__(self, podcasts):
        self.podcasts = podcasts
        widgets = [PodcastItem(p) for p in self.podcasts]
        super().__init__(urwid.SimpleFocusListWalker(widgets))

    def get_focused_podcast(self):
        widget, _ = self.get_focus()
        return widget.podcast


class PodcastItem(urwid.WidgetWrap):
    def __init__(self, podcast):
        self.podcast = podcast
        body = urwid.Text(self.body)
        body = urwid.Padding(body, left=1, right=1)
        item = urwid.LineBox(body, self.header, LEFT)
        super().__init__(urwid.AttrMap(item, p.frame.name, p.frame_focus.name))

    @property
    def header(self):
        return self.podcast.title

    @property
    def body(self):
        return self.podcast.short_description

    def selectable(self):
        return True
