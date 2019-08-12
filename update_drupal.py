from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import datetime

driver = webdriver.Chrome('/Users/james/PycharmProjects/update_blog/chromedriver') # use chromedriver as driver to open browser.
before = datetime.datetime.now()
print ("before open website", before)
driver.get("http://localhost:8081/user/login")  # go to the website.


user = "jameszhao"
pass_code = "zhaohaiyu"
title = "New Title"
content = "New content"

elem = driver.find_element_by_id("edit-name")  # find the element to put login.
elem.send_keys(user)  # send the login information.
elem = driver.find_element_by_id("edit-pass")
elem.send_keys(pass_code)
elem.send_keys(Keys.RETURN)  # send the Enter command.
after = datetime.datetime.now()
print ("after open website and login", after)

elem = driver.find_element_by_link_text("Home") # find the home page
elem.click()

elem =driver.find_element_by_css_selector(".field--name-title")
elem.click()

elem = driver.find_element_by_link_text("Edit")  # Find the edit button.
elem.click()

elem = driver.find_element_by_xpath("//html/body")
elem.click()

driver.switch_to.frame(0)  #switch to frame0 which has html for the new post.

elem = driver.find_element_by_xpath("//html/body")  # find the element again.
print ("after the element is found to put new update.", datetime.datetime.now())
elem.send_keys(content)

driver.switch_to.default_content() # swtich back to the page.

elem =driver.find_element_by_id("edit-submit")

print ("before clicking update.",datetime.datetime.now())
elem.click()
print ("After click update", datetime.datetime.now())