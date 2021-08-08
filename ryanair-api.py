from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import numpy as np

class RyanairAPI():
    def __init__(self, site_url = "https://www.ryanair.com/gb/en/cheap-flights", departure_city = "Tel Aviv"):
        self.url = site_url
        # self.driver = driver
        self.departure_city = departure_city
        self.driver
        self.temp_driver
        self.city_count = 0
        self.year = {"Jun": [], "Jul": [], "Aug": [], "Sep": [], "Oct": []}

    def open_fare_finder(self):
        self.driver = webdriver.Chrome()
        self.driver.get(self.url)
        webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
        self.driver.find_element_by_class_name("cookie-popup-with-overlay__button").click()
        time.sleep(5)
        # click on label-departure-input
        self.driver.find_element_by_id("label-departure-input").click()
        core = self.driver.find_elements_by_tag_name("input")  # ("core-list-item-title")
        departure = core[1]
        for i in range(10):
            departure.send_keys(Keys.BACK_SPACE, Keys.BACK_SPACE, Keys.BACK_SPACE, Keys.BACK_SPACE, Keys.BACK_SPACE,
                                Keys.BACK_SPACE, Keys.BACK_SPACE);
        departure.send_keys(self.departure_city)
        core[4].click()
        time.sleep(5)
        submit = self.driver.find_elements_by_tag_name("button")
        submit[0].click()
        time.sleep(5)

    def get_month_object(self):
        time.sleep(5)
        month = self.driver.find_elements_by_class_name("month")
        print(len(month))

        # switch to monthly table
        month_form = self.driver.find_element_by_xpath("//span[@translate='foh.farefinder.view_types.month']")
        month_form.click()

        time.sleep(3)
        # get the month object
        month_table = self.driver.find_element_by_class_name("monthly")

        return  month_table


    def convert_prices_tables_to_list(self, prices_table):
        month_list = {}
        curr_day = 1
        for i in range(prices_table.shape[0]):
            for j in range(prices_table.shape[1]):
                if prices_table[i][j][0].split()[0] == str(curr_day):
                    month_list[str(curr_day)] = prices_table[i][j][1]
                    curr_day += 1

        return month_list


    def get_all_dests(self):
        all_dests = self.driver.find_elements_by_class_name("ff-list-item")  # ("farefinder-list") #ff-list-item
        temp_driver = self.driver
        for i in all_dests:
            print(i.text)
            self.driver = temp_driver
            i.click()
            # break # stop at first city

            monthly_prices_table = self.get_month_prices(self.get_month_object())
            break  # stop at first city

    def set_month(self):
        pass

    # def get_month_object(self):
    #     time.sleep(5)
    #     month = self.driver.find_elements_by_class_name("month")
    #     print(len(month))
    #
    #     # switch to monthly table
    #     month_form = self.driver.find_element_by_xpath("//span[@translate='foh.farefinder.view_types.month']")
    #     month_form.click()
    #
    #     time.sleep(3)
    #     # get the month object
    #     month_table = self.driver.find_element_by_class_name("monthly")
    #
    #     return  month_table

    def get_all_prices(self):
        pass

    def save_prices(self):
        pass


    def get_month_prices(self, month_table):
        month_prices = [i for i in range(31)]
        prices = month_table.text.split("\n")
        prices = [i for i in prices if i != 'Lowest Fare']

        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        new_prices = []
        for i in range(prices.__len__() - 1):
            if prices[i] in days:
                new_prices.append(prices[i])
            elif prices[i].isnumeric() and prices[i + 1] not in days and not prices[i + 1].isnumeric() and not \
            prices[i + 1].split()[0].isnumeric():
                new_prices.append([prices[i], prices[i + 1]])
            elif prices[i].isnumeric() and prices[i + 1] not in days and prices[i + 1].isnumeric():
                new_prices.append([prices[i], "0"])
            elif prices[i].isnumeric() and prices[i + 1] in days:
                new_prices.append([prices[i], "0"])
            elif prices[i].split()[0].isnumeric() and len(prices[i].split()) > 1 and not prices[i + 1].isnumeric() and \
                    prices[i + 1] not in days:
                new_prices.append([prices[i], prices[i + 1]])
            elif prices[i].split()[0].isnumeric() and prices[i + 1] in days:
                new_prices.append([prices[i], "0"])
            elif prices[i].split()[0].isnumeric() and prices[i + 1].isnumeric():
                new_prices.append([prices[i], "0"])
            elif prices[i].isnumeric() and prices[i + 1].split()[0].isnumeric():
                new_prices.append([prices[i], "0"])

        if prices[-1].isnumeric() or prices[-1].split()[0].isnumeric():
            new_prices.append([prices[-1], "0"])

        prices_table = np.reshape(new_prices, (7, -1)).T

        return prices_table

