from selenium import webdriver


def set_browser():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    browser = webdriver.Chrome(executable_path='./chromedriver',
                               chrome_options=options
                               )
    return browser
