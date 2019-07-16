import pytest
from unittest.mock import patch

from polka_curses.main import main


@patch("polka_curses.main.ViewController")
def test_init_controller_in_main_func(controller):
    main()
    assert controller.called, "ViewController has not been initialized."


@patch("polka_curses.main.ViewController.run")
def test_controller_is_running_in_main_func(run):
    main()
    assert run.called, "ViewController doesn't start the main loop."
