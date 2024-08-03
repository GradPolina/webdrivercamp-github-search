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


@step("GitHub Integration API: verify total number of {options}")
def step_impl(context, options):
    base = Base(context.browser)
    ui_xpath = f'//section[contains(@class, "section-center")]//div[contains(., "{options}")]/h3'
    ui_element = base.find_element(ui_xpath)
    ui_count = int(ui_element.text)
    url = 'https://api.github.com/users/{username}'
    url_polina = url.format(username='GradPolina')
    response = requests.get(url_polina)
    assert response.status_code == 200
    user_data = response.json()
    if options == "repos":
        api_count = user_data['public_repos']
    elif options == "followers":
        api_count = user_data['followers']
    elif options == "following":
        api_count = user_data['following']
    elif options == "gists":
        api_count = user_data['public_gists']

    assert ui_count == api_count, (f"UI repo count ({ui_count})"
                                   f"mismatch with API repo count ({api_count})")


@step("API: send GET request to {url_followers}")
def step_impl(context, url_followers):
    context.response = context.browser.get(url_followers)


@step("GitHub Integration API: verify user's {data_type}")
def step_impl(context, data_type):
    base = Base(context.browser)
    url = 'https://api.github.com/users/{username}'
    url_polina = url.format(username='GradPolina')
    response = requests.get(url_polina)
    assert response.status_code == 200
    user_data = response.json()
    art_header_xpath = '//article[header]'

    if data_type == "Full Name":
        user_xpath = art_header_xpath + '//h4'
        user_element = base.find_element(user_xpath)
        api_user = user_data['name']
        assert user_element.text == api_user, (f"Expected Full Name: {api_user}, "
                                               f"but got: {user_element.text}")
    elif data_type == "Company Name":
        user_xpath = art_header_xpath + '//*[name() = "svg"]/parent::*[1]'
        user_element = base.find_element(user_xpath)
        api_user = user_data['company']
        assert user_element.text == api_user, (f"Expected Company Name: {api_user}, "
                                               f"but got: {user_element.text}")
    elif data_type == "Location":
        user_xpath = art_header_xpath + '//*[name() = "svg"]/parent::*[2]'
        user_element = base.find_element(user_xpath)
        api_user = user_data['location']
        assert user_element.text == api_user, (f"Expected Location: {api_user}, "
                                               f"but got: {user_element.text}")
    elif data_type == "Bio":
        user_xpath = art_header_xpath + '//p[@class = "bio"]'
        user_element = base.find_element(user_xpath)
        api_user = user_data['bio']
        assert user_element.text == api_user, (f"Expected Bio: {api_user}, "
                                               f"but got: {user_element.text}")
    elif data_type == "Twitter":
        user_xpath = art_header_xpath + '//p'
        user_element = base.find_element(user_xpath)
        api_user = user_data['twitter_username']
        assert user_element.get_attribute('href') == api_user, (f"Expected Twitter URL: https://twitter.com/{api_user}, "
                                                                f"but got: {user_element.get_attribute('href')}")
    elif data_type == "Blog":
        user_xpath = art_header_xpath + '//*[name() = "svg"]/parent::*[3]'
        user_element = base.find_element(user_xpath)
        api_user = user_data['blog']
        assert user_element.get_attribute('href') == api_user, (f"Expected Blog URL: {api_user}, "
                                                                f"but got: {user_element.get_attribute('href')}")


@step("Display followers components with max 100 followers")
def step_impl(context):
    base = Base(context.browser)
    followers_component_xpath = '//div[@class="followers"]'
    followers_component = base.find_element(followers_component_xpath)

    assert followers_component is not None, "Followers component is not displayed"
    assert len(followers_component) <= 100, (f"Expected max 100 followers, "
                                             f"but got {len(followers_component)}")


@step("Each followers has Name and Link")
def step_impl(context):
    followers_data = context.followers_data
    assert followers_data is not None, "Followers data not found"

    for follower in followers_data:
        name = follower.get('login', None)
        link = follower.get('html_url', None)
        assert name is not None and link is not None, "Follower missing name or link"

        base = Base(context.browser)
        follower_name_xpath = f"//div[@class='followers']//a[contains(text(), '{name}')]"
        follower_element = base.find_element(follower_name_xpath)
        assert follower_element is not None, f"Follower {name} not found in UI"
        assert follower_element.get_attribute('href') == link, (f"Expected link {link} for follower {name}, "
                                                                f"but got: {follower_element.get_attribute('href')}")
