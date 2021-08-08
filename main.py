from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import numpy as np


# list__airports-scrollable-container large-height   -> value 0 click
# fsw-airport-item

driver = webdriver.Chrome()
# maybe useful
# https://www.ryanair.com/gb/en/cheap-flights/?from=TLV&out-from-date=2021-05-01&out-to-date=2022-05-01&budget=150
driver.get("https://www.ryanair.com/gb/en/cheap-flights")

webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
driver.find_element_by_class_name("cookie-popup-with-overlay__button").click()
#ActionChains(driver).click(elm).perform()

time.sleep(5)
# click on label-departure-input
dep = driver.find_element_by_id("label-departure-input")
dep.click()

#dep_lst = driver.find_element_by_class_name("core-list")
core = driver.find_elements_by_tag_name("input") # ("core-list-item-title")
#print(dep_lst)
#core = dep_lst.find_elements_by_class_name("core-list-item-title") # ("core-list-item")
print(core)
print("hello")
print(len(core))
departure = core[1]
for i in range(10):
    departure.send_keys(Keys.BACK_SPACE, Keys.BACK_SPACE, Keys.BACK_SPACE, Keys.BACK_SPACE, Keys.BACK_SPACE, Keys.BACK_SPACE, Keys.BACK_SPACE);
departure.send_keys("Tel Aviv")
core[4].click()
# for i in core:
#     print(i.text)
#     print(i.get_attribute('value'))
#     if "Tel Aviv" in i.text:
#         print("----------------------Tel Aviv-------------------------")
# #        i.click()


#submit = driver.find_elements_by_class_name("core-btn-primary-i")
time.sleep(5)
submit = driver.find_elements_by_tag_name("button")
print(len(submit))
submit[0].click()

time.sleep(5)

mylist = driver.find_elements_by_class_name("ff-list-item") # ("farefinder-list") #ff-list-item
print(len(mylist))
for i in mylist:
    print(i.text)
    i.click()
    break


time.sleep(5)
month = driver.find_elements_by_class_name("month")
print(len(month))

# switch to monthly table
month_form = driver.find_element_by_xpath("//span[@translate='foh.farefinder.view_types.month']")
month_form.click()

time.sleep(3)

# set month
months = ["Jun", "Jul", "Aug", "Sep", "Oct"]
a = driver.find_elements_by_class_name("slide") # viewport
for i in a:
    print(i.text.split('\n'))  # first object-> year, second object -> month
    #break

# TODO
#  Add return flight

# get the month object
month_table = driver.find_element_by_class_name("monthly")

month_prices = [i for i in range(31)]
prices = month_table.text.split("\n")
prices = [i for i in prices if i != 'Lowest Fare']

days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
new_prices = []
for i in range(prices.__len__() - 1):
    if prices[i] in days:
        new_prices.append(prices[i])
    elif prices[i].isnumeric() and prices[i+1] not in days and not prices[i+1].isnumeric() and not prices[i+1].split()[0].isnumeric():
        new_prices.append([prices[i],prices[i+1]])
    elif prices[i].isnumeric() and prices[i + 1] not in days and prices[i + 1].isnumeric():
        new_prices.append([prices[i], "0"])
    elif prices[i].isnumeric() and prices[i + 1] in days:
        new_prices.append([prices[i], "0"])
    elif prices[i].split()[0].isnumeric() and len(prices[i].split()) > 1 and not prices[i+1].isnumeric() and prices[i + 1] not in days:
        new_prices.append([prices[i], prices[i + 1]])
    elif prices[i].split()[0].isnumeric() and prices[i + 1] in days:
        new_prices.append([prices[i], "0"])
    elif prices[i].split()[0].isnumeric() and prices[i + 1].isnumeric():
        new_prices.append([prices[i], "0"])
    elif prices[i].isnumeric() and prices[i+1].split()[0].isnumeric():
        new_prices.append([prices[i], "0"])

if prices[-1].isnumeric() or prices[-1].split()[0].isnumeric():
    new_prices.append([prices[-1], "0"])


prices_table = np.reshape(new_prices, (7, -1)).T


month_list = {}
curr_day = 1
for i in range(prices_table.shape[0]):
    for j in range(prices_table.shape[1]):
        if prices_table[i][j][0].split()[0] == str(curr_day):
            month_list[str(curr_day)] = prices_table[i][j][1]
            curr_day += 1




print('-'*30)
print(prices_table)

print('-'*30)


sun, mon, tue, wed, thu, fri, sat = ([] for _ in range(7))
curr_month = ""

for index, i in enumerate(prices, 1):
    # ignore lowest fare
    if i == 'Lowest Fare':
        pass

    if i == 'Mon' or curr_month == 'Mon':
        curr_month = 'Mon'
    elif i == 'Tue' or curr_month == 'Tue':
        curr_month = 'Tue'
    elif i == 'Wed' or curr_month == 'Wed':
        curr_month = 'Wed'
    elif i == 'Thu' or curr_month == 'Thu':
        curr_month = 'Thu'
    elif i == 'Fri' or curr_month == 'Fri':
        curr_month = 'Fri'
    elif i == 'Sat' or curr_month == 'Sat':
        curr_month = 'Sat'
    elif i == 'Sun' or curr_month == 'Sun':
        curr_month = 'Sun'




print("------------month--------------------")
for i in month:
    print(i.text)
    time.sleep(5)
    i.click()



# ng-transclude

time.sleep(135)
driver.close()





'''
driver.get("https://www.ryanair.com")
webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
driver.find_element_by_class_name("cookie-popup-with-overlay__button").click()
#ActionChains(driver).click(elm).perform()
# cookie-popup-with-overlay__button

print(driver.title)

# list__airports-scrollable-container large-height   -> value 0 click
# fsw-airport-item

dep = driver.find_element_by_id("input-button__departure")
dep.clear()
dep.send_keys(Keys.BACK_SPACE, Keys.BACK_SPACE, Keys.BACK_SPACE, Keys.BACK_SPACE, Keys.BACK_SPACE, Keys.BACK_SPACE, Keys.BACK_SPACE);
dep.send_keys("Tel Aviv")  # _hjRemoteVarsFrame
driver.execute_script("arguments[0].value = 'Tel Aviv';", dep)
#a = driver.find_elements_by_xpath("//*[@class='list__airports-scrollable-container' or @class='large-height']") #[0].click()
print("hello")
#driver.find_element_by_class_name('list__airports-scrollable-container large-height').find_elements_by_tag_name(
#    'fsw-airport-item').click()

#webdriver.ActionChains(driver).send_keys(Keys.TAB).perform()
#webdriver.ActionChains(driver).send_keys(Keys.ENTER).perform()

dest = driver.find_element_by_id("input-button__destination")
#dest.click()
dest.clear()
dest.send_keys("Athens")
driver.execute_script("arguments[0].value = 'Athens';", dest)
print("boom")
#webdriver.ActionChains(driver).send_keys(Keys.TAB).perform()
#dep.click()
#webdriver.ActionChains(driver).send_keys(Keys.ENTER).perform()
#dep.clear()
#dep.send_keys("Tel Aviv")
#dep.clear()
#dep.send_keys("Tel Aviv")

# input-button__departure
# input-button__destination

time.sleep(135)
driver.close()
'''