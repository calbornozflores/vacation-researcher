from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
from pathlib import Path
import datetime
import progressbar
import logging
import csv
from tools.io import get_dates, get_place, get_element
from tools.xpaths import loginButtom, loginUser, loginPass, sendCredentials, headerHotelButtom, \
                         cityInput, displayedOption, searchButtom, arrivalDate, departureDate, \
                         global_ids, resortURLXPATH, resortNumber, resortIdPrefix, resortNameXPATH, \
                         resortStarsXPATH, resortDistanceXPATH, resortPublicPriceXPATH, \
                         resortFinalPriceXPATH, resortPriceByNightXPATH, resortDiscountXPATH, \
                         availablePagesBar, availablePagesBarButtom


def run(WEBPAGE, USER, PWD):
    file = open('outputs/research.csv', 'a+', newline ='')
    extracted_attr = ["placeName", "pageNumber", "resortName", "resortStars", "resortDistance",
                      "resortPublicPrice", "resortFinalPrice", "resortPriceByNight",
                      "resortDiscount", "arrivalDate", "departureDate", "resortURL"]
    write = csv.writer(file)
    write.writerow(extracted_attr)

    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.maximize_window()
    driver.get(WEBPAGE)
    # Landing Page
    driver.find_element(By.XPATH, loginButtom).click()
    driver.find_element(By.XPATH, loginUser).send_keys(USER)
    driver.find_element(By.XPATH, loginPass).send_keys(PWD)
    driver.find_element(By.XPATH, sendCredentials).click()
    time.sleep(5)
    # Home Page
    driver.find_element(By.XPATH, headerHotelButtom).click()
    time.sleep(5)

    arrivalDateStr, departureDateStr = get_dates()
    placeNameStr = get_place()

    # Fill Out Fields
    driver.find_element(By.XPATH, cityInput).send_keys(placeNameStr)
    time.sleep(5)
    driver.find_element(By.XPATH, displayedOption(1)).click()
    driver.find_element(By.XPATH, arrivalDate).click()
    time.sleep(1)
    driver.find_element(By.XPATH, arrivalDate).clear()
    time.sleep(1)
    driver.find_element(By.XPATH, arrivalDate).send_keys(arrivalDateStr)
    driver.find_element(By.XPATH, arrivalDate).send_keys(Keys.ENTER)
    driver.find_element(By.XPATH, departureDate).send_keys(departureDateStr)
    driver.find_element(By.XPATH, searchButtom).click()

    time.sleep(20)
    goToNextPage = True

    totalResortNumber = int(driver.find_element(By.XPATH, resortNumber).text)

    nextPageNumber = 1
    while goToNextPage:
        resortsInfo_list = []
        webpage_ids = driver.find_elements(By.XPATH, global_ids)
        for wid in webpage_ids:
            att_id = wid.get_attribute('id')
            if resortIdPrefix in att_id:
                resortId = att_id.split("Name")[1] # Eg. rentalsResultsResortName592407
                resortName = get_element(driver, resortNameXPATH(resortId))
                resortStars = get_element(driver, resortStarsXPATH(resortId))
                resortDistance = get_element(driver, resortDistanceXPATH(resortId))
                resortPublicPrice = get_element(driver, resortPublicPriceXPATH(resortId))
                resortFinalPrice = get_element(driver, resortFinalPriceXPATH(resortId))
                resortPriceByNight = get_element(driver, resortPriceByNightXPATH(resortId))
                resortDiscount = get_element(driver, resortDiscountXPATH(resortId))

                resortsInfo_list.append(
                    [
                        placeNameStr,
                        nextPageNumber,
                        resortName,
                        resortStars,
                        resortDistance,
                        resortPublicPrice,
                        resortFinalPrice,
                        resortPriceByNight,
                        resortDiscount,
                        arrivalDateStr,
                        departureDateStr
                    ]
                )
        
        write.writerows(resortsInfo_list)
        availablePages = driver.find_element(By.XPATH, availablePagesBar).text.split(" ")
        availablePages = [int(pn) for pn in availablePages]
        nextPageNumber = nextPageNumber + 1

        try:
            pageNameIdx = availablePages.index(nextPageNumber) + 1 # Cause in the webpage the idxs referencing the pages start with 1
            print(availablePages, f"Select: {nextPageNumber} [{pageNameIdx}] / {totalResortNumber}")
            driver.find_element(By.XPATH, availablePagesBarButtom(pageNameIdx)).click()
            goToNextPage = True
            time.sleep(5)
        except:
            goToNextPage = False
    file.close()
    driver.close()

