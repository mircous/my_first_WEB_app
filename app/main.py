from flask import Flask
from flask import redirect
from flask import url_for
from flask import request
from flask import render_template
from flask import session
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
import sqlite3
import os, sys

app = Flask(__name__)


app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


lst2 = []
phone_number = 577371155
#name = 'Giorgi'
usernameStr = 'Primesellersglobal@gmail.com'
passwordStr = 'Pride123'

#usernameStr = 'giorgi.g@list.ru'
#passwordStr = '.6LzTtVri3!WNQ8'

#WEBSITE_URL = 'https://www.myhome.ge/ka/pr/11870912/1817709/qiravdeba-axali-ashenebuli-bina-krwanisshi-krwanisi-3-oTaxiani'

def get_content():
    connection = sqlite3.connect(str(os.getcwd()) + "/phonebook.db")
    cursor = connection.cursor()
    query1 = "SELECT * from Phonebookk"
    result = cursor.execute(query1)
    result = result.fetchall()
    """returns content from certain page"""
    WEBSITE_URL = result[0][0]
    response = requests.get(WEBSITE_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def find_pictures_hrefs(content):
    gird = content.select('div.swiper-wrapper')[0].contents
    lst=[]
    for x in gird:
        try:
            y = x.contents[0].contents[0].attrs['data-src']
            lst.append(y)
        except:
            pass
    return lst

#!!!!!!!@@@@@@@@  NEED TO CHANGE FOTOS VAR @@@@@@@@@@@@@@@@@!!!!!!!!!!!!!!!
def string():

    photos = str(os.getcwd()) + '/'
    fotos = "image.jpg"
    setring = ''
    seet = ''
    photo_mount = len(find_pictures_hrefs(get_content()))
    for x in range(photo_mount):
        try:
            if x>0:
                setring = (photos+str(x)+fotos+'\n')
            else:
                setring = (photos+str(x)+fotos)
            setring += seet
            seet = setring
        except:
            pass
    return setring


def save_pictures():
    y=0
    for z in find_pictures_hrefs(get_content()):
        img_data = requests.get(z).content
        with open(str(y)+'image.jpg', 'wb') as handler:
            handler.write(img_data)
        y += 1
    return "pictures are saved"


def get_needed_info():
    save_pictures()
    content = get_content()
    #"""returns needed info from certain page"""
    addresss = content.select('div.statement-title > span.address')[0].text
    address = addresss[7:-6].split('თბილისი')[0][0:-2]
    details = content.select('div.main-features.row.no-gutters > div.col-6.col-lg-4.mb-0.mb-md-4.mb-lg-0.d-flex.align-items-center.mb-lg-0.mb-4.pr-2.pr-lg-0')
    #''' binis farti'''
    needed_details = int(details[0].contents[1].contents[0].text.split('.')[0])
    #'''otaxebis raodenoba'''
    otaxi = int(details[0].contents[1].contents[1].text.split(' ')[0])
    #'''sartulebis raodenoba da chveni sartuli'''
    sartulebi = details[2].contents[1].contents[0].text
    current_floor = int(sartulebi.split('/')[0])
    total_floors = int(sartulebi.split('/')[1])

    #print(address)
    try:
        price = content.select('div.price-toggler-wrapper > div.d-flex.mb-2.align-items-center.justify-content-between')[0].contents[0].text.strip()
        try:
            frice = int(price.split(',')[0]+price.split(',')[1])
        except:
            try:
                frice = int(price)
            except:
                logging.info('2 much big %s', price)
    except ValueError:
        logging.info('Invalid path to %s', price)
    buxari = content.select('div.amenities > div.row > div.col-6')[1]
    classname = str(buxari.contents[1].contents[3])
    clearclassname = classname.split('class')[2].split('>')[0].split('"')[1]
    #'''კომენტარი'''
    try:
        comment = content.select('div.description > div > div.shortened > p.pr-comment.translated')[0].text
    except:
        comment = ' '
#    '''sivrce'''
    sivrce = content.select('div.amenities > div.row > div.col-6')[0].contents[1].contents
    ketilmowyoba = content.select('div.amenities > div.row > div.col-6')[1].contents[1].contents


    #print(ketilmowyoba)
    bathrooms = 0
    bedrooms = 0
    home_high = 2
    LoggiaSize = 0
    BalconySize = 0
    VerandaSize = 0
    StoreType = 0
    Parking = 0
    HotWater = 0
    gatboba = 0
    buxari = 0
    Gas = 0
    ElevatorRegular = 0
    ElevatorBig = 0
    Internet = 0
    Phone = 0
    TV = 0
    Furniture = 0

    try:
        bdroom = content.select('div.main-features > div')[1]
        bdrooms = bdroom.select('div > span.d-block')[0]
        bedrooms = bdrooms.text
        #ipdb.set_trace()
        #bdrm = driver.find_element(By.XPATH, "/html/body/div[7]/div/div[5]/div[4]/div[2]/div/span[1]")
        #print(bdrm)
        #bedrooms = int(sivrce[3].text.split(' ')[1])
    except:
        pass

    mdgomareoba = sivrce[0].text
    try:
        home_high = float(sivrce[2].text.split(' ')[2])
    except:
        pass
    try:
        try:
            bathrooms = int(sivrce[7].text[-41])
        except:
            bathrooms = int(sivrce[7].text[-42])
    except:
    #    '''if not chosen will be empty str'''
        #bathrooms = sivrce[7].text[-46:-40]
        pass
    try:
        LoggiaSize = int(sivrce[6].text.split(' მ')[0].split('\t')[-1])
    except:
        pass
    try:
        BalconySize = int(sivrce[4].text.split(' ')[0].split('\t')[-1])
    except:
        pass
    try:
        VerandaSize = int(sivrce[4].text.split(' ')[0].split('\t')[-1])
    except:
        pass
    try:
        StoreType = sivrce[10].text.split('\t')[-1]
    except:
        pass
    try:
        Parking = sivrce[9].text.split('\t')[-1]
        if Parking == 'პარკინგი':
            Parking = 0
    except:
        pass
    try:
        HotWater = ketilmowyoba[0].text.split('\t')[-1]
    except:
        pass
    try:
        gatboba = sivrce[8].text.split('\t')[-1]
    except:
        pass
    try:
        buxari = ketilmowyoba[3].text
        if buxari == 'ბუხარი':
            buxari = 0
        else:
            buxari = 1
    except:
        pass
    try:
        Gas = ketilmowyoba[1].text
        if Gas == 'ბუნებრივი აირი':
            Gas = 0
        else:
            Gas = 1
    except:
        pass
    try:
        ElevatorRegular = ketilmowyoba[5].text
        if ElevatorRegular == 'სამგზავრო ლიფტი':
            ElevatorRegular = 0
        else:
            ElevatorRegular = 1
    except:
        pass
    try:
        ElevatorBig = ketilmowyoba[6].text
        if ElevatorBig == 'სატვირთო ლიფტი':
            ElevatorBig = 0
        else:
            ElevatorBig = 1
    except:
        pass
    try:
        Internet = ketilmowyoba[2].text
        if Internet == 'ინტერნეტი':
            Internet = 0
        else:
            Internet = 1
    except:
        pass
    try:
        Phone = ketilmowyoba[7].text
        if Phone == 'ტელეფონი':
            Phone = 0
        else:
            Phone = 1
    except:
        pass
    try:
        TV = ketilmowyoba[8].text
        if TV == 'ტელევიზორი':
            TV = 0
        else:
            TV = 1
    except:
        pass
    try:
        conditioner = ketilmowyoba[9].text
        if conditioner == 'კონდიციონერი':
            conditioner = 0
        else:
            conditioner = 1
    except:
        pass
    try:
        Furniture = ketilmowyoba[4].text
        if Furniture == 'ავეჯი':
            Furniture = 0
        else:
            Furniture = 1
    except:
        pass

    current_dict = {
        'comment':comment,
        'Furniture':Furniture,
        'conditioner':conditioner,
        'TV':TV,
        'Phone':Phone,
        'Internet':Internet,
        'ElevatorBig':ElevatorBig,
        'ElevatorRegular':ElevatorRegular,
        'Gas':Gas,
        'buxari':buxari,
        'gatboba':gatboba,
        'HotWater':HotWater,
        'Parking':Parking,
        'StoreType':StoreType,
        'VerandaSize':VerandaSize,
        'BalconySize':BalconySize,
        'LoggiaSize':LoggiaSize,
        'bathroom':bathrooms,
        'bedrooms':bedrooms,
        'address':address,
        'mdgomareoba':mdgomareoba,
        'home_high':home_high,
        'total_price':frice,
        'total_rooms':otaxi,
        'current_floor':current_floor,
        'total_floors':total_floors,
        "apartment_area":needed_details
    }
    #print(current_dict)
    return current_dict


#@app.route('/selenium')
def selenium():
    #name = 'Giorgi'
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    name = session['name']
    dict = get_needed_info()
    driver.maximize_window()
    time.sleep(3)
    browser = driver.get("https://auth.my.ge/ka/?Continue=https%3A%2F%2Fwww.myhome.ge%2Fka%2F")
    time.sleep(2)
    driver.find_element(By.ID, "Email").send_keys(usernameStr)
    driver.find_element(By.ID, "Password").send_keys(passwordStr)
    driver.find_element(By.XPATH, "//button[@class='btn btn-lg btn-full']").click()
    time.sleep(1)
    return driver


@app.route('/refresh')
def refresh():
    connection = sqlite3.connect(str(os.getcwd()) + "/phonebook.db")
    cursor = connection.cursor()
    query1 = "SELECT * from Phonebookk"
    result = cursor.execute(query1)
    result = result.fetchall()
    try:
        #driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        #driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(service=Service(executable_path=os.environ.get("CHROMEDRIVER_PATH")), options=chrome_options)
        time.sleep(2)
        dict = get_needed_info()
        seet = string()
        time.sleep(2)
        name = "Flatz"
        #driver.maximize_window()
        time.sleep(3)
        driver.get("https://auth.my.ge/ka/?Continue=https%3A%2F%2Fwww.myhome.ge%2Fka%2F")
        time.sleep(2)
        driver.find_element(By.ID, "Email").send_keys(usernameStr)
        driver.find_element(By.ID, "Password").send_keys(passwordStr)
        driver.find_element(By.XPATH, "//button[@class='btn btn-lg btn-full']").click()
        time.sleep(3)
        #driver.get("https://www.myhome.ge/ka/my/addProduct")
        time.sleep(3)
        driver.find_element(By.XPATH, "//button[@class='dropdown-toggle cursor-pointer d-flex align-items-center justify-content-between statement_button w-100 h-100']").click()
        time.sleep(3)
        driver.find_element(By.XPATH, "//label[@class='dropdown-item d-flex align-items-center']").click()
        ''' required con. clicks'''
        element = driver.find_element(By.ID, 'StreetAddr')
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
        #accept cockies
        driver.find_element(By.XPATH, '/html/body/div[4]/div/button').click()
        #qiravdeba
        driver.find_element(By.XPATH, "//label[@for='AdTypeID_329']").click()
        #axali ashenebuli
        driver.find_element(By.XPATH, "/html/body/div[3]/div/div/form/div/div[2]/section/div[2]/div[6]/div[2]/div/div[2]").click()
        #driver.find_element(By.ID, "select2-RentMinTerm_1023-container").click()
        '''if 3თვე: -.-/li[2], if 6 : -.-/li[3], if 9 : -.-/li[4],if 12 : -.-/li[5] ,if 15: -.-/li[6]'''
        #driver.find_element(By.XPATH, "/html/body/span/span/span[2]/ul/li[2]").click()
        #driver.find_element(By.XPATH, "//label[@for='RentType_1019']").click()
        '''//label[@for='RentType_1019'] - მთლიანი ბინა
        //label[@for='RentType_1020'] - ბინის ნაწილი
        //label[@for='RentType_1021'] - ბინის ნაწილი მეპატრონესთან ერთად'''
        #SCROLLING
        element = driver.find_element(By.ID, 'StreetAddr')
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
        driver.find_element(By.ID, 'select2-ConditionID_1362-container').click()
        '''if ახალი გარემონტებული : -.-/li[2],  if  მიმდინარე რემონტი : -.-/li[3],
        if თეთრი კარკასი : -.-/li[4]
        if შავი კარკასი : -.-/li[5], if მწვანე კარკასი : -.-/li[6]'''
        driver.find_element(By.XPATH, '/html/body/span/span/span[2]/ul/li[2]').click()
        time.sleep(3)
        driver.find_element(By.ID, 'CeilingHeight_1024').send_keys(dict['home_high'])
        '''შშმპ ადაპტირებული'''
        # if turn this optionon need to change part of code !!!
        #driver.find_element(By.ID, 'SpecialPersons_321').click()
        '''third part'''
        #scroll down
        element = driver.find_element(By.ID, 'CadCode')
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
        time.sleep(1)
        '''mapping'''
        driver.find_element(By.XPATH, "/html/body/div[3]/div/div/form/div/div[2]/section/div[2]/div[21]/div/div/div/div/input").send_keys(dict['address'])
        time.sleep(2)
        driver.find_element(By.XPATH, "/html/body/div[3]/div/div/form/div/div[2]/section/div[2]/div[21]/div/div/div/div[3]/div/div[3]/div/div/ul/li/a/span").click()
        driver.find_element(By.XPATH, "/html/body/div[3]/div/div/form/div/div[2]/section/div[2]/div[21]/div/div/div/div[2]/input").send_keys(dict['address'])
        time.sleep(1)
        element = driver.find_element(By.ID, "select2-ParkingID_375-container")
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
        '''basic settings'''
        driver.find_element(By.XPATH, "/html/body/div[3]/div/div/form/div/div[2]/section[2]/div/div[2]/div/div/div[2]/input").send_keys(dict['apartment_area'])
        driver.find_element(By.XPATH, "/html/body/div[3]/div/div/form/div/div[2]/section[2]/div/div[2]/div/div[2]/div[2]/input").send_keys(dict['total_floors'])
        driver.find_element(By.XPATH, "/html/body/div[3]/div/div/form/div/div[2]/section[2]/div/div[2]/div/div[2]/div[3]/input").send_keys(dict['current_floor'])
        '''if დუპლექსი'''
        #driver.find_element(By.XPATH, "//label[@for='FloorType_1289']").click()
        '''choosing amount of rooms'''
        driver.find_element(By.XPATH, "/html/body/div[3]/div/div/form/div/div[2]/section[2]/div/div[2]/div/div[4]/div[2]/div/span/span/span/span").click()
        '''X = AMOUNT_ROOMS +1    /html/body/span/span/span[2]/ul/li[X] !!!'''
        driver.find_element(By.XPATH, "/html/body/span/span/span[2]/ul/li["+ str(dict['total_rooms']+1) +']').click()
        '''chosing amount of BedRooms'''
        '''X = AMOUNT_of_BEDROOMS + 1    /html/body/span/span/span[2]/ul/li[X] !!!'''
        try:
            driver.find_element(By.ID, 'select2-BedRooms_342-container').click()
            driver.find_element(By.XPATH, '/html/body/span/span/span[2]/ul/li['+ str(dict['bedrooms']+1) + ']').click()
        except:
            pass
        '''chosing amount of bathROOMs'''
        '''X = AMOUNT_of_BATHROOMs + 1  /html/body/span/span/span[2]/ul/li[X] !!!'''
        try:
            driver.find_element(By.ID, 'select2-BathRooms_344-container').click()
            driver.find_element(By.XPATH, '/html/body/span/span/span[2]/ul/li[' + str(dict['bathroom']+1) + ']').click()
        except:
            pass
            ''' მისაღები, ფართი, აირჩიე ! '''
            #driver.find_element(By.ID, 'LivingRoom_3484').click()
            #driver.find_element(By.ID, 'LivingRoomM2_3485').send_keys(LivingRoom)
            #driver.find_element(By.ID, 'select2-LivingRoomType_3486-container').click()
            '''if გამოყოფილი :  -.-/li[2], if სტუდიო : -.-/li[3]'''
            #driver.find_element(By.XPATH, 'html/body/span/span/span[2]/ul/li[2]').click()
            '''ლოჯი, ფართი'''
        if dict['LoggiaSize'] > 0:
            driver.find_element(By.ID, 'LoggiaSize_360').send_keys(dict['LoggiaSize'])
            driver.find_element(By.ID, 'Loggia_347').click()
        else:
            pass
        '''აივიანი, ფართი, აირჩიე'''
        if dict['BalconySize'] > 0:
            driver.find_element(By.ID, 'Balcony_348').click()
            driver.find_element(By.ID, 'BalconySize_361').send_keys(dict['BalconySize'])
            #driver.find_element(By.ID, 'select2-BalconyType_362-container').click()
            '''if ღია : -.-/li[2], if დახურული : -.-/li[3]'''
            #driver.find_element(By.XPATH, 'html/body/span/span/span[2]/ul/li[2]').click()
            '''ვერანდა, ფართი'''
        if dict['VerandaSize'] > 0:
            driver.find_element(By.ID, 'Veranda_349').click()
            driver.find_element(By.ID, 'VerandaSize_365').send_keys(dict['VerandaSize'])
        else:
            pass
        '''სათავსო, ფართი, აირჩიე'''
        if dict['StoreType'] != 'სათავსო':
            driver.find_element(By.ID, 'StoreType_350').click()
            #driver.find_element(By.ID, 'StoreSize_366').send_keys(StoreSize)
            driver.find_element(By.ID, 'select2-StoreTypeID_367-container').click()
            '''სარდაფი, სხვენი, საკუჭნაო, გარე სათავსო, საერთო სათავსო'''
            if dict['StoreType'] == 'სარდაფი':
                x = 1
            elif dict['StoreType'] == 'სხვენი':
                x = 2
            elif dict['StoreType'] == 'საკუჭნაო':
                x = 3
            elif dict['StoreType'] == 'გარე სათავსო':
                x = 4
            else:
                x = 5
            driver.find_element(By.XPATH, 'html/body/span/span/span[2]/ul/li[' + str(x) + ']').click()
        else:
            pass
            '''პარკინგი - აირჩიე'''
        if dict['Parking'] != 0:
            if dict['Parking'] == 'ეზოს პარკინგი':
                x = 1-1
            elif dict['Parking'] == 'ავტოფარეხი':
                x = 2-1
            elif dict['Parking'] == 'პარკინგის ადგილი':
                x = 3-1
            elif dict['Parking'] == 'მიწისქვეშა პარკინგი':
                x = 4-1
            else:
                x = 5-1
            time.sleep(1)
            '''need to scroll'''
            element = driver.find_element(By.ID, 'FirePlace_351')
            actions = ActionChains(driver)
            actions.move_to_element(element).perform()
            driver.find_element(By.ID, 'select2-ParkingID_375-container').click()
            time.sleep(1)
            driver.find_element(By.XPATH, 'html/body/span/span/span[2]/ul/li[' + str(x) + ']').click()
        else:
            pass
            '''აუზი - აირჩიე'''
            #driver.find_element(By.ID, 'select2-PoolType_372-container').click()
            #ღია, დახურული
            #driver.find_element(By.XPATH, 'html/body/span/span/span[2]/ul/li[2]').click()
            '''ცხელი წყალი - აირჩიე'''
        if dict['HotWater'] != 0:
            driver.find_element(By.ID, 'select2-HotWaterID_391-container').click()
            time.sleep(1)
            if dict['HotWater'] == 'გაზის გამაცხელებელი':
                x = 1
            elif dict['HotWater'] == 'ავზი':
                x = 2
            elif dict['HotWater'] == 'დენის გამაცხელებელი':
                x = 3
            elif dict['HotWater'] == 'ბუნებრივი ცხელი წყალი':
                x = 4
            elif dict['HotWater'] == 'მზის გამათბობელი':
                x = 5
            else:
                x = 6
            driver.find_element(By.XPATH, 'html/body/span/span/span[2]/ul/li[' + str(x) + ']').click()
        else:
            pass
            '''გათბობა - აირჩიე'''
        if dict['gatboba'] != 0:
            driver.find_element(By.ID, 'select2-WarmingID_595-container').click()
            if dict['gatboba'] == 'ცენტრალური გათბობა':
                x = 1
            elif dict['gatboba'] == 'გაზის გამათბობელი':
                x = 2
            elif dict['gatboba'] == 'დენის გამათბობელი':
                x = 3
            else:
                x = 4
            time.sleep(1)
            driver.find_element(By.XPATH, 'html/body/span/span/span[2]/ul/li[' + str(x) + ']').click()
        else:
            pass
            '''ბუხარი'''
        if dict['buxari'] != 0:
            driver.find_element(By.ID, 'FirePlace_351').click()
        else:
            pass
            ''' ბუნებრივი აირი'''
        if dict['Gas'] != 0:
            driver.find_element(By.ID, 'Gas_382').click()
        else:
            pass
            '''სიგნალიზაცია'''
            #driver.find_element(By.ID, 'Alarm_578').click()
            '''სამგზავრო ლიფტი'''
        if dict['ElevatorRegular'] != 0:
            driver.find_element(By.ID, 'Elevator1_579').click()
        else:
            pass
            '''სატვირთო ლიფტი'''
        if dict['ElevatorBig'] != 0:
            driver.find_element(By.ID, 'Elevator2_580').click()
        else:
            pass
            '''ინტერნეტი'''
        if dict['Internet'] != 0:
            driver.find_element(By.ID, 'Internet_661').click()
        else:
            pass
        time.sleep(3)
        #SCROLLING
        element = driver.find_element(By.ID, 'Price')
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
        time.sleep(1)
        #driver.find_element(By.ID, 'dropdownMenuButton').click()
        #time.sleep(3)
        #driver.find_element(By.XPATH, "//label[@onclick='myproduct.select.currency(this);']").click()
        driver.find_element(By.XPATH, '/html/body/div[3]/div/div/form/div/div[2]/section[5]/div[2]/div[2]/input').send_keys(dict['total_price'])
        time.sleep(1)
        driver.find_element(By.XPATH, "html/body/div[3]/div/div/form/div/div[2]/section[5]/div[4]/div/div[2]/input").send_keys(name)
        time.sleep(1)
        driver.find_element(By.XPATH, "html/body/div[3]/div/div/form/div/div[2]/section[5]/div[4]/div[2]/div[2]/input").send_keys(phone_number)
        time.sleep(1)
        #inputting images
        #VideoUrl
        element = driver.find_element(By.ID, 'VideoUrl')
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
        '''adding pics'''
        driver.find_element(By.ID, 'CommentGeo').send_keys(dict['comment'])
        time.sleep(1)
        driver.find_element(By.ID, 'profile-tab').click()
        time.sleep(3)
        driver.find_element(By.XPATH, '/html/body/div[3]/div/div/form/div/div[2]/section[3]/div/div[2]/div/div/a').click()
        time.sleep(1)
        driver.find_element(By.ID, 'contact-tab').click()
        time.sleep(3)
        driver.find_element(By.XPATH, '/html/body/div[3]/div/div/form/div/div[2]/section[3]/div/div[3]/div/div/a').click()
        time.sleep(1)
        #driver.find_element(By.ID, 'contact-tab').click()
        driver.find_element(By.ID, "images").send_keys(seet)
        time.sleep(1)
        '''ავეჯი და ტექნიკა კი-არა'''
        driver.find_element(By.XPATH, "//label[@for='HasFurnitureAndTechnic_385']").click()
        if dict['Phone'] != 0:
            driver.find_element(By.ID, "Telephone_387").click()
        else:
            pass
        if dict['TV'] != 0:
            driver.find_element(By.ID, 'TV_388').click()
        else:
            pass
            '''კონდიციონერი'''
        if dict['conditioner'] != 0:
            driver.find_element(By.ID, 'Conditioner_389').click()
        else:
            pass
            '''მაცივარი'''
        #driver.find_element(By.ID, 'Refrigerator_599').click()
        '''სარეცხი მანქანა'''
        #driver.find_element(By.ID, 'WashingMachine_600').click()
        '''ჭურჭლის სარეცხი მანქანა'''
        #driver.find_element(By.ID, 'Dishwasher_601').click()
        '''ქურა (გაზის/ელექტრო)'''
        #driver.find_element(By.ID, 'Curry_602').click()
        '''ღუმელი'''
        #driver.find_element(By.ID, 'Furnace_603').click()
        '''ავეჯი'''
        if dict['Furniture'] != 0:
            driver.find_element(By.ID, 'Furniture_604').click()
        else:
            pass
        element = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/form/div/div[2]/div[2]/div[2]/button")
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
        time.sleep(1)
        try:
            driver.execute_script("arguments[0].click();", element)
        except:
            driver.find_element(By.XPATH, "/html/body/div[3]/div/div/form/div/div[2]/div[2]/div[2]/button").click()
        time.sleep(1)
        driver.find_element(By.XPATH, "//label[@for='payBalance']").click()
        driver.find_element(By.ID, "paymentButton").click()
        time.sleep(3)
        sql = "DELETE FROM Phonebookk LIMIT 1"
        cursor.execute(sql)
        connection.commit()
        driver.quit()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(service=Service(executable_path=os.environ.get("CHROMEDRIVER_PATH")), options=chrome_options)
        time.sleep(2)
        dict = get_needed_info()
        seet = string()
        time.sleep(2)
        name = "Flatz"
        #driver.maximize_window()
        time.sleep(3)
        driver.get("https://martivad.herokuapp.com/refresh")
        time.sleep(2)
        driver.quit()
        return "done"
    except:
        #return 'done'
        return "error"

@app.route('/while_loop')
def while_loop():
    connection = sqlite3.connect(str(os.getcwd()) + "/phonebook.db")
    cursor = connection.cursor()
    query1 = "SELECT * from Phonebookk"
    result = cursor.execute(query1)
    result = result.fetchall()
    return redirect(url_for('refresh'))


@app.route('/cong',  methods=['GET', 'POST'])
def index1():
    if request.method == 'POST':
        session['url'] = str(lst2[0])
        lst2.remove(lst2[0])
        lst2.append(request.form['url'])
        return session['url']+'''
            <form method="post">
                <p><input type=text name=url>
                <p>
                <p><input type=submit value=Go>
            </form>
        '''
    return 'congrats you found secret page :P' + '''
        <form method="post">
            <p><input type=text name=url>
            <p>
            <p><input type=submit value=Go>
        </form>
    '''


@app.route('/', methods=['GET', 'POST'])
def index():
    #driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    if request.method == 'POST':
        name = request.form["username"]
        connection = sqlite3.connect(str(os.getcwd()) + "/phonebook.db")
        cursor = connection.cursor()
        query1 = "SELECT * from Phonebookk"
        result = cursor.execute(query1)
        result = result.fetchall()
        if len(result) == 0:
            query1 = "INSERT INTO Phonebookk VALUES('{n}')".format(n = name)
            cursor.execute(query1)
            connection.commit()
            return redirect(url_for('refresh'))
        else:
            query1 = "INSERT INTO Phonebookk VALUES('{n}')".format(n = name)
            cursor.execute(query1)
            connection.commit()
            return redirect(url_for('resultpage'))
    return 'გთხოვთ შეიყვანოთ განცხადების ლინკი'+'''
        <form method="post">
            <p><input type=text name=username>
            <p>
            <p><input type=submit value=Go>
        </form>
    '''

@app.route('/resultpage', methods = ['GET', 'POST'])
def resultpage():
    connection = sqlite3.connect(str(os.getcwd()) + "/phonebook.db")
    cursor = connection.cursor()
    query1 = "SELECT * from Phonebookk"
    result = cursor.execute(query1)
    result = result.fetchall()
    if request.method == "POST":
        return redirect(url_for('index'))
    return "tqveni rigis nomeria : " + str(len(result))+" This is your data ---->"+ str(result) +'''
        <form method="post">

            <p><input type=submit value=Okay>
        </form>
    '''

@app.route('/delete', methods = ['GET', "POST"])
def delete():
    connection = sqlite3.connect(str(os.getcwd()) + "/phonebook.db")
    cursor = connection.cursor()
    query1 = "SELECT * from Phonebookk"
    result = cursor.execute(query1)
    result = result.fetchall()
    if request.method == "POST":
        name = request.form["NEW"]
        connection = sqlite3.connect(str(os.getcwd()) + "/phonebook.db")
        sql = "DELETE FROM Phonebookk LIMIT 1"
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        return redirect(url_for('delete'))
    return  'want to delete? here is data'+ str(result) + '''
        <form method="post">
            <p><input type=text name=NEW>
            <p>
            <p><input type=submit value=SURE>
        </form>
    '''

@app.route('/gogo')
def gogo():
    return get_content()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('login'))
