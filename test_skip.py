import pytest
from selenium import webdriver
from selene import browser
"""
Параметризуйте фикстуру несколькими вариантами размеров окна
Пропустите мобильный тест, если соотношение сторон десктопное (и наоборот)
"""

@pytest.fixture(params=[(2560, 1440), (320, 480), (1920, 1080), (240, 320)],
                ids=['desktop', 'mobile', 'desktop', 'mobile'])
def open_browser(request):
    chrome_options = webdriver.ChromeOptions()
    browser.config.driver_options = chrome_options
    browser.config.window_height = request.param[0]
    browser.config.window_width = request.param[1]
    id = request.node.callspec.id                          # взято из https://stackoverflow.com/questions/56466111/how-to-find-the-test-id-for-parametrized-tests-during-execution-of-the-test

    yield browser, id
    browser.quit()


def test_github_desktop(open_browser):
    window, id = open_browser
    if 'mobile' in id:
        pytest.skip('Используется мобильное соотношение сторон')
    window.open('https://github.com/')
    window.element('a.HeaderMenu-link--sign-in').click()


def test_github_mobile(open_browser):
    window, id = open_browser
    if 'desktop' in id:
        pytest.skip('Используется десктопное соотношение сторон')
    window.open('https://github.com/')
    window.element('.flex-column [aria-label="Toggle navigation"]').click()
    window.element('a.HeaderMenu-link--sign-in').click()
