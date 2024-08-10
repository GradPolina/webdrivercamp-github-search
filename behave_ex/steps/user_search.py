from behave import step
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import json

from behave_ex.components.base import Base



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


@step("GitHub Integration API: verify user's {data_type}")
def step_impl(context, data_type):
    base = Base(context.browser)
    url = 'https://api.github.com/users/{username}'
    url_polina = url.format(username='GradPolina')
    response = requests.get(url_polina)
    assert response.status_code == 200
    user_data = response.json()

    if data_type == "Full Name":
        user_xpath = '//article[header]//h4'
        user_element = base.find_element(user_xpath)
        api_user = user_data['name']
        assert user_element.text == api_user, (f"Expected Full Name: {api_user}, "
                                               f"but got: {user_element.text}")
    elif data_type == "Company Name":
        user_xpath = '(//article[header]//*[name() = "svg"]/parent::*)[1]'
        user_element = base.find_element(user_xpath)
        api_user = user_data['company'] if user_data['company'] else ''
        assert user_element.text == api_user, (f"Expected Company Name: {api_user}, "
                                               f"but got: {user_element.text}")
    elif data_type == "Location":
        user_xpath = '(//article[header]//*[name() = "svg"]/parent::*)[2]'
        user_element = base.find_element(user_xpath)
        api_user = user_data['location']
        assert user_element.text == api_user, (f"Expected Location: {api_user}, "
                                               f"but got: {user_element.text}")
    elif data_type == "Bio":
        user_xpath = '//article[header]//p[@class = "bio"]'
        user_element = base.find_element(user_xpath)
        api_user = user_data['bio'] if user_data['bio'] else ""
        assert user_element.text == api_user, (f"Expected Bio: {api_user}, "
                                               f"but got: {user_element.text}")
    elif data_type == "Twitter":
        user_xpath = '//article[header]//p'
        user_element = base.find_element(user_xpath)
        api_user = user_data['twitter_username'] if user_data['twitter_username'] else "@john doe"
        assert user_element.text == api_user, (f"Expected Twitter username: {api_user}, "
                                               f"but got: {user_element.text}")
    elif data_type == "Blog":
        user_xpath = '(//article[header]//*[name() = "svg"]/parent::*)[3]'
        user_element = base.find_element(user_xpath)
        api_user = user_data['blog'] if user_data['blog'] else "https://"
        assert user_element.get_attribute('href') == api_user, (f"Expected Blog URL: {api_user}, "
                                                                f"but got: {user_element.get_attribute('href')}")


@step("Display followers components with max 100 followers")
def step_impl(context):
    base = Base(context.browser)
    followers_component_xpath = '//div[@class="followers"]//article'
    followers_component = base.find_element(followers_component_xpath)
    if not followers_component:
        print("Followers component is not displayed")
    followers_count = len(followers_component.find_elements())
    if followers_count > 100:
        raise (AssertionError(f"Expected max 100 followers, but got {followers_count}"))
    elif followers_count <= 100:
        print("The number of followers is < = 100.")


@step("Each followers has Name and Link")
def step_impl(context):
    url_followers = 'https://api.github.com/users/GradPolina/followers?per_page=100'
    response = requests.get(url_followers)
    api_followers = response.json()
    base = Base(context.browser)
    followers_xpath = '//div[@class="followers"]//article//div'
    ui_followers = base.find_all_elements(followers_xpath)
    assert ui_followers, "No followers found in the UI"
    for api_follower in api_followers:
        name = api_follower.get('login')
        link = api_follower.get('html_url')
        assert name is not None, "Follower from API is missing a name"
        assert link is not None, "Follower from API is missing a link"

        matching_ui_follower = None
        for ui_follower in ui_followers:
            ui_name, ui_link = ui_follower.text.split("\n")
            if ui_name == name:
                assert ui_link == link
                matching_ui_follower = name
                break

        assert matching_ui_follower is not None, f"Follower {name} not found in UI"


@step("Click on the Follow button")
def step_impl(context):
    base = Base(context.browser)
    follow_button_xpath = '//header/a'
    follow_button = base.find_element(follow_button_xpath)
    follow_button.click()
    time.sleep(2)


@step("Verify that redirected to the GitHub follow page for {validUsername}")
def step_impl(context, validUsername):
    current_url = context.browser.current_url
    expected_url = f"https://github.com/{validUsername}"
    assert current_url.startswith(expected_url), (f"Expected to be redirected to {expected_url}, "
                                                  f"but got {current_url}")

url_api = 'https://api.github.com/user'
token = ' '
@step("Authenticated with the GitHub API")
def step_impl(context):
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github+json'
        }
    response = requests.get(url_api, headers=headers)
    if response.status_code == 200:
        print("Authenticated successfully.")
        return headers
    else:
        print(f"Authentication failed: {response.status_code}")
        return None


@step("Send a request to update the {location}")
def update_location(context, location):
    data = {'location': location}
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github+json'
    }
    response = requests.patch(url_api, headers=headers, json=data)
    print(f"Response status code: {response.status_code}")
    return response.json()


@step("GitHub Integration API: verify updated to {location}")
def verify_update(context, location):
    base = Base(context.browser)
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github+json'
    }
    response = requests.get(url_api, headers=headers)
    location_new = response.json()
    assert response.status_code == 200
    user_xpath = '(//article[header]//*[name() = "svg"]/parent::*)[2]'
    user_element = base.find_element(user_xpath)
    api_user = location_new['location']
    assert user_element.text == api_user, (f"Expected Location: {api_user}, "
                                           f"but got: {user_element.text}")
    print("Update successful. New location is:", {user_element.text})







