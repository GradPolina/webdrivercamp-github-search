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
    repo_count_xpath = '//span[@id="Repos-count")]'
    repo_count = base.find_element(repo_count_xpath)
    ui_repo_count = int(repo_count.text)
    url = 'https://api.github.com/users/{username}'
    url_polina = url.format(username='GradPolina')
    response = requests.get(url_polina)
    assert response.status_code == 200
    api_repo_count = response.json()['public_repos']
    assert api_repo_count == ui_repo_count, (f"UI repo count ({ui_repo_count})"
                                             f"mismatch with API repo count ({api_repo_count})")


@step("API: send GET request to {followers}")
def step_impl(context, followers):
    context.response = context.browser.get(followers)


@step("GitHub Integration API: verify total number of Followers")
def step_impl(context):
    base = Base(context.browser)
    followers_data_path = '//span[@id="Followers-count")]'
    followers_count = base.find_element(followers_data_path)
    ui_followers_count = int(followers_count.text)
    url = 'https://api.github.com/users/{username}'
    url_polina = url.format(username='GradPolina')
    response = requests.get(url_polina)
    assert response.status_code == 200
    api_followers_count = response.json()['followers']
    assert api_followers_count == ui_followers_count, (f"UI followers {ui_followers_count} "
                                                       f"mismatched with API followers count {api_followers_count}")

    for follower in api_followers_count:
        assert 'login' in follower, f"Follower data missing 'login': {follower}"
        assert 'html_url' in follower, f"Follower data missing 'html_url': {follower}"


@step("GitHub Integration API: verify total number of Following")
def step_impl(context):
    base = Base(context.browser)
    following_data_path = '//span[@id="Following-count")]'
    following_count = base.find_element(following_data_path)
    ui_following_count = int(following_count.text)
    url = 'https://api.github.com/users/{username}'
    url_polina = url.format(username='GradPolina')
    response = requests.get(url_polina)
    assert response.status_code == 200
    api_followers_count = response.json()['following']
    assert api_followers_count == ui_following_count, (f"UI following {ui_following_count} "
                                                       f"mismatched with API following count {api_followers_count}")


@step("GitHub Integration API: verify total number of Gists")
def step_impl(context):
    base = Base(context.browser)
    gists_data_path = '//span[@id="Gists-count")]'
    gists_count = base.find_element(gists_data_path)
    ui_gists_count = int(gists_count.text)
    url = 'https://api.github.com/users/{username}'
    url_polina = url.format(username='GradPolina')
    response = requests.get(url_polina)
    assert response.status_code == 200
    api_followers_count = response.json()['public_gists']
    assert api_followers_count == ui_gists_count, (f"UI Gists {ui_gists_count} "
                                                   f"mismatched with API Gists {api_followers_count}")


@step("GitHub Integration API: verify user's Full Name, Twitter, Bio, Company Name, Location, and Blog")
def step_impl(context):
    base = context.base
    full_name_xpath = '//span[@data-testid="full-name"]'
    twitter_xpath = '//a[@data-testid="twitter-link"]'
    bio_xpath = '//p[@data-testid="bio"]'
    company_name_xpath = '//span[@data-testid="company-name"]'
    location_xpath = '//span[@data-testid="location"]'
    blog_xpath = '//a[@data-testid="blog-link"]'

    full_name_element = base.find_element(full_name_xpath)
    twitter_element = base.find_element(twitter_xpath)
    bio_element = base.find_element(bio_xpath)
    company_name_element = base.find_element(company_name_xpath)
    location_element = base.find_element(location_xpath)
    blog_element = base.find_element(blog_xpath)

    url = 'https://api.github.com/users/{username}'
    url_polina = url.format(username='GradPolina')
    response = requests.get(url_polina)
    assert response.status_code == 200
    user_data = response.json()

    api_full_name = response.json()['name']
    assert full_name_element.text == api_full_name, (f"Expected full name: {api_full_name}, "
                                                     f"but got: {full_name_element.text}")

    api_twitter = response.json()['twitter_username']
    assert twitter_element.get_attribute('href') == api_twitter, (f"Expected Twitter URL: https://twitter.com/{api_twitter}, "
                                                                  f"but got: {twitter_element.get_attribute('href')}")
    api_bio = response.json()['bio']
    assert bio_element.text == api_bio, f"Expected bio: {api_bio}, but got: {bio_element.text}"

    api_company = response.json()['company']
    assert company_name_element.text == api_company, (f"Expected company name: {api_company}, "
                                                      f"but got: {company_name_element.text}")

    api_location = response.json()['location']
    assert location_element.text == api_location, (f"Expected location: {api_location}, "
                                                   f"but got: {location_element.text}")

    api_blog = response.json()['blog']
    assert blog_element.get_attribute('href') == api_blog, (f"Expected blog URL: {api_blog}, "
                                                            f"but got: {blog_element.get_attribute('href')}")


@step("Display followers components with max 100 followers")
def step_impl(context):
    base = context.base
    followers_component_xpath = '//div[@class="followers"]//h4'
    followers_component = base.find_element(followers_component_xpath)

    assert followers_component is not None, "Followers component is not displayed"
    assert len(followers_component) <= 100, (f"Expected max 100 followers, "
                                             f"but got {len(followers_component)}")
