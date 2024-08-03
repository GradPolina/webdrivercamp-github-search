from selenium import webdriver

def before_scenario(context):
    context.browser = webdriver.Chrome()
    context.browser.implicitly_wait(10)

def after_scenario(context):
    context.browser.quit()
