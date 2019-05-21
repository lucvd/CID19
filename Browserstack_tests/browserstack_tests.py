from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from queue import  Queue
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
        try:
            # Setup
            environment = q.get()
            print("%s: Starting" % environment["browser"])
            for key in CONFIG["capabilities"]:
                if key not in environment:
                    environment[key] = CONFIG["capabilities"][key]
            driver = webdriver.Remote(desired_capabilities=environment,
                                      command_executor="http://%s:%s@%s/wd/hub" % (BROWSERSTACK_USERNAME, BROWSERSTACK_ACCESS_KEY, CONFIG['server']))

            #Start actually testing the code
            driver.get("http://connectid.pythonanywhere.com/")
            assert "Connect-ID" in driver.title
            driver.find_element_by_xpath \
                ("//*[@id=\"page-top\"]/header/div/div/a").click()
            driver.find_element_by_id("username").send_keys("jeroen.jerry@hotmail.com")
            elem = driver.find_element_by_id("password")
            elem.send_keys("linkedintest!")
            elem.submit()
            assert "No results found." not in driver.page_source
        except AssertionError as e:
            requests.put('https://' + BROWSERSTACK_USERNAME + ':' + BROWSERSTACK_ACCESS_KEY + '@api.browserstack.com/automate/sessions/'
                         + driver.session_id + '.json', data={"status": "failed", "reason": "didn't pass assertion test"})
        finally:    # Teardown
            driver.quit()
            q.task_done()


for i in range(num_threads):
    worker = Thread(target=run_test, args=(q,))
    worker.setDaemon(True)
    worker.start()

q.join()
