from selenium import webdriver
from selenium.webdriver.common.by import By


def get_keys():
    """
    projectRoot/API_KEY.txt inline structure:
    www.webpage.com username password
    """
    WEBPAGE, USER, PWD = open("API_KEY.txt").readline().split(" ")
    return WEBPAGE, USER, PWD


def get_dates():
    arrivalDate = input("Insert Arrival Date [DD/MM/YYYY]: ")
    departureDate = input("Insert Departure Date [DD/MM/YYYY]: ")
    return arrivalDate, departureDate


def get_place():
    placeNameStr = input("Insert Place Name [City, Country]: ")
    return placeNameStr


def get_element(driver, XPATH):
    try:
        element = driver.find_element(By.XPATH, XPATH).text
    except:
        element = ""
    return element