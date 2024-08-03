from selenium import webdriver

def before_feature(context, feature):
    context.browser = webdriver.Chrome()

def after_feature(context, feature):
    context.browser.quit()

