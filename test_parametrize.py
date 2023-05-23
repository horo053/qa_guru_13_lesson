import pytest
from selenium import webdriver
from selene import browser
"""
Переопределите параметр с помощью indirect параметризации на уровне теста
"""


@pytest.fixture(params=[(2560, 1440), (320, 480), (1920, 1080), (240, 320)])
def open_browser(request):
    chrome_options = webdriver.ChromeOptions()
    browser.config.driver_options = chrome_options
    browser.config.window_height = request.param[0]
    browser.config.window_width = request.param[1]
    yield browser
    browser.quit()


@pytest.mark.parametrize("open_browser", [(2560, 1440), (1920, 1080)], indirect=True)
def test_github_desktop(open_browser):
    open_browser.open('https://github.com/')
    open_browser.element('a.HeaderMenu-link--sign-in').click()


@pytest.mark.parametrize("open_browser", [(320, 480), (240, 320)], indirect=True)
def test_github_mobile(open_browser):
    open_browser.open('https://github.com/')
    open_browser.element('.flex-column [aria-label="Toggle navigation"]').click()
    open_browser.element('a.HeaderMenu-link--sign-in').click()