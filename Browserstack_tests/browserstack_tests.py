from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.common.by import By
from queue import Queue
from threading import Thread
import requests
import os, json
import unittest
import time


CONFIG_FILE = os.environ['CONFIG_FILE'] if 'CONFIG_FILE' in os.environ else 'single.json'
TASK_ID = int(os.environ['TASK_ID']) if 'TASK_ID' in os.environ else 0

with open(CONFIG_FILE) as data_file:
    CONFIG = json.load(data_file)

BROWSERSTACK_USERNAME = os.environ['BROWSERSTACK_USERNAME'] if 'BROWSERSTACK_USERNAME' in os.environ else CONFIG['user']
BROWSERSTACK_ACCESS_KEY = os.environ['BROWSERSTACK_ACCESS_KEY'] if 'BROWSERSTACK_ACCESS_KEY' in os.environ else CONFIG['key']

environments = [
    {
        "browser": "chrome",
        "browser_version": "73.0",
        "os": "Windows",
        "os_version": "10"
    },
    {
        "browser": "firefox",
        "browser_version": "66.0",
        "os": "Windows",
        "os_version": "10"
    },
    {
        "browser": "safari",
        "os": "OS X",
        "os_version": "Mojave"
    },
    {
        "browser": "Edge",
        "browser_version": "18.0",
        "os": "Windows",
        "os_version": "10"
    }]

q = Queue(maxsize=0)

for environment in environments:
    q.put(environment)

num_threads = 10



def run_test(q):
    while q.empty() is False:
        tests_successful = False
        try:
            # Setup
            environment = q.get()
            print("%s: Starting" % environment["browser"])
            for key in CONFIG["capabilities"]:
                if key not in environment:
                    environment[key] = CONFIG["capabilities"][key]
            driver = webdriver.Remote(desired_capabilities=environment,
                                      command_executor="http://%s:%s@%s/wd/hub" % (BROWSERSTACK_USERNAME, BROWSERSTACK_ACCESS_KEY, 'hub.browserstack.com'))

            #Start actually testing the code
            driver.get("http://connectid.pythonanywhere.com/")
            assert "Connect-ID" in driver.title
            driver.find_element_by_xpath \
                ("//*[@id=\"page-top\"]/header/div/div/a").click()

            WebDriverWait(driver, 10).until(expected.title_is('LinkedIn Login, LinkedIn Sign in | LinkedIn'))
            driver.find_element_by_id("username").send_keys("jeroen.jerry@hotmail.com")
            elem = driver.find_element_by_id("password")
            elem.send_keys("linkedintest!")
            elem.submit()
            WebDriverWait(driver, 10).until(expected.title_is('Connect-ID'))
            assert "Connect-ID" in driver.title

            # navigate through the page and see if things work, mac already fails with finding the css selector...
            #driver.find_element_by_css_selector("body > div:nth-child(3) > div > div.col-lg-3.hidden-sm.hidden-md > div > div > div > div > h5 > a").click()
            driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div/div/div/div/h5/a").click()
            assert "Create a new project" in driver.page_source

            driver.find_element_by_css_selector("body > div:nth-child(3) > div > form > button").click()
            assert "This field is required" in driver.page_source

            navbar_element = driver.find_element_by_css_selector("#navbarSupportedContent > ul > li:nth-child(2) > a")
            if not navbar_element.is_displayed():
                driver.find_element_by_css_selector("body > nav > button > span").click()
            navbar_element.click()
            assert "jeroentest veltmans" in driver.page_source      #take name of the logged in test user

            navbar_element = driver.find_element_by_css_selector("#navbarSupportedContent > ul > li:nth-child(3) > a")
            if not navbar_element.is_displayed():
                driver.find_element_by_css_selector("body > nav > button > span").click()
            navbar_element.click()
            #could send test message and see if this one is shown or not

            navbar_element = driver.find_element_by_id("navbarDropdown")
            if not navbar_element.is_displayed():
                driver.find_element_by_css_selector("body > nav > button > span").click()
            navbar_element.click()
            driver.find_element_by_css_selector("#navbarSupportedContent > ul > li.nav-item.dropdown.show > div > a:nth-child(3)").click()
            assert "Create a new project" in driver.page_source

            '''   
            navbar_element = driver.find_element_by_id("navbarDropdown")
            if not navbar_element.is_displayed():
                driver.find_element_by_css_selector("body > nav > button > span").click()
            navbar_element.click()

            second_element = driver.find_element_by_css_selector("#navbarSupportedContent > ul > li.nav-item.dropdown.show > div > a:nth-child(1)")
            
            assert "jeroentest veltmans" in driver.page_source

            driver.find_element_by_css_selector("body > div:nth-child(3) > div.jumbotron > div > div > div.col-lg-7.col-xl-8 > h1 > span > a").click()
            assert "Headline:" in driver.page_source
            '''

            tests_successful = True

        except (AssertionError) as e:
            print(e)
        finally:    # Teardown
            if not tests_successful:
                requests.put('https://' + BROWSERSTACK_USERNAME + ':' + BROWSERSTACK_ACCESS_KEY + '@api.browserstack.com/automate/sessions/'
                         + driver.session_id + '.json', data={"status": "failed", "reason": "did not pass an assertion test"})

            driver.quit()
            q.task_done()


for i in range(num_threads):
    worker = Thread(target=run_test, args=(q,))
    worker.setDaemon(True)
    worker.start()

q.join()
