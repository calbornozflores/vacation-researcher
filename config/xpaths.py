loginButtom = '//*[@id="home"]/div[1]/div/div/div/div/div[1]/div/div[1]/div[2]/button'
loginUser = '//*[@id="LoginBlock_UserName"]'
loginPass = '//*[@id="Password"]'
sendCredentials = '//*[@id="form0"]/button'
headerHotelButtom = '//*[@id="navbar"]/ul/li[2]/a'
cityInput = '//*[@id="ctl00_ctl00_ctl00_ContentPlaceHolderMain_ContentPlaceHolderMain_ContentPlaceHolderMain_RentalsSearchControl_txtGeolocation"]'
displayedOption = lambda idx: f'//*[@id="ctl00_ctl00_ctl00_ContentPlaceHolderMain_ContentPlaceHolderMain_ContentPlaceHolderMain_RentalsSearchControl_pnlGeolocation"]/span[1]/div/ul/li[{idx}]'
searchButtom = '//*[@id="ctl00_ctl00_ctl00_ContentPlaceHolderMain_ContentPlaceHolderMain_ContentPlaceHolderMain_RentalsSearchControl_btnSearch"]'

arrivalDate = '//*[@id="txtArrivalDate"]'
departureDate = '//*[@id="txtDepartureDate"]'

global_ids = '//*[@id]'
resortNumber = '//*[@id="rentalResultsCount"]'

resortIdPrefix = "rentalsResultsResortName"

resortURLXPATH = lambda resortId: f'//*[@href="{resortIdPrefix}{resortId}"]'
resortNameXPATH = lambda resortId: f'//*[@id="{resortIdPrefix}{resortId}"]/div/div[1]'
resortStarsXPATH = lambda resortId: f'//*[@id="{resortIdPrefix}{resortId}"]/div/div[6]'
resortDistanceXPATH = lambda resortId: f'//*[@id="{resortIdPrefix}{resortId}"]/div/div[4]'
resortPublicPriceXPATH = lambda resortId: f'//*[@id="RentalsResultsItemContainer{resortId}"]/div[1]/div[3]/div[1]/div[1]/span[2]'
resortFinalPriceXPATH = lambda resortId: f'//*[@id="RentalsResultsItemContainer{resortId}"]/div[1]/div[3]/div[1]/div[3]/span'
resortPriceByNightXPATH = lambda resortId: f'//*[@id="RentalsResultsItemContainer{resortId}"]/div[1]/div[3]/div[1]/div[3]/div/span'
resortDiscountXPATH = lambda resortId: f'//*[@id="{resortIdPrefix}{resortId}"]/div/div[7]/div/span'

availablePagesBar = '//*[@id="rentalsResultsPager"]'
availablePagesBarButtom = lambda pageNameIdx: f'{availablePagesBar}/a[{pageNameIdx}]'