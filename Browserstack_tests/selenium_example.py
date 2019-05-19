from selenium import webdriver

driver = webdriver.Chrome('D:\\Programs\\chromedriver.exe')
driver.get("http://connectid.pythonanywhere.com/")
assert "Connect-ID" in driver.title
driver.find_element_by_xpath\
    ("//*[@id=\"page-top\"]/header/div/div/a").click()
driver.find_element_by_id("username").send_keys("jeroen.jerry@hotmail.com")
elem = driver.find_element_by_id("password")
elem.send_keys("linkedintest!")
elem.submit()
assert "No results found." not in driver.page_source
driver.close()