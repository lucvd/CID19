from selenium import webdriver
import os, sys, json

json_name = sys.argv[1]

with open(json_name, "r") as f:
    obj = json.loads(f.read())

instance_caps= obj[int(sys.argv[2])]
print ("Test "+sys.argv[2]+" started")

#------------------------------------------------------#
# Mention any other capabilities required in the test
caps = {}
caps["browserstack.debug"] = "true"
caps["build"] = "parallel tests"

#------------------------------------------------------#

caps = dict(caps.items() + instance_caps.items())

#------------------------------------------------------#
# THE TEST TO BE RUN PARALLELY GOES HERE

driver = webdriver.Remote(
    command_executor='https://%s:%s@hub.browserstack.com/wd/hub' % (
        "jeroenveltmans1", "BwHWqoz9bA29UXwuBGmT"
    ),
    desired_capabilities=caps)

driver.get("http://www.google.com")
inputElement = driver.find_element_by_name("q")
inputElement.send_keys("browserstack")
inputElement.submit()
print (driver.title)
driver.quit()
#------------------------------------------------------#