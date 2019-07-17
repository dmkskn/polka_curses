from typing import NamedTuple


class Palette(NamedTuple):
    name: str
    fore: str = ""
    back: str = ""
    mono: str = ""
    fore_high: str = ""
    back_high: str = ""


PALETTE = [
    Palette("frame", fore_high="#000", back_high="#fff"),
    Palette("header", fore_high="#fff", back_high="#00f"),
    Palette("footer", fore_high="#fff", back_high="#00f"),
    Palette("highlighted", fore_high="#000", back_high="#ff0"),
    Palette("highlighted_header", fore_high="#fff", back_high="#f00"),
]
