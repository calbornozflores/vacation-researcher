from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import time
import datetime
import progressbar
import logging
import csv
from tools.io import get_dates, get_place, get_element
from config.xpaths import loginButtom, loginUser, loginPass, sendCredentials, headerHotelButtom, \
                         cityInput, displayedOption, searchButtom, arrivalDate, departureDate, \
                         global_ids, resortURLXPATH, resortNumber, resortIdPrefix, resortNameXPATH, \
                         resortStarsXPATH, resortDistanceXPATH, resortPublicPriceXPATH, \
                         resortFinalPriceXPATH, resortPriceByNightXPATH, resortDiscountXPATH, \
                         availablePagesBar, availablePagesBarButtom


def run(WEBPAGE, USER, PWD):
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
    logging.info("Opening Output File ...")
    file = open('outputs/research.csv', 'a+', newline ='')
    extracted_attr = ["placeName", "pageNumber", "resortName", "resortStars", "resortDistance",
                      "resortPublicPrice", "resortFinalPrice", "resortPriceByNight",
                      "resortDiscount", "arrivalDate", "departureDate", "resortURL"]
    write = csv.writer(file)
    write.writerow(extracted_attr)

    logging.info("Opening Chrome Windows ...")
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.maximize_window()
    logging.info("Entering URL ...")
    driver.get(WEBPAGE)
    # Landing Page
    logging.info("Clicking login buttom ...")
    driver.find_element(By.XPATH, loginButtom).click()
    logging.info("Filling out user ...")
    driver.find_element(By.XPATH, loginUser).send_keys(USER)
    logging.info("Filling out password ...")
    driver.find_element(By.XPATH, loginPass).send_keys(PWD)
    logging.info("Sending credentials ...")
    driver.find_element(By.XPATH, sendCredentials).click()
    time.sleep(5)
    # Home Page
    logging.info("Entering Hotel Section ...")
    driver.find_element(By.XPATH, headerHotelButtom).click()
    time.sleep(5)

    logging.info("Receiving Date Range ...")
    arrivalDateStr, departureDateStr = get_dates()
    logging.info("Receiving City to travel ...")
    placeNameStr = get_place()

    # Fill Out Fields
    logging.info("Filling out City to travel ...")
    driver.find_element(By.XPATH, cityInput).send_keys(placeNameStr)
    time.sleep(5)
    driver.find_element(By.XPATH, displayedOption(1)).click()
    logging.info("Filling out Date Range ...")
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

    bar = progressbar.ProgressBar(maxval = totalResortNumber, \
        widgets=[progressbar.Bar(u"█", '[', ']'), ' ', progressbar.Percentage()])
    bar.start()

    resortIdx = 0
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
                resortIdx = resortIdx +1
                bar.update(resortIdx)
        
        write.writerows(resortsInfo_list)
        nextPageNumber = nextPageNumber + 1

        try:
            availablePages = driver.find_element(By.XPATH, availablePagesBar).text.split(" ")
            availablePages = [int(pn) for pn in availablePages]
            pageNameIdx = availablePages.index(nextPageNumber) + 1 # Cause in the webpage the idxs referencing the pages start with 1
            driver.find_element(By.XPATH, availablePagesBarButtom(pageNameIdx)).click()
            goToNextPage = True
            time.sleep(5)
        except:
            goToNextPage = False
    bar.finish()
    file.close()
    driver.close()

