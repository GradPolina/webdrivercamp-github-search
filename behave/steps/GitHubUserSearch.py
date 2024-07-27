from behave import step
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import requests

from behave.components.base import Base


@step('Navigate to {url}')
def step_impl(context, url):
    context.browser.get(url)
    time.sleep(2)


@step('UI: Search for {username}')
def step_impl(context, username):
    base = Base(context.browser)
    search_box_xpath = '//input[@data-testid="search-bar"]'
    search_box = base.find_element(search_box_xpath)
    search_box.clear()
    search_box.send_keys(username)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)


@step("GitHub Integration API: verify total number of Repos")
def step_impl(context):
    base = Base(context.browser)
    repo_count_xpath = '//h3[contains(text(),"8")]'
    repo_count = base.find_element(repo_count_xpath)
    ui_repo_count = int(repo_count.text)
    url = 'https://api.github.com/users/{username}'
    username = 'GradPolina'
    response = requests.get(url)
    api_repo_count = response.json()

    assert ui_repo_count == api_repo_count, f"UI repo count ({ui_repo_count}) does not match API repo count ({api_repo_count})"
