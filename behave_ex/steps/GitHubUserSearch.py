from behave import step
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests

from behave_ex.components.base import Base


@step('Navigate to {url}')
def step_impl(context, url):
    context.browser = webdriver.Chrome()
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
    url_polina = url.format(username='GradPolina')
    response = requests.get(url_polina)
    api_repo_count = response.json()['public_repos']
    assert api_repo_count == ui_repo_count, (f"UI repo count ({ui_repo_count})"
                                             f"mismatch with API repo count ({api_repo_count})")


@step("API: send GET request to {followers}")
def step_impl(context, followers):
    context.response = context.browser.get(followers)


@step("API: verify status code is {code}")
def step_impl(context, code):
    assert context.response.status_code == code, (f'expected status {code}, '
                                                  f'but got {context.response.status_code}, {context.response.text}')


@step("GitHub Integration API: verify total number of Following")
def step_impl(context):
    base = Base(context.browser)
    followers_data = context.response.json()
    followers_data_path = '//span[@id="Followers-count")]'
    followers_count = base.find_element(followers_data_path)
    user_followers_count = int(followers_count.text)
    assert len(followers_data) == user_followers_count, (f"US followers {user_followers_count} "
                                                         f"mismatched with API followers count {followers_data}")

    for follower in followers_data:
        assert 'login' in follower, f"Follower data missing 'login': {follower}"
        assert 'html_url' in follower, f"Follower data missing 'html_url': {follower}"
