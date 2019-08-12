import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import datetime


email = "414052254@qq.com"
pass_code = "zhaohaiyu"
title = "New Title"
content = "New content"

#options = webdriver.ChromeOptions()
#options.add_argument("user-data-dir=/Users/james/Library/Application Support/Google/Chrome")
print ('Start time,',time.time_ns())
driver = webdriver.Chrome('/Users/james/PycharmProjects/update_blog/chromedriver') # use chromedriver as driver to open browser.
before = time.time_ns()
print ("Before open website", before)
driver.get('http://localhost:8000/wp-admin')  # go to the website.

elem = driver.find_element_by_id("user_login")  # find the element to put login.
elem.send_keys(email)  # send the login information.
elem = driver.find_element_by_id("user_pass")
elem.send_keys(pass_code)
elem.send_keys(Keys.RETURN)  # send the Enter command.
print("After open website and login", time.time_ns())

elem = driver.find_element_by_id("wp-admin-bar-site-name")  # Find the topleft corner to view the website.
elem.click()
print("After clicking the top-left coner",time.time_ns())
elem = driver.find_element_by_class_name("post-edit-link")  # Find the edit link.
elem.click()
print("After finding the edit link and click", time.time_ns())

elem = driver.find_element_by_class_name("edit-post-more-menu")  # Find the menu to change the visual mode to code mode,
# so we can find the "post-content-0" to edit content.
elem.click()
print("After finding the the menu and click",time.time_ns())
#elem =driver.find_element_by_class_name("components-button components-menu-item__button")
#elem.click()
elem =driver.find_element_by_css_selector(".components-menu-group:nth-child(2) .components-button:nth-child(2)")  # Found the element through the Seleium IDE. Could not find it
# in the inspect of the website.
elem.click()
print("After finding the Code-editor and click", time.time_ns())

elem =driver.find_element_by_id("post-content-0")
elem.send_keys(content)
print("After the element is found and put the new content.", time.time_ns())

elem =driver.find_element_by_css_selector(".editor-post-publish-button")
elem.click()
print("After finding the update button and update", time.time_ns())


#button_new = driver.find_element_by_id("wp-admin-bar-new-content")
#button_new.click()

#elem =driver.find_element_by_id("post-title-0")
#elem.send_keys(title)

#elem=driver.find_element_by_id("mce_0")
#elem.send_keys(content)






#driver.set_window_position(0, 0)
#driver.set_window_position(1200, 933)

#button_new = driver.find_element_by_css_selector('css=#post-21 .post-edit-link')
#button_new.click()

#time.sleep(5) # Let the user actually see something!

#driver.quit()