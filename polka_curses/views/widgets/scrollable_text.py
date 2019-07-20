import urwid
from urwid import LEFT, SPACE


class ScrollableText(urwid.Text):
    def __init__(self, markup, align=LEFT, wrap=SPACE, layout=None, offset=1):
        self.offset = offset
        self._cache_trim_top = 0
        super().__init__(markup)

    def selectable(self):
        return True

    def render(self, size, focus=False):
        maxcol, maxrow = size

        super_canvas = super().render((maxcol,), focus)
        final_canvas = urwid.CompositeCanvas(super_canvas)

        cols, rows = final_canvas.cols(), final_canvas.rows()

        if cols <= maxcol:
            width = maxcol - cols
            if width > 0:
                final_canvas.pad_trim_left_right(0, width)

        if rows <= maxrow:
            height = maxrow - rows
            if height > 0:
                final_canvas.pad_trim_top_bottom(0, height)

        if cols <= maxcol and rows <= maxrow:
            return final_canvas

        trim_top = self._cache_trim_top
        trim_end = rows - maxrow - trim_top
        trim_right = cols - maxcol

        if trim_top > 0:
            final_canvas.trim(trim_top)

        if trim_end > 0:
            final_canvas.trim_end(trim_end)

        if trim_right > 0:
            final_canvas.pad_trim_left_right(0, -trim_right)

        return final_canvas

    def keypress(self, size, key):
        if key == "up":
            self._scroll_up(size)
        elif key == "down":
            self._scroll_down(size)
        else:
            return key

    def _scroll_up(self, size):
        new_trim_top = self._cache_trim_top - self.offset
        self._cache_trim_top = self._ensure_bounds(size, new_trim_top)
        self._invalidate()

    def _scroll_down(self, size):
        new_trim_top = self._cache_trim_top + self.offset
        self._cache_trim_top = self._ensure_bounds(size, new_trim_top)
        self._invalidate()

    def _ensure_bounds(self, size, new_trim_top):
        maxcol, maxrow = size
        rows = self.rows((maxcol,))
        return max(0, min(rows - maxrow, new_trim_top))
