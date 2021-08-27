from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import numpy as np
import copy

class RyanairAPI:
    def __init__(self, site_url="https://www.ryanair.com/gb/en/cheap-flights", departure_city="Tel Aviv"):
        self.url = site_url
        # self.driver = driver
        self.source_country = "Israel"
        self.departure_city = departure_city
        self.driver = ""
        self.temp_driver = ""
        self.dest_temp_driver = ""
        self.months_temp_driver = ""
        self.months_url = ""
        self.dests_url = ""
        self.curr_month = ""
        self.curr_dest_city = ""
        self.curr_dest_country = ""
        self.curr_year = ""
        self.city_count = 0
        self.year = {"Jun": [], "Jul": [], "Aug": [], "Sep": [], "Oct": []}

    def gather_data_one_page(self):
        pass

    def gather_data(self):
        self.open_fare_finder()
        # TODO choose city   get_all_dests()?
        # self.get_all_dests()
        # month_table = self.get_month_object()
        # # self.set_month()
        # prices_table = self.get_month_prices(month_table)
        # month_list = self.convert_prices_tables_to_list(prices_table)
        # print(month_list)
        all_destinations = self.get_all_dests()
        city_dests = [dest.text.split()[0] for dest in all_destinations]
        print(city_dests)
        for city in city_dests:
            print(f"------------------------------{city}---------------------------------------------------------")
            self.driver.get(self.dests_url)  #########################################
            # time.sleep(5)
            # self.driver = self.dest_temp_driver
            # self.driver = copy.deepcopy(self.dest_temp_driver)
            for dest in self.get_all_dests():
                if city == dest.text.split()[0]:
                    print(f"#######################################{city}####################################################")
                    # self.curr_dest_city = dest.text.split()[0]
                    # self.curr_dest_country = dest.text.split()[1]
                    if len(dest.text.split()) == 8:
                        self.curr_dest_city = dest.text.split()[0]  # ???????????????????????
                        self.curr_dest_country = dest.text.split()[1]
                    elif "/" in dest.text.split():
                        self.curr_dest_city = "".join(dest.text.split()[:3])  # ???????????????????????
                        self.curr_dest_country = dest.text.split()[3]
                    else:
                        self.curr_dest_city = " ".join(dest.text.split()[:2])  # ???????????????????????
                        self.curr_dest_country = dest.text.split()[2]

                    dest.click()

                    _ = self.get_month_object()
                    months = self.set_month()
                    # self.driver = self.months_temp_driver
                    for month in months:
                        if month.text.__len__() == 0:
                            continue
                        time.sleep(1.5)
                        if self.city_count <= 4:
                            month.click()
                            self.city_count += 1
                        self.curr_year = month.text.split()[0]
                        self.curr_month = month.text.split()[1]

                        month_table = self.get_month_object()
                        prices_table = self.get_month_prices(month_table)
                        month_list = self.convert_prices_tables_to_list(prices_table)
                        print(month_list)
                        self.save_month(month_list)

                    break

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
                                Keys.BACK_SPACE, Keys.BACK_SPACE)
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

        return month_table

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
        # self.dest_temp_driver = self.driver
        self.dests_url = self.driver.current_url
        # self.dest_temp_driver = copy.deepcopy(self.driver)
        return all_dests
        # for i in all_dests:
        #     print(i.text)
        #     self.curr_dest_city = i.text.split()[0]
        #     self.curr_dest_country = i.text.split()[1]
        #     self.driver = temp_driver
        #     i.click()
        #     # break # stop at first city
        #     monthly_prices_table = self.get_month_prices(self.get_month_object())
        #     break  # stop at first city

    def set_month(self):
        months = self.driver.find_elements_by_class_name("slide")
        self.months_url = self.driver.current_url
        # self.months_temp_driver = self.driver
        # self.months_temp_driver = copy.deepcopy(self.driver)
        return months
        # for i in months:
        #     i.click()
        #     self.curr_year = i.text.split()[0]
        #     self.curr_month = i.text.split()[1]

    def save_month(self, month_list):
        with open("data\\flights.txt", "a") as f:
            for day in month_list.keys():
                if month_list[day] != "0":
                    f.write(f"{day},{self.curr_month},{self.curr_year},{self.departure_city},{self.source_country},"
                            f"{self.curr_dest_city},{self.curr_dest_country},{month_list[day]},Ryanair,\n")

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

